@echo off
REM ============================================================
REM create_configs.bat
REM Creates three config files in the project root (the folder
REM where this script is located):
REM   db_config.toml, test_db_config.toml, server_security.toml
REM Existing files are NOT overwritten: delete a file if you
REM want to regenerate it.
REM ============================================================

setlocal

REM Project root = folder containing this script (trailing backslash included)
set "PROJECT_ROOT=%~dp0"

REM ---------- db_config.toml ----------
if exist "%PROJECT_ROOT%db_config.toml" (
    echo SKIP: db_config.toml already exists
) else (
    > "%PROJECT_ROOT%db_config.toml" (
        echo [mysql]
        echo host = 'your host here'
        echo port = 'your port here'
        echo database = 'database_name_here'
        echo driver = 'mysql+pymysql'
    )
    echo OK: created db_config.toml
)

REM ---------- test_db_config.toml (same parameters as db_config.toml) ----------
if exist "%PROJECT_ROOT%test_db_config.toml" (
    echo SKIP: test_db_config.toml already exists
) else (
    > "%PROJECT_ROOT%test_db_config.toml" (
        echo [mysql]
        echo host = 'your host here'
        echo port = 'your port here'
        echo database = 'database_name_here'
        echo driver = 'mysql+pymysql'
    )
    echo OK: created test_db_config.toml
)

REM ---------- server_security.toml ----------
if exist "%PROJECT_ROOT%server_security.toml" (
    echo SKIP: server_security.toml already exists
) else (
    > "%PROJECT_ROOT%server_security.toml" (
        echo [mysql]
        echo user = 'your db username'
        echo password = 'db password'
    )
    echo OK: created server_security.toml
)

endlocal
