import { ReactNode, useEffect } from "react";
import {
  Navigate,
  Routes,
  Route,
  useNavigationType,
  useLocation,
} from "react-router-dom";
import Login from "./pages/Login";
import Incio from "./pages/Incio";
import Movimentacoes from "./pages/Movimentacoes";
import Caixinhas from "./pages/Caixinhas";
import DetalhesCaixinha from "./pages/DetalhesCaixinha";
import Categorias from "./pages/Categorias";
import ContasConectadas from "./pages/ContasConectadas";
import { getAccessToken } from "./services/valoraApi";

function Protected({ children }: { children: ReactNode }) {
  return getAccessToken() ? <>{children}</> : <Navigate to="/" replace />;
}

function App() {
  const action = useNavigationType();
  const location = useLocation();
  const pathname = location.pathname;

  useEffect(() => {
    if (action !== "POP") window.scrollTo(0, 0);
  }, [action, pathname]);

  useEffect(() => {
    const titleByPath: Record<string, string> = {
      "/": "Valora | Entrar",
      "/dashboard": "Valora | Início",
      "/movimentacoes": "Valora | Movimentações",
      "/caixinhas": "Valora | Caixinhas",
      "/categorias": "Valora | Categorias",
      "/contas-conectadas": "Valora | Contas conectadas",
    };
    document.title = titleByPath[pathname] || "Valora";
  }, [pathname]);

  useEffect(() => {
    const onExpired = () => window.location.replace("/");
    window.addEventListener("valora:session-expired", onExpired);
    return () => window.removeEventListener("valora:session-expired", onExpired);
  }, []);

  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/dashboard" element={<Protected><Incio /></Protected>} />
      <Route path="/02-incio" element={<Protected><Incio /></Protected>} />
      <Route path="/movimentacoes" element={<Protected><Movimentacoes /></Protected>} />
      <Route path="/03-movimentacoes" element={<Protected><Movimentacoes /></Protected>} />
      <Route path="/caixinhas" element={<Protected><Caixinhas /></Protected>} />
      <Route path="/04-caixinhas" element={<Protected><Caixinhas /></Protected>} />
      <Route path="/categorias" element={<Protected><Categorias /></Protected>} />
      <Route path="/06-categorias" element={<Protected><Categorias /></Protected>} />
      <Route path="/contas-conectadas" element={<Protected><ContasConectadas /></Protected>} />
      <Route path="/07-conectar-conta" element={<Protected><ContasConectadas /></Protected>} />
      <Route path="/detalhes-caixinha" element={<Protected><DetalhesCaixinha /></Protected>} />
      <Route path="/05-detalhes-da-caixinha" element={<Protected><DetalhesCaixinha /></Protected>} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

export default App;
