@echo off
chcp 65001 >nul
title Kokoro TTS Studio
color 0E
cls

echo ==========================================================
echo             ЗАПУСК KOKORO TTS STUDIO WEB GUI
echo ==========================================================
echo.

if not exist gui_venv (
    color 0C
    echo [ОШИБКА] Окружение "gui_venv" не найдено.
    echo Сначала запустите install_gui.bat
    pause
    exit
)

echo [SYSTEM] Активация окружения...
call gui_venv\Scripts\activate

echo [SYSTEM] Запуск интерфейса...
echo ----------------------------------------------------------
python gui.py

if %errorlevel% GTR 1 (
    color 0C
    echo.
    echo [CRITICAL] Приложение завершилась со сбоем.
    pause
) else (
    color 0A
    echo.
    echo [SYSTEM] Выход из приложения.
    timeout /t 3 >nul
)