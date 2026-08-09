@echo off
title App MTChart Pro Cloud
color 02
cls

echo =======================================================
echo          GESTAO DE PROCESSO: MTC app Cloud
echo =======================================================
echo [SISTEMA] Iniciando processos...

:: Navega ate o diretorio do projeto
cd /d "C:\Users\Merotec\Desktop\AppMTC_Cloud"

:: 2. Ativa o ambiente virtual e inicia o servidor Flet
if not exist .venv (
    color 0C
    echo [ERRO] Ambiente .venv nao encontrado em: %cd%
    echo [AVISO] criando ambiente .venv...
    python -m venv .venv
    echo [AVISO] Ambiente .venv criado em: %cd%	
    pause
    exit
)

echo [VENV] Ativando ambiente virtual...
call .venv\Scripts\activate

:: Mantém o terminal aberto e pronto para novos comandos
cmd /k