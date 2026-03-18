@echo off

:: Diretório onde o .bat está
set BASE_DIR=%~dp0

:: Verifica se a pasta venv existe
if not exist "%BASE_DIR%\venv" (
    echo Criando ambiente virtual...
    python -m venv "%BASE_DIR%\venv"
)

:: Ativar o ambiente virtual
call "%BASE_DIR%\venv\Scripts\activate.bat"

:: Atualizar pip (opcional)
python -m pip install --upgrade pip

:: Se existir requirements.txt, instalar dependências
if exist "%BASE_DIR%\requirements.txt" (
    echo Instalando dependencias...
    pip install -r "%BASE_DIR%\requirements.txt"
)

:: Executar o script Python
::python "%BASE_DIR%\main.py"

:: Manter a janela aberta após a execução
pause
