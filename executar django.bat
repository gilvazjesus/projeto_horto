@echo off

:: Diretório onde o .bat está
set BASE_DIR=%~dp0

:: Ativar o ambiente virtual
call "%BASE_DIR%\venv\Scripts\activate.bat"

:: Ir para o diretório do projeto
cd /d "%BASE_DIR%\projeto_horto"

:: Rodar o servidor Django
python manage.py runserver

:: Manter a janela aberta após execução
pause