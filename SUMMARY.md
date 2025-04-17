# CSV/엑셀 검색 도구 프로젝트 요약

## 개발 완료 항목

1. CSV 파일 검색 도구 (`csv_search.py`)
   - 표준 라이브러리만 사용
   - 파일 선택 기능
   - 키워드 검색 기능
   - 결과 표시 기능 (Treeview)
   - 오류 처리

2. 엑셀 파일 검색 도구 버전 (`excel_search.py`, `excel_search_lite.py`)
   - pandas 사용 버전
   - openpyxl 사용 버전

3. 샘플 데이터 생성 도구
   - CSV 샘플 파일 생성 (`create_sample_csv.py`)
   - 엑셀 샘플 파일 생성 (`create_sample_excel.py`, `create_sample_excel_lite.py`)

4. 문서화
   - README.md 파일 작성 (사용 방법 등)
   - 코드 주석 추가

5. 배포 도구
   - PyInstaller 실행 파일 생성 스크립트 (`build_exe.bat`)

## 사용 방법

1. 기본 실행:
   ```
   python csv_search.py
   ```

2. 샘플 데이터 생성:
   ```
   python create_sample_csv.py
   ```

3. 실행 파일 생성:
   ```
   build_exe.bat
   ```

## 파일 구조

- `csv_search.py`: 메인 CSV 검색 애플리케이션
- `excel_search.py`: pandas 기반 엑셀 검색 애플리케이션
- `excel_search_lite.py`: openpyxl 기반 엑셀 검색 애플리케이션
- `create_sample_csv.py`: 샘플 CSV 파일 생성기
- `create_sample_excel.py`: pandas 기반 샘플 엑셀 파일 생성기
- `create_sample_excel_lite.py`: openpyxl 기반 샘플 엑셀 파일 생성기
- `requirements.txt`: 필요한 라이브러리 목록
- `README.md`: 사용자 가이드
- `build_exe.bat`: 실행 파일 생성 스크립트
- 샘플 파일:
  - `employee_data.csv`, `sales_data.csv`, `inventory_data.csv`, `supplier_data.csv`
  - `sample_data.csv`: 통합 샘플 파일

## 추가 개선 가능 사항

1. 검색 옵션 확장 (대소문자 구분, 정규식 등)
2. 결과 내보내기 기능 (CSV, 엑셀 등)
3. UI 디자인 개선
4. 다국어 지원
5. 동시에 여러 파일 검색 기능
6. 진행 상황 표시 막대 추가 