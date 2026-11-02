const API_URL = (import.meta.env.VITE_API_URL || "http://localhost:8080").replace(/\/$/, "");
const TOKEN_KEY = "valora.accessToken";
const USER_KEY = "valora.currentUser";

export type ValoraUser = {
  id: number;
  nome: string;
  email: string;
  telefone: string;
  endereco?: {
    logradouro: string;
    bairro: string;
    cep: string;
    cidade: string;
    uf: string;
    numero?: string;
    complemento?: string;
  };
};

export type CategoryDto = {
  idCategoria: number;
  idUsuario: number;
  nmCategoria: string;
  dtCriacao: string;
};

export type CashboxDto = {
  idCaixinha: number;
  idUsuario: number;
  nmCaixinha: string;
  vlMeta: number;
  vlAtual: number;
  dtCriacao: string;
};

export type AccountDto = {
  id: number;
  nome: string;
  saldo: number;
};

type RequestOptions = Omit<RequestInit, "body"> & {
  body?: unknown;
  authenticated?: boolean;
};

function readJsonSafely(text: string): unknown {
  if (!text) return null;
  try {
    return JSON.parse(text) as unknown;
  } catch {
    return text;
  }
}

function getMessage(payload: unknown, fallback: string): string {
  if (typeof payload === "string" && payload.trim()) return payload;
  if (payload && typeof payload === "object") {
    const value = payload as Record<string, unknown>;
    for (const key of ["message", "detail", "erro", "error"]) {
      if (typeof value[key] === "string" && value[key]) return value[key] as string;
    }
    if (Array.isArray(value.errors) && value.errors.length) {
      return value.errors
        .map((item) => {
          if (item && typeof item === "object") {
            const entry = item as Record<string, unknown>;
            return String(entry.defaultMessage || entry.message || "");
          }
          return String(item);
        })
        .filter(Boolean)
        .join(" ");
    }
  }
  return fallback;
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { authenticated = true, headers: customHeaders, body, ...rest } = options;
  const headers = new Headers(customHeaders);
  if (body !== undefined) headers.set("Content-Type", "application/json");

  const token = authenticated ? getAccessToken() : null;
  if (token) headers.set("Authorization", `Bearer ${token}`);

  let response: Response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      ...rest,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  } catch {
    throw new Error(`Não foi possível acessar a API em ${API_URL}. Confira se o back-end está ligado e se a URL está correta.`);
  }

  const raw = await response.text();
  const payload = readJsonSafely(raw);
  if (!response.ok) {
    if (response.status === 401 && authenticated && token) {
      clearSession();
      window.dispatchEvent(new Event("valora:session-expired"));
    }
    throw new Error(getMessage(payload, `A API respondeu com HTTP ${response.status}.`));
  }

  if (response.status === 204 || payload === null) return undefined as T;
  return payload as T;
}

export function getAccessToken(): string | null {
  return sessionStorage.getItem(TOKEN_KEY);
}

export function getStoredUser(): ValoraUser | null {
  const raw = sessionStorage.getItem(USER_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as ValoraUser;
  } catch {
    sessionStorage.removeItem(USER_KEY);
    return null;
  }
}

export function clearSession(): void {
  sessionStorage.removeItem(TOKEN_KEY);
  sessionStorage.removeItem(USER_KEY);
}

async function fetchCurrentUser(): Promise<ValoraUser> {
  const user = await request<ValoraUser>("/api/usuario/me");
  sessionStorage.setItem(USER_KEY, JSON.stringify(user));
  return user;
}

export type RegisterPayload = {
  nome: string;
  email: string;
  telefone: string;
  senha: string;
  cpf: string;
  dataNascimento: string;
  endereco: {
    logradouro: string;
    bairro: string;
    cep: string;
    cidade: string;
    uf: string;
    numero?: string;
    complemento?: string;
  };
};

export const api = {
  auth: {
    async login(email: string, senha: string): Promise<ValoraUser> {
      clearSession();
      const result = await request<{ token: string }>("/api/auth", {
        method: "POST",
        authenticated: false,
        body: { email, senha },
      });
      if (!result?.token) throw new Error("A API não retornou o token de autenticação.");
      sessionStorage.setItem(TOKEN_KEY, result.token);
      try {
        return await fetchCurrentUser();
      } catch (error) {
        clearSession();
        throw error;
      }
    },

    async register(payload: RegisterPayload): Promise<ValoraUser> {
      await request<ValoraUser>("/api/usuario", {
        method: "POST",
        authenticated: false,
        body: payload,
      });
      return api.auth.login(payload.email, payload.senha);
    },

    async me(): Promise<ValoraUser> {
      return fetchCurrentUser();
    },

    logout(): void {
      clearSession();
    },
  },

  categorias: {
    list(): Promise<CategoryDto[]> {
      return request<CategoryDto[]>("/api/categorias");
    },
    get(id: number): Promise<CategoryDto> {
      return request<CategoryDto>(`/api/categorias/${id}`);
    },
    create(nome: string): Promise<CategoryDto> {
      return request<CategoryDto>("/api/categorias", {
        method: "POST",
        body: { idCategoria: null, idUsuario: null, nmCategoria: nome },
      });
    },
    update(id: number, nome: string): Promise<CategoryDto> {
      return request<CategoryDto>(`/api/categorias/${id}`, {
        method: "PUT",
        body: { idCategoria: id, idUsuario: null, nmCategoria: nome },
      });
    },
    remove(id: number): Promise<void> {
      return request<void>(`/api/categorias/${id}`, { method: "DELETE" });
    },
  },

  caixinhas: {
    list(): Promise<CashboxDto[]> {
      return request<CashboxDto[]>("/api/caixinhas");
    },
    get(id: number): Promise<CashboxDto> {
      return request<CashboxDto>(`/api/caixinhas/${id}`);
    },
    create(data: { nome: string; meta: number; valorAtual: number }): Promise<CashboxDto> {
      return request<CashboxDto>("/api/caixinhas", {
        method: "POST",
        body: {
          idCaixinha: null,
          idUsuario: null,
          nmCaixinha: data.nome,
          vlMeta: data.meta,
          vlAtual: data.valorAtual,
        },
      });
    },
    update(
      id: number,
      data: { nome: string; meta: number; valorAtual: number },
    ): Promise<CashboxDto> {
      return request<CashboxDto>(`/api/caixinhas/${id}`, {
        method: "PUT",
        body: {
          idCaixinha: id,
          idUsuario: null,
          nmCaixinha: data.nome,
          vlMeta: data.meta,
          vlAtual: data.valorAtual,
        },
      });
    },
    remove(id: number): Promise<void> {
      return request<void>(`/api/caixinhas/${id}`, { method: "DELETE" });
    },
  },

  contas: {
    list(): Promise<{ content: AccountDto[]; totalElements: number; totalPages: number }> {
      return request("/api/conta/listar-contas");
    },
    create(data: { nome: string; saldo: number; idUsuario: number }): Promise<AccountDto> {
      return request<AccountDto>("/api/conta", { method: "POST", body: data });
    },
  },
};
