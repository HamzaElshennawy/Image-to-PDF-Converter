@echo off
REM Batch wrapper for script.py (image -> PDF)
REM Use Windows py launcher to pick system Python; pass all args
py -3 "%~dp0script.py" %*