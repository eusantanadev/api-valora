import { FormEvent, useEffect, useRef, useState } from "react";
import "./CadastroModal.css";
import { api, type RegisterPayload } from "../services/valoraApi";

type CadastroModalProps = {
  onClose: () => void;
  onRegistered?: () => void;
};

export default function CadastroModal({ onClose, onRegistered }: CadastroModalProps) {
  const [showPassword, setShowPassword] = useState(false);
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(false);
  const dialogRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
      if (event.key === "Tab") {
        const focusable = dialogRef.current?.querySelectorAll<HTMLElement>(
          'button:not([disabled]), input:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])',
        );
        if (!focusable?.length) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
    };
    window.addEventListener("keydown", onKeyDown);
    dialogRef.current?.querySelector<HTMLElement>("input")?.focus();
    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [onClose]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setFeedback("");
    const data = new FormData(event.currentTarget);
    const senha = String(data.get("senha") ?? "");
    const confirmar = String(data.get("confirmarSenha") ?? "");
    if (senha !== confirmar) {
      setFeedback("As senhas precisam ser iguais.");
      return;
    }

    const payload: RegisterPayload = {
      nome: String(data.get("nome") ?? "").trim(),
      email: String(data.get("email") ?? "").trim(),
      telefone: String(data.get("telefone") ?? "").trim(),
      cpf: String(data.get("cpf") ?? "").replace(/\D/g, ""),
      dataNascimento: String(data.get("nascimento") ?? ""),
      senha,
      endereco: {
        logradouro: String(data.get("logradouro") ?? "").trim(),
        bairro: String(data.get("bairro") ?? "").trim(),
        cep: String(data.get("cep") ?? "").trim(),
        cidade: String(data.get("cidade") ?? "").trim(),
        uf: String(data.get("uf") ?? "").trim().toUpperCase(),
        numero: String(data.get("numero") ?? "").trim(),
        complemento: String(data.get("complemento") ?? "").trim(),
      },
    };

    setLoading(true);
    try {
      await api.auth.register(payload);
      setFeedback("Conta criada! Entrando na Valora...");
      onRegistered?.();
    } catch (error) {
      setFeedback(error instanceof Error ? error.message : "Não foi possível concluir o cadastro.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="valora-modal-backdrop" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}>
      <div className="valora-cadastro-modal" role="dialog" aria-modal="true" aria-labelledby="valora-cadastro-title" ref={dialogRef}>
        <button type="button" className="valora-modal-close" aria-label="Fechar cadastro" onClick={onClose}>×</button>
        <div className="valora-cadastro-brand"><img src="/logo-certo-1@2x.png" alt="" /> <span>Valora</span></div>
        <div className="valora-cadastro-heading">
          <p className="valora-cadastro-kicker">COMECE SUA JORNADA</p>
          <h2 id="valora-cadastro-title">Crie sua conta</h2>
          <p>Seu dinheiro, seus planos. Tudo em um só lugar.</p>
        </div>
        <form className="valora-cadastro-form" onSubmit={handleSubmit}>
          <label>Nome completo<input name="nome" placeholder="Digite seu nome completo" autoComplete="name" required /></label>
          <div className="valora-cadastro-row">
            <label>E-mail<input name="email" type="email" placeholder="seuemail@exemplo.com" autoComplete="email" required /></label>
            <label>Telefone<input name="telefone" type="tel" placeholder="(11) 99999-9999" autoComplete="tel" required /></label>
          </div>
          <div className="valora-cadastro-row">
            <label>CPF<input name="cpf" placeholder="00000000000" inputMode="numeric" maxLength={14} onChange={(event) => { event.currentTarget.value = event.currentTarget.value.replace(/\D/g, "").slice(0, 11); }} required /></label>
            <label>Data de nascimento<input name="nascimento" type="date" autoComplete="bday" required /></label>
          </div>
          <div className="valora-cadastro-row">
            <label>CEP<input name="cep" placeholder="00000-000" inputMode="numeric" required /></label>
            <label>UF<input name="uf" placeholder="SP" maxLength={2} required /></label>
          </div>
          <label>Logradouro<input name="logradouro" placeholder="Rua, avenida..." required /></label>
          <div className="valora-cadastro-row">
            <label>Número<input name="numero" placeholder="Número" /></label>
            <label>Bairro<input name="bairro" placeholder="Bairro" required /></label>
          </div>
          <div className="valora-cadastro-row">
            <label>Cidade<input name="cidade" placeholder="Cidade" required /></label>
            <label>Complemento<input name="complemento" placeholder="Opcional" /></label>
          </div>
          <label>Senha
            <div className="valora-cadastro-password"><input name="senha" type={showPassword ? "text" : "password"} placeholder="Crie uma senha" autoComplete="new-password" minLength={8} maxLength={20} required /><button type="button" onClick={() => setShowPassword((value) => !value)}>{showPassword ? "Ocultar" : "Mostrar"}</button></div>
          </label>
          <label>Confirmar senha<input name="confirmarSenha" type="password" placeholder="Repita sua senha" autoComplete="new-password" minLength={8} maxLength={20} required /></label>
          {feedback && <p className="valora-cadastro-feedback" role="status">{feedback}</p>}
          <button type="submit" className="valora-cadastro-submit" disabled={loading}>{loading ? "Criando conta..." : "Criar minha conta"} <span aria-hidden="true">→</span></button>
        </form>
        <p className="valora-cadastro-footer">Já tem uma conta? <button type="button" onClick={onClose}>Entrar</button></p>
      </div>
    </div>
  );
}
