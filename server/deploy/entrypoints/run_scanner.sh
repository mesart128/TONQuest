#!/bin/sh
echo "Starting scanner..."
ls -l scanner_runner.py  # Проверка наличия файла
python --version  # Проверка версии Python
python scanner_runner.py
echo "Scanner script finished"