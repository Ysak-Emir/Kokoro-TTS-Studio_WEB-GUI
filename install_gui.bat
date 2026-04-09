@echo off
chcp 65001 >nul
title Kokoro GUI: Smart Installer
color 0B
cls

echo =========================================================
echo          KOKORO TTS WEB GUI: МАСТЕР УСТАНОВКИ
echo =========================================================
echo.

:: 1. Проверка: не установлено ли уже всё?
if exist gui_venv (
    color 0E
    echo [ИНФО] Виртуальное окружение уже создано.
    echo.
    set /p choice="Вы хотите переустановить библиотеки (y/n)? "
    if /i "%choice%"=="n" (
        cls
        color 0A
        echo ======================================================
        echo   ОТМЕНА: У вас уже все установлено.
        echo   Просто запустите run_gui.bat
        echo ======================================================
        pause
        exit
    )
    echo [SYSTEM] Начинаю обновление/переустановку...
)

:: 2. Проверка наличия Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [КРИТИЧЕСКАЯ ОШИБКА] Python не найден в системе!
    echo Пожалуйста, установите Python и поставьте галочку "Add to PATH".
    pause
    exit
)

:: 3. Создание виртуального окружения (если нет)
if not exist gui_venv (
    echo [1/2] Шаг 1: Создание окружения "gui_venv"...
    python -m venv gui_venv
) else (
    echo [1/2] Шаг 1: Окружение уже есть, пропускаю создание...
)

:: 4. Активация и установка
echo [2/2] Шаг 2: Установка зависимостей из requirements.txt...
echo ------------------------------------------------------
call studio_venv\Scripts\activate

:: Проверяем, есть ли файл требований
if not exist requirements.txt (
    color 0C
    echo [ОШИБКА] Файл requirements.txt не найден!
    pause
    exit
)

python -m pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [ОШИБКА] Что-то пошло не так при загрузке библиотек.
    echo Проверьте интернет-соединение.
    pause
    exit
)

cls
color 0A
echo ======================================================
echo   УСПЕШНО: Установка завершена!
echo   Теперь вы можете закрыть это окно и запустить
echo   проект через run_gui.bat
echo ======================================================
pause