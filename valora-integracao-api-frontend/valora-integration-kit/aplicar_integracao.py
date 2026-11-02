#!/usr/bin/env python3
"""Aplica o kit de integração aos clones locais dos repositórios Valora.

Exemplo:
  python aplicar_integracao.py --api ../api-valora --frontend ../Valora/Valora

O instalador cria backups .bak dos arquivos que serão substituídos.
"""
from __future__ import annotations

import argparse
import importlib.util
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def resolve_frontend(candidate: Path) -> Path:
    candidate = candidate.expanduser().resolve()
    if (candidate / "src").is_dir():
        return candidate
    nested = candidate / "Valora"
    if (nested / "src").is_dir():
        return nested
    raise SystemExit(
        f"Não encontrei src/ em {candidate} nem em {nested}. "
        "Informe a pasta do front-end React (a pasta que contém src/)."
    )


def backup_and_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        backup = destination.with_name(destination.name + ".bak")
        if not backup.exists():
            shutil.copy2(destination, backup)
    shutil.copy2(source, destination)
    print(f"OK  {destination}")


def load_page_patcher():
    script = ROOT / "scripts" / "patch_pages.py"
    spec = importlib.util.spec_from_file_location("valora_patch_pages", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("Não foi possível carregar scripts/patch_pages.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser(description="Aplica a integração da API com o front-end Valora.")
    parser.add_argument("--api", required=True, help="Pasta raiz do clone api-valora")
    parser.add_argument("--frontend", required=True, help="Pasta do clone do front-end ou a pasta Valora/ dentro dele")
    args = parser.parse_args()

    api = Path(args.api).expanduser().resolve()
    frontend = resolve_frontend(Path(args.frontend))

    if not (api / "pom.xml").is_file() or not (api / "src/main/java").is_dir():
        raise SystemExit(f"Pasta da API não reconhecida: {api}")
    for relative in (
        "src/pages/Login.tsx",
        "src/pages/Categorias.tsx",
        "src/pages/Caixinhas.tsx",
        "src/pages/DetalhesCaixinha.tsx",
        "src/components/CadastroModal.tsx",
    ):
        if not (frontend / relative).is_file():
            raise SystemExit(f"Front-end não corresponde à versão esperada do repositório: falta {relative}")

    # Back-end: sobrescreve somente os arquivos que fazem parte da integração.
    backend_overlay = ROOT / "backend" / "src" / "main" / "java" / "com" / "valora" / "api"
    backend_target = api / "src" / "main" / "java" / "com" / "valora" / "api"
    if not backend_overlay.is_dir():
        raise SystemExit("Pasta backend/ do pacote está incompleta.")
    for source in sorted(backend_overlay.rglob("*.java")):
        relative = source.relative_to(backend_overlay)
        backup_and_copy(source, backend_target / relative)

    # Front-end: arquivos de infraestrutura e componentes de login/cadastro.
    frontend_overlay = ROOT / "frontend" / "Valora"
    for relative in (
        Path("src/App.tsx"),
        Path("src/components/FormContent.tsx"),
        Path("src/components/CadastroModal.tsx"),
        Path("src/services/valoraApi.ts"),
    ):
        backup_and_copy(frontend_overlay / relative, frontend / relative)

    # Mantém configurações locais existentes; cria um .env.local apenas se não houver um.
    env_example = frontend_overlay / ".env.example"
    env_local = frontend / ".env.local"
    if not env_local.exists():
        shutil.copy2(env_example, env_local)
        print(f"OK  {env_local} (criado a partir de .env.example)")
    else:
        print(f"INFO {env_local} já existe; não foi alterado.")

    # Conecta os estados/handlers das páginas existentes aos serviços HTTP.
    patcher = load_page_patcher()
    patcher.patch_login(frontend)
    patcher.patch_categories(frontend)
    patcher.patch_cashboxes(frontend)
    patcher.patch_details(frontend)

    print("\nIntegração aplicada.")
    print("Back-end: confira DB_URL, DB_USERNAME, DB_PASSWORD e JWT_SECRET antes de iniciar.")
    print("Front-end: execute npm install e npm run start dentro da pasta do React.")
    print("Os arquivos originais substituídos foram preservados com a extensão .bak.")


if __name__ == "__main__":
    main()
