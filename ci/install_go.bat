@echo off
setlocal enabledelayedexpansion

REM Define the Go version you want to install
set "GO_VERSION=1.18.2"

REM Define the installation directory
set "INSTALL_DIR=C:\Go"

REM Define the Go binary URL
set "GO_URL=https://golang.org/dl/go%GO_VERSION%.windows-amd64.msi"

REM Create a temporary directory for downloads
set "TEMP_DIR=%TEMP%\golang_installer"
mkdir "%TEMP_DIR%"

REM Download the Go MSI installer
echo Downloading Go %GO_VERSION%...
curl -L -o "%TEMP_DIR%\go.msi" "%GO_URL%"

REM Install Go
echo Installing Go %GO_VERSION% to %INSTALL_DIR%...
msiexec /i "%TEMP_DIR%\go.msi" /qn /log "%TEMP_DIR%\go_install.log" TARGETDIR="%INSTALL_DIR%"

REM Add Go binary directory to PATH
set "NEW_PATH=%INSTALL_DIR%\bin;%PATH%"
setx PATH "!NEW_PATH!" /M

REM Clean up temporary files
rmdir /s /q "%TEMP_DIR%"

echo Go %GO_VERSION% is installed.
echo Please open a new command prompt to use Go.

go version