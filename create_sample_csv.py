import csv

def create_sample_csv():
    # 직원 정보 데이터
    employee_data = [
        ['사원번호', '이름', '부서', '입사일', '급여'],
        [1001, '김철수', '인사팀', '2020-01-15', 3500000],
        [1002, '이영희', '개발팀', '2018-03-22', 4200000],
        [1003, '박민수', '마케팅', '2021-05-10', 3800000],
        [1004, '최지은', '영업팀', '2019-11-05', 3900000],
        [1005, '정준호', '개발팀', '2022-02-28', 4000000]
    ]
    
    # 판매 데이터
    sales_data = [
        ['주문번호', '제품명', '가격', '판매량', '판매일'],
        ['S001', '노트북', 1200000, 3, '2023-01-15'],
        ['S002', '모니터', 350000, 5, '2023-01-20'],
        ['S003', '키보드', 55000, 10, '2023-02-05'],
        ['S004', '마우스', 35000, 15, '2023-02-10'],
        ['S005', '스피커', 80000, 8, '2023-03-15'],
        ['S006', '헤드폰', 120000, 12, '2023-03-22'],
        ['S007', '태블릿', 800000, 4, '2023-04-10'],
        ['S008', '프린터', 250000, 2, '2023-04-25']
    ]
    
    # 재고 정보
    inventory_data = [
        ['제품코드', '제품명', '카테고리', '공급업체', '현재고', '재주문수량'],
        ['P001', '노트북', '컴퓨터', '삼성전자', 15, 5],
        ['P002', '모니터', '주변기기', 'LG전자', 23, 10],
        ['P003', '키보드', '주변기기', '로지텍', 50, 20],
        ['P004', '마우스', '주변기기', '로지텍', 45, 20],
        ['P005', '스피커', '오디오', '보스', 12, 5],
        ['P006', '헤드폰', '오디오', '소니', 18, 8],
        ['P007', '태블릿', '모바일', '애플', 10, 5],
        ['P008', '프린터', '주변기기', 'HP', 5, 3]
    ]
    
    # 거래처 정보
    supplier_data = [
        ['업체번호', '업체명', '연락처', '담당자', '이메일', '주소'],
        ['V001', '삼성전자', '02-123-4567', '홍길동', 'samsung@example.com', '서울시 강남구'],
        ['V002', 'LG전자', '02-234-5678', '이순신', 'lg@example.com', '서울시 영등포구'],
        ['V003', '로지텍', '031-345-6789', '김유신', 'logitech@example.com', '경기도 성남시'],
        ['V004', '소니', '02-456-7890', '강감찬', 'sony@example.com', '서울시 강서구'],
        ['V005', '애플', '02-567-8901', '세종대왕', 'apple@example.com', '서울시 중구']
    ]
    
    # CSV 파일로 저장
    files = [
        ('employee_data.csv', employee_data),
        ('sales_data.csv', sales_data),
        ('inventory_data.csv', inventory_data),
        ('supplier_data.csv', supplier_data)
    ]
    
    for filename, data in files:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print(f"샘플 CSV 파일 '{filename}'이 생성되었습니다.")
    
    # 모든 데이터를 하나의 통합 파일로 저장
    with open('sample_data.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        
        # 직원 정보 섹션
        writer.writerow(['직원 정보'])
        writer.writerows(employee_data)
        writer.writerow([])  # 빈 줄 추가
        
        # 판매 데이터 섹션
        writer.writerow(['판매 데이터'])
        writer.writerows(sales_data)
        writer.writerow([])
        
        # 재고 정보 섹션
        writer.writerow(['재고 정보'])
        writer.writerows(inventory_data)
        writer.writerow([])
        
        # 거래처 정보 섹션
        writer.writerow(['거래처 정보'])
        writer.writerows(supplier_data)
    
    print("통합 샘플 CSV 파일 'sample_data.csv'가 생성되었습니다.")

if __name__ == "__main__":
    create_sample_csv() 