import pandas as pd
import numpy as np

# 샘플 데이터 생성
def create_sample_excel():
    # 첫 번째 시트 - 직원 정보
    employee_data = {
        '사원번호': [1001, 1002, 1003, 1004, 1005],
        '이름': ['김철수', '이영희', '박민수', '최지은', '정준호'],
        '부서': ['인사팀', '개발팀', '마케팅', '영업팀', '개발팀'],
        '입사일': ['2020-01-15', '2018-03-22', '2021-05-10', '2019-11-05', '2022-02-28'],
        '급여': [3500000, 4200000, 3800000, 3900000, 4000000]
    }
    df_employee = pd.DataFrame(employee_data)
    
    # 두 번째 시트 - 판매 데이터
    sales_data = {
        '주문번호': ['S001', 'S002', 'S003', 'S004', 'S005', 'S006', 'S007', 'S008'],
        '제품명': ['노트북', '모니터', '키보드', '마우스', '스피커', '헤드폰', '태블릿', '프린터'],
        '가격': [1200000, 350000, 55000, 35000, 80000, 120000, 800000, 250000],
        '판매량': [3, 5, 10, 15, 8, 12, 4, 2],
        '판매일': ['2023-01-15', '2023-01-20', '2023-02-05', '2023-02-10', '2023-03-15', '2023-03-22', '2023-04-10', '2023-04-25']
    }
    df_sales = pd.DataFrame(sales_data)
    
    # 세 번째 시트 - 재고 정보
    inventory_data = {
        '제품코드': ['P001', 'P002', 'P003', 'P004', 'P005', 'P006', 'P007', 'P008'],
        '제품명': ['노트북', '모니터', '키보드', '마우스', '스피커', '헤드폰', '태블릿', '프린터'],
        '카테고리': ['컴퓨터', '주변기기', '주변기기', '주변기기', '오디오', '오디오', '모바일', '주변기기'],
        '공급업체': ['삼성전자', 'LG전자', '로지텍', '로지텍', '보스', '소니', '애플', 'HP'],
        '현재고': [15, 23, 50, 45, 12, 18, 10, 5],
        '재주문수량': [5, 10, 20, 20, 5, 8, 5, 3]
    }
    df_inventory = pd.DataFrame(inventory_data)
    
    # 네 번째 시트 - 거래처 정보
    supplier_data = {
        '업체번호': ['V001', 'V002', 'V003', 'V004', 'V005'],
        '업체명': ['삼성전자', 'LG전자', '로지텍', '소니', '애플'],
        '연락처': ['02-123-4567', '02-234-5678', '031-345-6789', '02-456-7890', '02-567-8901'],
        '담당자': ['홍길동', '이순신', '김유신', '강감찬', '세종대왕'],
        '이메일': ['samsung@example.com', 'lg@example.com', 'logitech@example.com', 'sony@example.com', 'apple@example.com'],
        '주소': ['서울시 강남구', '서울시 영등포구', '경기도 성남시', '서울시 강서구', '서울시 중구']
    }
    df_supplier = pd.DataFrame(supplier_data)
    
    # 엑셀 파일로 저장
    with pd.ExcelWriter('sample_data.xlsx') as writer:
        df_employee.to_excel(writer, sheet_name='직원정보', index=False)
        df_sales.to_excel(writer, sheet_name='판매데이터', index=False)
        df_inventory.to_excel(writer, sheet_name='재고정보', index=False)
        df_supplier.to_excel(writer, sheet_name='거래처정보', index=False)
    
    print("샘플 엑셀 파일 'sample_data.xlsx'가 생성되었습니다.")

if __name__ == "__main__":
    create_sample_excel() 