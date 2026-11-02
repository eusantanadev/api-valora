#!/usr/bin/env python3
"""Adapta as páginas existentes de Categorias e Caixinhas sem recriar o layout.

Uso, dentro da pasta do kit:
  python scripts/patch_pages.py --frontend ../Valora

A opção --frontend deve apontar para a pasta raiz que contém src/.
O script cria cópias .bak antes de alterar cada arquivo.
"""
from __future__ import annotations
import argparse
import re
from pathlib import Path


def replace_once(source: str, pattern: str, replacement: str, label: str, flags: int = 0) -> str:
    updated, count = re.subn(pattern, replacement, source, count=1, flags=flags)
    if count != 1:
        print(f"Aviso: Trecho não encontrado em {label}. Pulando (pode já ter sido modificado).")
        return source
    return updated


def patch_categories(frontend: Path) -> None:
    path = frontend / "src/pages/Categorias.tsx"
    source = path.read_text(encoding="utf-8")
    source = source.replace(
        "import Topbar5 from '../components/Topbar5';",
        "import Topbar5 from '../components/Topbar5';\nimport { api, type CategoryDto } from '../services/valoraApi';",
        1,
    )
    source = replace_once(
        source,
        r"type Cat=\{name:string;color:string;bg:string;symbol:string;spent:number;percent:number\};",
        "type Cat={idCategoria?:number;name:string;color:string;bg:string;symbol:string;spent:number;percent:number};\n"
        "const fromApiCategory=(item:CategoryDto):Cat=>({idCategoria:item.idCategoria,name:item.nmCategoria,color:'#8159e0',bg:'#e9e3ff',symbol:'dots',spent:0,percent:0});",
        "Categorias.tsx: tipo Cat",
    )
    source = replace_once(source, r"const initial:Cat\[\]=\[[\s\S]*?\];\n", "", "Categorias.tsx: dados simulados")
    source = source.replace("const [cats,setCats]=useState<Cat[]>(initial)", "const [cats,setCats]=useState<Cat[]>([])", 1)
    source = source.replace(
        "[color,setColor]=useState('#8159e0');",
        "[color,setColor]=useState('#8159e0'),[apiError,setApiError]=useState('');",
        1,
    )
    source = replace_once(
        source,
        r"useEffect\(\(\)=>\{const f=\(\)=>setZoom\(Math\.max\(1,innerWidth/1440\)\);f\(\);window\.addEventListener\('resize',f\);return\(\)=>window\.removeEventListener\('resize',f\)\},\[\]\);",
        "useEffect(()=>{const f=()=>setZoom(Math.max(1,innerWidth/1440));f();window.addEventListener('resize',f);return()=>window.removeEventListener('resize',f)},[]);\n"
        "useEffect(()=>{let active=true;api.categorias.list().then(items=>{if(active)setCats(items.map(fromApiCategory))}).catch(error=>{if(active)setApiError(error instanceof Error?error.message:'Erro ao carregar categorias')});return()=>{active=false}},[]);",
        "Categorias.tsx: carregamento inicial",
    )
    source = replace_once(
        source,
        r"const remove=\(i:number\)=>\{[\s\S]*?const save=\(\)=>\{[\s\S]*?(?=\nreturn)",
        "const remove=async(i:number)=>{const item=cats[i];if(!item?.idCategoria)return;if(!window.confirm('Excluir a categoria '+item.name+'?'))return;try{await api.categorias.remove(item.idCategoria);setCats(old=>old.filter((_,j)=>j!==i));setApiError('')}catch(error){setApiError(error instanceof Error?error.message:'Não foi possível excluir a categoria')}};\n"
        "const save=async()=>{if(!name.trim())return;try{const result=editing===null?await api.categorias.create(name.trim()):await api.categorias.update(cats[editing].idCategoria!,name.trim());const normalized=fromApiCategory(result);setCats(old=>editing===null?[...old,normalized]:old.map((c,i)=>i===editing?{...normalized,color,bg:color+'20',symbol:c.symbol}:c));setModal(false);setApiError('')}catch(error){setApiError(error instanceof Error?error.message:'Não foi possível salvar a categoria')}};",
        "Categorias.tsx: ações de categoria",
        flags=re.S,
    )
    source = source.replace(
        "<p style={abs(254,144,650,24)} className=\"text-[#595291] text-[16px]\">Organize e personalize suas categorias de gastos.</p>",
        "<p style={abs(254,144,650,24)} className=\"text-[#595291] text-[16px]\">Organize e personalize suas categorias de gastos.</p>{apiError&&<p role=\"alert\" className=\"absolute left-[254px] top-[164px] text-[11px] text-red-600\">{apiError}</p>}",
        1,
    )
    source = source.replace("<b className=\"absolute left-[71px] top-[150px] text-[18px]\">R$ 1.250,30</b>", "<b className=\"absolute left-[71px] top-[150px] text-[18px]\">R$ 0,00</b>", 1)
    backup = path.with_suffix(path.suffix + ".bak")
    if not backup.exists(): backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    path.write_text(source, encoding="utf-8")


def patch_login(frontend: Path) -> None:
    path = frontend / "src/pages/Login.tsx"
    source = path.read_text(encoding="utf-8")
    source = source.replace(
        'import { FunctionComponent, useCallback, useState } from "react";',
        'import { FunctionComponent, useCallback, useState } from "react";\nimport { useNavigate } from "react-router-dom";',
        1,
    )
    source = source.replace(
        '  const [cadastroAberto, setCadastroAberto] = useState(false);',
        '  const navigate = useNavigate();\n  const [cadastroAberto, setCadastroAberto] = useState(false);',
        1,
    )
    source = source.replace(
        '{cadastroAberto && <CadastroModal onClose={fecharCadastro} />}',
        '{cadastroAberto && <CadastroModal onClose={fecharCadastro} onRegistered={() => { fecharCadastro(); navigate("/dashboard", { replace: true }); }} />}',
        1,
    )
    backup = path.with_suffix(path.suffix + ".bak")
    if not backup.exists(): backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    path.write_text(source, encoding="utf-8")


def patch_cashboxes(frontend: Path) -> None:
    path = frontend / "src/pages/Caixinhas.tsx"
    source = path.read_text(encoding="utf-8")
    source = source.replace(
        "import { GoalIcon } from '../components/GoalIcon';",
        "import { GoalIcon } from '../components/GoalIcon';\nimport { api, type CashboxDto } from '../services/valoraApi';",
        1,
    )
    source = replace_once(
        source,
        r"type Goal=\{name:string;amount:number;target:number;icon:string\};\nconst initial:Goal\[\]=\[[\s\S]*?\];",
        "type Goal={idCaixinha:number;name:string;amount:number;target:number;icon:string};\n"
        "const fromApiCashbox=(item:CashboxDto):Goal=>({idCaixinha:item.idCaixinha,name:item.nmCaixinha,amount:Number(item.vlAtual),target:Number(item.vlMeta),icon:'target'});",
        "Caixinhas.tsx: dados simulados",
    )
    source = source.replace("const [goals,setGoals]=useState(initial);", "const [goals,setGoals]=useState<Goal[]>([]);", 1)
    source = source.replace(
        "[chosenColor,setChosenColor]=useState('#5212d6');",
        "[chosenColor,setChosenColor]=useState('#5212d6'),[apiError,setApiError]=useState('');",
        1,
    )
    source = replace_once(
        source,
        r"useEffect\(\(\)=>\{const f=\(\)=>setZoom\(Math\.max\(1,window\.innerWidth/1440\)\);f\(\);window\.addEventListener\('resize',f\);return\(\)=>window\.removeEventListener\('resize',f\)\},\[\]\);",
        "useEffect(()=>{const f=()=>setZoom(Math.max(1,window.innerWidth/1440));f();window.addEventListener('resize',f);return()=>window.removeEventListener('resize',f)},[]);\n"
        "useEffect(()=>{let active=true;api.caixinhas.list().then(items=>{if(active)setGoals(items.map(fromApiCashbox))}).catch(error=>{if(active)setApiError(error instanceof Error?error.message:'Erro ao carregar caixinhas')});return()=>{active=false}},[]);",
        "Caixinhas.tsx: carregamento inicial",
    )
    source = replace_once(
        source,
        r"onSubmit=\{e=>\{e\.preventDefault\(\);const t=Number\(target\),v=Number\(start\)\|\|0;if\(!name\.trim\(\)\|\|t<=0\)return;setGoals\(old=>\[\.\.\.old,\{name:name\.trim\(\),target:t,amount:v,icon:chosenIcon\}\]\);setName\(''\);setTarget\(''\);setStart\(''\);setFormOpen\(false\)\}\}",
        "onSubmit={async e=>{e.preventDefault();const t=Number(target),v=Number(start)||0;if(!name.trim()||t<=0)return;try{const saved=await api.caixinhas.create({nome:name.trim(),meta:t,valorAtual:v});setGoals(old=>[...old,fromApiCashbox(saved)]);setName('');setTarget('');setStart('');setFormOpen(false);setApiError('')}catch(error){setApiError(error instanceof Error?error.message:'Não foi possível criar a caixinha')}}}",
        "Caixinhas.tsx: criação de caixinha",
    )
    source = source.replace("onClick={()=>navigate('/detalhes-caixinha')}", "onClick={()=>navigate('/detalhes-caixinha?id='+g.idCaixinha)}", 1)
    source = source.replace("{Math.floor(sum/total*100)}%", "{total>0?Math.floor(sum/total*100):0}%", 1)
    source = source.replace(
        "<p style={pos(253,138,580,25)} className=\"text-[#5c5791] text-[15px]\">Organize seus sonhos e acompanhe seu progresso.</p>",
        "<p style={pos(253,138,580,25)} className=\"text-[#5c5791] text-[15px]\">Organize seus sonhos e acompanhe seu progresso.</p>{apiError&&<p role=\"alert\" className=\"absolute left-[253px] top-[158px] text-[11px] text-red-600\">{apiError}</p>}",
        1,
    )
    source = replace_once(
        source,
        r"\n \{\[\n \['12/03/2025[\s\S]*?\]\.map\(\(row,i\)=>[\s\S]*?\)\}",
        "\n <p className=\"absolute left-[20px] top-[115px] text-[11px] text-[#5c5791]\">O histórico ficará disponível quando a API de movimentações for implementada.</p>",
        "Caixinhas.tsx: remover extrato fictício",
    )
    backup = path.with_suffix(path.suffix + ".bak")
    if not backup.exists(): backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    path.write_text(source, encoding="utf-8")


def patch_details(frontend: Path) -> None:
    path = frontend / "src/pages/DetalhesCaixinha.tsx"
    source = path.read_text(encoding="utf-8")
    source = source.replace(
        "import {GoalIcon} from '../components/GoalIcon';",
        "import {GoalIcon} from '../components/GoalIcon';\nimport {api, type CashboxDto} from '../services/valoraApi';",
        1,
    )
    source = replace_once(source, r"const seed:Movement\[\]=\[[\s\S]*?\];", "const seed:Movement[]=[];", "DetalhesCaixinha.tsx: extrato de exemplo")
    source = replace_once(
        source,
        r"const \[goalName,setGoalName\]=useState\('Carro'\),\[nameEditing,setNameEditing\]=useState\(false\),\[draftName,setDraftName\]=useState\('Carro'\),\[amount,setAmount\]=useState\(10000\),\[movements,setMovements\]=useState\(seed\),\[deposit,setDeposit\]=useState\(''\),\[withdraw,setWithdraw\]=useState\(''\),\[period,setPeriod\]=useState\('Últimos 6 meses'\),\[more,setMore\]=useState\(false\),\[deleted,setDeleted\]=useState\(false\);\nconst target=30000,pct=Math\.round\(amount/target\*100\);",
        "const cashboxId=Number(new URLSearchParams(window.location.search).get('id'));\n"
        "const [cashbox,setCashbox]=useState<CashboxDto|null>(null),[apiError,setApiError]=useState('');\n"
        "const [goalName,setGoalName]=useState(''),[nameEditing,setNameEditing]=useState(false),[draftName,setDraftName]=useState(''),[amount,setAmount]=useState(0),[movements]=useState(seed),[deposit,setDeposit]=useState(''),[withdraw,setWithdraw]=useState(''),[period,setPeriod]=useState('Últimos 6 meses'),[more,setMore]=useState(false),[deleted,setDeleted]=useState(false);\n"
        "useEffect(()=>{if(!cashboxId){setApiError('Abra uma caixinha pela lista para visualizar os detalhes.');return}let active=true;api.caixinhas.get(cashboxId).then(item=>{if(!active)return;setCashbox(item);setGoalName(item.nmCaixinha);setDraftName(item.nmCaixinha);setAmount(Number(item.vlAtual))}).catch(error=>{if(active)setApiError(error instanceof Error?error.message:'Não foi possível carregar a caixinha')});return()=>{active=false}},[cashboxId]);\n"
        "const target=Number(cashbox?.vlMeta??0),pct=target>0?Math.round(amount/target*100):0;",
        "DetalhesCaixinha.tsx: estado e carregamento da caixinha",
    )
    source = replace_once(
        source,
        r"function register\(kind:'Entrada'\|'Saída',raw:string\)\{[\s\S]*?(?=\nconst nav=)",
        "async function register(kind:'Entrada'|'Saída',raw:string){const v=Number(raw.replace(',','.'));if(!cashbox||!Number.isFinite(v)||v<=0)return;if(kind==='Saída'&&v>amount)return;const balance=amount+(kind==='Entrada'?v:-v);try{const updated=await api.caixinhas.update(cashbox.idCaixinha,{nome:goalName,meta:Number(cashbox.vlMeta),valorAtual:balance});setCashbox(updated);setAmount(Number(updated.vlAtual));setDeposit('');setWithdraw('');setApiError('')}catch(error){setApiError(error instanceof Error?error.message:'Não foi possível atualizar o saldo')}}\n"
        "async function saveGoalName(){if(!cashbox||!draftName.trim())return;try{const updated=await api.caixinhas.update(cashbox.idCaixinha,{nome:draftName.trim(),meta:Number(cashbox.vlMeta),valorAtual:amount});setCashbox(updated);setGoalName(updated.nmCaixinha);setNameEditing(false);setApiError('')}catch(error){setApiError(error instanceof Error?error.message:'Não foi possível atualizar a caixinha')}}",
        "DetalhesCaixinha.tsx: atualização do saldo e do nome",
    )
    source = source.replace("setGoalName(draftName.trim());setNameEditing(false)", "void saveGoalName()")
    source = source.replace("de R$ 30.000,00", "de {brl(target)}", 1)
    source = source.replace("Junte dinheiro para conquistar seu carro. &nbsp;🚗", "Acompanhe o andamento deste objetivo.", 1)
    source = source.replace("['Criada em','10/01/2025','calendar']", "['Criada em',cashbox?.dtCriacao?new Date(cashbox.dtCriacao).toLocaleDateString('pt-BR'):'—','calendar']", 1)
    source = source.replace(
        "onClick={()=>{if(window.confirm('Deseja excluir esta caixinha?')){setDeleted(true);navigate('/caixinhas')}}}",
        "onClick={()=>{if(window.confirm('Deseja excluir esta caixinha?')&&cashbox){api.caixinhas.remove(cashbox.idCaixinha).then(()=>{setDeleted(true);navigate('/caixinhas')}).catch(error=>setApiError(error instanceof Error?error.message:'Não foi possível excluir a caixinha'))}}}",
        1,
    )
    source = source.replace(
        "<p style={pos(270,176,580,25)} className=\"text-[#575294] text-[16px]\">Acompanhe o andamento deste objetivo.</p>",
        "<p style={pos(270,176,580,25)} className=\"text-[#575294] text-[16px]\">Acompanhe o andamento deste objetivo.</p>{apiError&&<p role=\"alert\" className=\"absolute left-[270px] top-[198px] text-[11px] text-red-600\">{apiError}</p>}",
        1,
    )
    source = source.replace(
        "{movements.map((m,i)=><div key={i} className=\"h-[36px] border-b border-[#e5e5f2] grid items-center px-[3px] text-[10px] text-[#575294]\" style={{gridTemplateColumns:'139px 199px 187px 91px 1fr'}}><span>{m.date}</span><span>{m.desc}</span><span>{m.kind==='Entrada'?'↑':'↓'} &nbsp;{m.kind}</span><b className={m.kind==='Entrada'?'text-[#059e54]':'text-[#f2141f]'}>{m.kind==='Entrada'?'+ ':'- '}{brl(m.value)}</b><span>{brl(m.balance)}</span></div>)}",
        "{movements.map((m,i)=><div key={i} className=\"h-[36px] border-b border-[#e5e5f2] grid items-center px-[3px] text-[10px] text-[#575294]\" style={{gridTemplateColumns:'139px 199px 187px 91px 1fr'}}><span>{m.date}</span><span>{m.desc}</span><span>{m.kind==='Entrada'?'↑':'↓'} &nbsp;{m.kind}</span><b className={m.kind==='Entrada'?'text-[#059e54]':'text-[#f2141f]'}>{m.kind==='Entrada'?'+ ':'- '}{brl(m.value)}</b><span>{brl(m.balance)}</span></div>)}{movements.length===0&&<p className=\"mt-8 text-center text-[11px] text-[#77718e]\">A API atualiza o saldo, mas ainda não armazena o histórico de depósitos e retiradas.</p>}",
        1,
    )
    backup = path.with_suffix(path.suffix + ".bak")
    if not backup.exists(): backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    path.write_text(source, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frontend", required=True, help="Pasta raiz do projeto React, contendo src/")
    args = parser.parse_args()
    frontend = Path(args.frontend).expanduser().resolve()
    if not (frontend / "src/pages/Categorias.tsx").exists() or not (frontend / "src/pages/Caixinhas.tsx").exists():
        raise SystemExit(f"Pasta React não reconhecida: {frontend}")
    patch_login(frontend)
    patch_categories(frontend)
    patch_cashboxes(frontend)
    patch_details(frontend)
    print("Login, Categorias, Caixinhas e DetalhesCaixinha atualizados. Backups .bak foram criados ao lado dos originais.")


if __name__ == "__main__":
    main()