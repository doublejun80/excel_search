# CSV/엑셀 검색 도구

CSV 파일이나 엑셀 파일 내부에서 특정 키워드를 검색하고 결과를 표시하는 도구입니다.

## 기능

- CSV 파일 선택 및 로드
- 키워드 검색
- 행, 열, 값을 포함한 검색 결과 표시
- 사용자 친화적인 인터페이스
- 상태 메시지로 검색 진행 상황 표시

## 파일 설명

- `csv_search.py`: CSV 파일 검색 도구 (기본 라이브러리만 사용)
- `excel_search.py`: 엑셀 파일 검색 도구 (pandas와 openpyxl 필요)
- `excel_search_lite.py`: 엑셀 파일 검색 도구 (openpyxl만 사용)
- `create_sample_csv.py`: 샘플 CSV 파일 생성 도구
- `create_sample_excel.py`: 샘플 엑셀 파일 생성 도구 (pandas 필요)
- `create_sample_excel_lite.py`: 샘플 엑셀 파일 생성 도구 (openpyxl만 사용)

## 설치 방법

### 소스 코드에서 실행

1. Python 3.8 이상이 설치되어 있어야 합니다.
2. CSV 검색 도구는 외부 라이브러리 없이 바로 실행 가능합니다:
   ```
   python csv_search.py
   ```
3. 엑셀 검색 도구를 사용하려면 필요한 라이브러리를 설치해야 합니다:
   ```
   pip install pandas openpyxl
   python excel_search.py
   ```

## 사용 방법

1. "파일 선택" 버튼을 클릭하여 검색할 CSV 파일을 선택합니다.
2. "검색어" 입력 필드에 찾고자 하는 키워드를 입력합니다.
3. "검색" 버튼을 클릭하여 검색을 시작합니다.
4. 검색 결과가 표 형태로 표시됩니다. 결과에는 행 번호, 열 이름, 셀 값이 포함됩니다.
5. 상태 표시줄에서 검색 진행 상황을 확인할 수 있습니다.

## 샘플 데이터

테스트를 위한 샘플 CSV 파일을 생성하려면:

```
python create_sample_csv.py
```

이 명령을 실행하면 여러 CSV 파일과 하나의 통합 파일이 생성됩니다.

## 주의사항

- 매우 큰 파일을 검색할 경우 시간이 오래 걸릴 수 있습니다.
- 현재 검색은 대소문자를 구분하지 않습니다. 