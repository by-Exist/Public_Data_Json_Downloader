import os
import pickle
import csv
import json
from api_downloader import FOLDER_NAME
from collections import ChainMap, namedtuple

# pickle이 모여있는 폴더로 프로그램 실행 경로를 이동
os.chdir(os.path.dirname(os.path.abspath(__file__))+'\\'+FOLDER_NAME)

# 폴더 내의 pickle 파일 이름들을 불러오기
file_names = [file_name for file_name in os.listdir()]

# 파일들을 하나하나 다시 딕셔너리로 복원하고서 information에 딕셔너리를 모으기
information = []
for file_name in file_names:
    with open(file_name, 'rb') as f:
        info = pickle.load(f)
        information.append(info)

# 모든 딕셔너리들을 마치 하나처럼 활용할 수 있도록 기능을 제공하는 'ChainMap' 활용
information = ChainMap(*information)

# namedtuple은 (클래스명, "속성a 속성b 속성c 속성d") 형태로 생성할 수 있으며
# 해당 클래스로 생성한 객체는 생성할 때 속성값 a, b, c, d를 전달해야 하며
# 생성한 객체는 객체.속성a, 객체.속성b...의 형태로 접근 가능
Product = namedtuple('Product', '제조사 제품명 바코드번호 품목제조번호 재료')

# csv파일과 딕셔너리에 저장된 데이터를 합쳐 하나의 제품으로 완성하여 담을 리스트 생성
products = []

# csv파일을 열어 한줄한줄 읽을 때마다, 품목제조번호로 딕셔너리를 조사하고
# 데이터가 있을 경우에는 (회사명, 제품명, 바코드, 품목제조번호, 재료)의 형태로 가공
# 데이터가 없을 경우에는 (회사명, 제품명, 바코드, 품목제조번호, None)의 형태로 가공
count = 0
with open('../barcorddata.csv', 'r') as f:

    csv = csv.reader(f)

    # 첫 컬럼명 라인 버리기
    next(csv)

    for product_info in csv:
        if value := information.get(product_info[3]):
            count += 1
            products.append(
                # 1. 원본
                Product(*product_info, value[1])
                # # 2. json으로 저장하기 위해 임시로 작성한 코드
                # {
                #     '제조사':product_info[0],
                #     '제품명':product_info[1],
                #     '바코드번호':product_info[2],
                #     '품목제조번호':product_info[3]
                # }
            )
        else:
            products.append(
                # Product(*product_info, None)
            )

print(count)

# 생성된 제품들을 DB에 기록하는 과정.
for product in products:
    """
    쿼리문을 만들어놓고
        '''INSERT INTO product (company, name, barcode, product_number, material) VALUES (?, ?, ?, ?, ?)'''
    데이터를 집어넣어서
        (product.company, product.name, product.barcode, product.number, product.material)

    위와 같은 형태로 DB에 데이터를 전송할 수 있다.
    """
    print(product)

# # csv파일을 json으로 변환하는 과정
# with open('convert_json.json', 'w', encoding='utf-8') as f:
#     json.dump(products, f, ensure_ascii=False, indent=4)
