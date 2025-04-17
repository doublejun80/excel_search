@echo off
echo CSV/엑셀 검색 도구 실행 파일 생성

REM PyInstaller 설치 확인 및 설치
echo PyInstaller 설치 확인 중...
pip show pyinstaller
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller를 설치합니다...
    pip install pyinstaller
)

REM CSV 검색 도구 실행 파일 생성
echo CSV 검색 도구 실행 파일을 생성합니다...
pyinstaller --onefile --windowed --name csv_search csv_search.py

echo 실행 파일 생성이 완료되었습니다.
echo 생성된 파일은 dist 폴더에 있습니다.
pause 