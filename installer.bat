@ECHO OFF
pyinstaller --clean --distpath . --onefile --windowed report_card_gen.py

DEL report_card_gen.spec
RD /S /Q "build"
