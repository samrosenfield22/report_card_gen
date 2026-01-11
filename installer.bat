@ECHO OFF
set PROG=report_card_gen
pyinstaller --clean --onefile --windowed %PROG%.py

copy "credentials.json" "dist/credentials.json"
DEL %PROG%.spec
RD /S /Q "build"
