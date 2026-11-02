import { FormEvent, FunctionComponent, useState } from "react";
import { useNavigate } from "react-router-dom";
import Component1 from "./Component1";
import { api } from "../services/valoraApi";

export type FormContentType = { className?: string };

const FormContent: FunctionComponent<FormContentType> = ({ className = "" }) => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(false);

  async function entrar(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setFeedback("");
    setLoading(true);
    try {
      await api.auth.login(email.trim(), senha);
      navigate("/dashboard", { replace: true });
    } catch (error) {
      setFeedback(error instanceof Error ? error.message : "Não foi possível entrar.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      onSubmit={entrar}
      className={`valora-login-form m-0 self-stretch flex flex-col items-center py-0 pl-0 pr-12 box-border gap-[19px] max-w-full mq825:pr-6 mq825:box-border ${className}`}
    >
      <div className="self-stretch flex flex-col items-center py-0 px-5 box-border gap-1.5 max-w-full">
        <div className="w-full flex items-start pt-0 pb-[9px] pl-0 pr-4 box-border max-w-[366px]"><Component1 /></div>
        <h2 className="m-0 self-stretch relative text-[34px] font-semibold font-[Inter] text-[#1f1447] text-center mq825:text-[27px] mq450:text-xl">Dê valor aos seus planos.</h2>
        <div className="self-stretch relative text-base font-[Inter] text-[#756e94] text-center">Seu dinheiro, sob seu controle.</div>
      </div>
      <div className="self-stretch flex flex-col items-start pt-[39px] px-0 pb-[13px] box-border gap-3 max-w-full">
        <label htmlFor="valora-email" className="self-stretch relative text-[13px] font-semibold font-[Inter] text-[#1a1729] text-left">E-mail</label>
        <div className="self-stretch h-[60px] rounded-xl bg-[#fff] border-[#d1ccdb] border-solid border-[1px] box-border overflow-hidden shrink-0 flex items-start pt-4 px-[13px] pb-[25px] max-w-full">
          <input id="valora-email" className="w-full [border:none] [outline:none] font-[Inter] text-sm bg-[transparent] h-[17px] flex-1 relative text-[#6e6980] text-left inline-block min-w-[250px] p-0 max-w-full" placeholder="marina@email.com" type="email" autoComplete="email" required value={email} onChange={(event) => setEmail(event.target.value)} />
        </div>
      </div>
      <div className="self-stretch flex flex-col items-center pt-0 px-0 pb-[9px] box-border gap-3 max-w-full">
        <label htmlFor="valora-password" className="self-stretch relative text-[13px] font-semibold font-[Inter] text-[#1a1729] text-left">Senha</label>
        <div className="self-stretch flex items-start pt-0 px-0 pb-px box-border max-w-full">
          <div className="h-[60px] flex-1 rounded-xl bg-[#fff] border-[#d1ccdb] border-solid border-[1px] box-border overflow-hidden flex items-start pt-4 px-[13px] pb-[25px] max-w-full">
            <input id="valora-password" className="w-full [border:none] [outline:none] font-[Inter] text-sm bg-[transparent] h-[17px] flex-1 relative text-[#6e6980] text-left inline-block min-w-[250px] p-0 max-w-full" placeholder="••••••••••" type="password" autoComplete="current-password" required value={senha} onChange={(event) => setSenha(event.target.value)} />
          </div>
        </div>
        <div className="w-full relative text-[13px] font-semibold font-[Inter] text-[#6e3bd1] text-right inline-block max-w-[406px] mq450:max-w-full">Esqueci minha senha</div>
      </div>
      {feedback && <p role="alert" className="w-full max-w-[406px] text-[12px] text-[#b42318]">{feedback}</p>}
      <button disabled={loading} className="disabled:opacity-60 cursor-pointer [border:none] pt-[18px] px-[23px] pb-5 bg-[transparent] self-stretch rounded-xl [background:linear-gradient(90deg,_#6329db,_#4514ad)] overflow-hidden flex items-center justify-between flex-wrap content-center gap-0 [row-gap:20px]" type="submit">
        <span className="w-[238px] relative text-base font-semibold font-[Inter] text-[#fff] text-right inline-block min-w-[48px] max-w-[238px]">{loading ? "Entrando..." : "Entrar"}</span>
        <img className="h-[22px] w-[22px] relative" alt="" src="/Arrow-right.svg" />
      </button>
      <div className="self-stretch flex items-center justify-center flex-wrap content-center pt-0 pb-2 pl-5 pr-[18px] gap-[18px]">
        <div className="h-px flex-1 relative bg-[#b6b2bd] min-w-[96px] max-w-[120px]" />
        <div className="relative text-xs font-[Inter] text-[#6e6980] text-left">ou acesse com</div>
        <div className="h-px flex-1 relative bg-[#b6b2bd] min-w-[96px] max-w-[120px]" />
      </div>
      <button className="cursor-pointer border-[rgba(0,0,0,0.2)] border-solid border-[1px] pt-3.5 px-5 pb-[23px] bg-[#fff] self-stretch h-14 rounded-xl box-border overflow-hidden shrink-0 flex items-center justify-center" type="button" disabled>
        <span className="flex-1 relative text-sm font-semibold font-[Inter] text-[#1a1729] whitespace-pre-wrap text-left inline-block max-w-[184.1px]">G Entrar com Google (indisponível)</span>
      </button>
    </form>
  );
};

export default FormContent;
