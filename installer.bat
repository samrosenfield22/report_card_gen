@ECHO OFF
set PROG=report_card_gen
pyinstaller --clean --distpath . --onefile --windowed %PROG%.py

DEL %PROG%.spec
RD /S /Q "build"
