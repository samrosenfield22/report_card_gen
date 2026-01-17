@ECHO OFF

RD /S /Q "dist"

set PROG=report_card_gen
pyinstaller --clean --onefile --windowed %PROG%.py

copy "credentials.json" "dist/credentials.json"
copy "token.json" "dist/token.json"

XCOPY "docs" "dist/docs" /E /I /H /Y
XCOPY "user" "dist/user" /E /I /H /Y

DEL %PROG%.spec
DEL "dist\user\email_address.txt"
DEL "dist\user\app_password.txt"
RD /S /Q "build"
