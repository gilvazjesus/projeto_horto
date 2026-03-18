@echo off

:: Diretório onde o .bat está
set BASE_DIR=%~dp0

:: Ativar o ambiente virtual
call "%BASE_DIR%\venv\Scripts\activate.bat"

:: Executar o script Python
python "%BASE_DIR%\main.py"

:: Manter a janela aberta após a execução
pause
