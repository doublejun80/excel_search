import os
import sys
import shutil
from pathlib import Path

# 파일 이름 및 경로
script_name = "csv_search_app.py"  # 검색 도구 파이썬 파일 이름
icon_file = None  # 아이콘 파일 (있는 경우)
output_name = "CSV검색도구"  # EXE 파일 이름

# 메인 디렉토리 생성
dist_dir = Path("배포용")
if dist_dir.exists():
    shutil.rmtree(dist_dir)
dist_dir.mkdir()

# 배포 명령 구성
cmd = f'pyinstaller --noconfirm --onefile --windowed --clean --name "{output_name}"'

# 아이콘 추가 (있는 경우)
if icon_file and os.path.exists(icon_file):
    cmd += f' --icon="{icon_file}"'

# 파이썬 스크립트 추가
cmd += f' "{script_name}"'

# PyInstaller 실행
print("실행 파일 생성 중...")
os.system(cmd)

# 생성된 파일 이동
exe_path = Path("dist") / f"{output_name}.exe"
if exe_path.exists():
    shutil.copy(exe_path, dist_dir)
    print(f"실행 파일이 '{dist_dir / exe_path.name}' 경로에 생성되었습니다.")
else:
    print("실행 파일 생성에 실패했습니다.")
    sys.exit(1)

# 사용설명서 생성
readme_text = """# CSV 검색 도구 사용 설명서

이 프로그램은 CSV 파일에서 특정 단어를 검색하고 선택한 열의 정보를 표시하는 도구입니다.

## 사용 방법

1. **파일 선택**:
   - "파일 선택" 버튼을 클릭해 CSV 파일을 선택합니다.
   - 인코딩 문제가 있으면 드롭다운에서 다른 인코딩(cp949, utf-8 등)을 선택하고 "적용" 버튼을 클릭합니다.

2. **검색어 입력**:
   - "검색" 영역에 찾고자 하는 단어나 문구를 입력합니다.

3. **출력할 열 선택**:
   - 왼쪽 패널의 체크박스로 결과에 표시할 열을 선택합니다.
   - "전체 선택/해제" 체크박스로 모든 열을 한 번에 선택하거나 해제할 수 있습니다.

4. **검색 실행**:
   - "검색" 버튼을 클릭하거나 Enter 키를 누릅니다.
   - 검색 결과가 오른쪽 패널에 표시됩니다.

5. **결과 탐색**:
   - 열이 많은 경우 "◀ 왼쪽" / "오른쪽 ▶" 버튼이나 좌우 방향키로 이동할 수 있습니다.
   - 모든 검색 결과는 자동으로 클립보드에 복사됩니다.

6. **결과 복사**:
   - "클립보드에 복사" 버튼을 클릭하거나 Ctrl+C를 눌러 결과를 다시 복사할 수 있습니다.
   - 복사된 결과는 엑셀에 바로 붙여넣기(Ctrl+V) 할 수 있습니다.

## 참고 사항

- 검색은 대소문자를 구분하지 않습니다.
- 결과는 자동으로 클립보드에 복사되니 바로 엑셀에 붙여넣기 할 수 있습니다.
- 한글 파일은 기본적으로 cp949 인코딩을 사용하지만, 문제가 있을 경우 다른 인코딩을 시도해보세요.
"""

readme_path = dist_dir / "사용설명서.txt"
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(readme_text)
print(f"사용설명서가 '{readme_path}' 경로에 생성되었습니다.")

print("\n배포 패키지 준비가 완료되었습니다!")
print(f"'{dist_dir}' 폴더를 압축하여 배포하세요.")
