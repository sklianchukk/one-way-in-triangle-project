@echo off
chcp 65001 >nul
title Projekt: Miasta i Drogi

if not exist in mkdir in
if not exist out mkdir out
if not exist backup mkdir backup

:menu
cls
echo ======================================================
echo           PROJEKT: MIASTA I DROGI (JS)
echo ======================================================
echo 1. Uruchom program (obliczenia)
echo 2. Wyjdź
echo ======================================================
set /p choice="Wybierz opcję (1-2): "

if "%choice%"=="2" exit
if "%choice%"=="1" goto :run
goto :menu

:run
cls
echo [WEJŚCIE]
set /p m_val="Podaj liczbę miast m (m > 2): "
echo %m_val% > in\input.txt

echo.
echo [INFO] Uruchamianie skryptu Python...
echo [INFO] Proszę czekać, trwają obliczenia...

python script.py

if %errorlevel% equ 0 (
    echo.
    echo [SUKCES] Obliczenia zakończone pomyślnie.
    echo [SUKCES] Raport został wygenerowany w /backup/ i otwarty.
) else (
    echo.
    echo [BŁĄD] Wystąpił problem w skrypcie Python.
    echo [BŁĄD] Sprawdź poprawność danych wejściowych.
)

echo.
pause
goto :menu