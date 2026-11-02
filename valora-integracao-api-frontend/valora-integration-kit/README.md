# Valora — integração da API com o front-end

Este pacote aplica a integração sobre os **arquivos atuais dos repositórios indicados**, preservando os componentes e o layout existentes. Ele não recria o front-end.

## O que a integração liga

- Login: `POST /api/auth`, gravação do JWT na sessão e consulta ao perfil por `GET /api/usuario/me`.
- Cadastro: `POST /api/usuario`, respeitando os campos e validações exigidos pela API, e login automático após o cadastro.
- Categorias: listar, cadastrar, editar e excluir usando os endpoints `/api/categorias`.
- Caixinhas: listar, cadastrar, abrir detalhes, atualizar nome/meta/saldo e excluir usando `/api/caixinhas`.
- Rotas internas do front-end passam a exigir uma sessão com token.
- CORS passa a aceitar o Vite local (`localhost:5173` e `127.0.0.1:5173`).
- A API passa a derivar o dono de categorias e caixinhas do JWT, evitando aceitar o `idUsuario` enviado pelo navegador como fonte de autorização.
- As respostas de categorias e caixinhas usam DTOs que não serializam o objeto completo `UsuarioModel`.

## Estrutura do pacote

- `backend/`: arquivos Java novos/alterados para a API.
- `frontend/Valora/`: arquivos de infraestrutura, serviços HTTP e componentes React integrados.
- `scripts/patch_pages.py`: liga as telas já existentes de categorias, caixinhas e detalhes à API.
- `aplicar_integracao.py`: instalador que copia os arquivos, cria backups e aplica o patch das páginas em um único comando.

## Aplicar aos clones locais

Primeiro, tenha os dois repositórios clonados no computador:

- API: `https://github.com/ArthurTorres1/api-valora`
- Front-end: `https://github.com/BTaques/Valora`

Extraia este pacote em uma pasta. Abra o terminal nessa pasta e execute (ajuste os caminhos para as pastas onde clonou os projetos):

### Windows

```powershell
py aplicar_integracao.py --api "C:\caminho\api-valora" --frontend "C:\caminho\Valora\Valora"
```

Também é aceito passar a raiz do clone do front-end (`C:\caminho\Valora`); o instalador localiza automaticamente a pasta interna `Valora/` que contém `src/`.

### macOS / Linux

```bash
python3 aplicar_integracao.py --api ../api-valora --frontend ../Valora/Valora
```

O instalador faz backup dos arquivos Java e React substituídos com a extensão `.bak`. Ele também cria `frontend/.env.local` com a URL local da API, caso o arquivo ainda não exista. Um `.env.local` já existente é preservado.

## Executar a API

O projeto usa Java 21, Spring Boot 3, Maven Wrapper e Oracle. Configure as variáveis de ambiente esperadas por `src/main/resources/application.properties`:

| Variável | Conteúdo |
|---|---|
| `DB_URL` | URL JDBC do Oracle, por exemplo `jdbc:oracle:thin:@//HOST:PORT/SERVICE_NAME` |
| `DB_USERNAME` | Usuário do banco Oracle |
| `DB_PASSWORD` | Senha do banco Oracle |
| `JWT_SECRET` | Segredo aleatório com pelo menos 32 bytes para assinar os tokens JWT |

Na pasta `api-valora`:

```bash
./mvnw spring-boot:run
```

No Windows:

```powershell
.\mvnw.cmd spring-boot:run
```

A API ficará disponível em `http://localhost:8080`, desde que o Oracle esteja acessível e as migrações Flyway sejam executadas sem erro.

## Executar o front-end

Na pasta React que contém `package.json`:

```bash
npm install
npm run start
```

O Vite usa normalmente `http://localhost:5173`. O arquivo `.env.local` contém:

```env
VITE_API_URL=http://localhost:8080
```

Depois de instalar dependências, valide também a compilação de produção:

```bash
npm run build
```

## Limitações que existem na API original

A integração não inventa endpoints que não estão no repositório original:

- **Movimentações:** a API atual não possui entidade, tabela, repositório ou controller de movimentações. Assim, o extrato, o cadastro de transações e os indicadores que dependem de transações ainda não são persistidos pela API. Na tela de detalhes da caixinha, depósitos/retiradas atualizam o saldo da caixinha, mas o histórico individual dessas operações não é gravado.
- **Open Finance:** a tela de conexão bancária é visual. A API possui um CRUD simples de contas, mas não possui integração Open Finance, consentimento bancário ou sincronização automática com instituições. Não conecte credenciais bancárias a essa tela.
- **Atributos visuais de categoria:** a tabela de categorias na API guarda o nome, mas não guarda cor ou ícone. Esses atributos continuam sendo apenas visuais no front-end e podem voltar ao padrão após recarregar.
- **Dashboard e tela de movimentações:** como não há API de movimentações, esses dados não podem ser convertidos em dados financeiros persistentes sem desenvolver essa parte do back-end.

## Segurança e produção

O pacote restringe categorias e caixinhas ao usuário autenticado. Ainda assim, antes de publicar a aplicação, revise também as rotas administrativas/de usuários e o CRUD de contas que já existiam na API; não exponha uma API financeira publicamente sem revisar a autorização por proprietário. Para produção, inclua o domínio real do front-end na política de CORS e use HTTPS. Nunca publique `.env.local`, credenciais Oracle ou `JWT_SECRET` no Git.

## Validação

Este pacote foi montado a partir das estruturas e contratos lidos nos dois repositórios. Não foi possível executar um teste ponta a ponta aqui: a API depende de credenciais e acesso a um Oracle, e este ambiente não tem acesso de rede ao GitHub para clonar os projetos nem Maven/dependências instalados para compilar os repositórios. Portanto, após aplicar, execute `npm run build` e suba a API no seu ambiente Oracle antes de considerar o sistema validado.

## Observação sobre os repositórios remotos

A conexão com GitHub reportou permissão de leitura (`push: false`) para ambos os repositórios. Por isso, não foi possível gravar commits nos repositórios originais. O instalador aplica as alterações nos clones locais, sem alterar o histórico remoto.
