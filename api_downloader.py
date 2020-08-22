import os
import pickle
import requests
import json
import re



start_low = 1    # 요청 시작 위치, 최신 다운로드 파일명에 따라 자동으로 변경.
LOAD_SIZE = 1000    # 요청 데이터 길이
SAVE_CYCLE = 5    # 저장 반복 주기

FILE_NAME = "product_{}.pickle"    # 저장 파일명 형식
FOLDER_NAME = "products"    # 파일 저장 폴더명
file_start_number = 1    # 파일 넘버링 시작 숫자, 최신 다운로드 파일명에 따라 변경.

URL_FMT = """......{}/{}"""    # API 데이터 요청 URL 형식, 형식에 맞게 수정.

# API Message 종류, 형식에 맞게 수정.
API_MESSAGE = {
    "INFO-000": "정상 처리되었습니다.",
    "ERROR-300": "필수 값이 누락되어 있습니다. 요청인자를 참고 하십시오.",
    "INFO-100": "인증키가 유효하지 않습니다. 인증키가 없는 경우, 홈페이지에서 인증키를 신청하십시오.",
    "ERROR-301": "파일타입 값이 누락 혹은 유효하지 않습니다. 요청인자 중 TYPE을 확인하십시오.",
    "ERROR-310": "해당하는 서비스를 찾을 수 없습니다. 요청인자 중 SERVICE를 확인하십시오.",
    "ERROR-331": "요청시작위치 값을 확인하십시오. 요청인자 중 START_INDEX를 확인하십시오.",
    "ERROR-332": "요청종료위치 값을 확인하십시오. 요청이자 중 END_INDEX값을 확인하십시오.",
    "ERROR-334": "종료위치보다 시작위치가 더 큽니다. 요청시작조회건수는 정수를 입력하세요.",
    "ERROR-336": "데이터요청은 한번에 최대 1000건을 넘을 수 없습니다.",
    "ERROR-500": "서버오류입니다.",
    "ERROR-601": "SQL 문장 오류입니다.",
    "INFO-200": "해당하는 데이터가 없습니다.",
    "INFO-300": "유효 호출건수를 이미 초과하셨습니다.",
    "INFO-400": "권한이 없습니다. 관리자에게 문의하십시오."
}



def default_setting():

    """프로그램 실행시 필요한 설정 모음 함수."""

    global file_start_number
    global start_low

    # 파일 디렉토리 설정.
    save_path = os.path.dirname(os.path.abspath(__file__))+'\\'+FOLDER_NAME
    if os.path.isdir(save_path):
        os.chdir(save_path)
    else:
        os.mkdir(save_path)
        os.chdir(save_path)

    # file_start_number 설정.
    numbering = [int(re.search(r'[0-9]+', file_name).group()) for file_name in os.listdir()]
    if len(numbering) != 0:
        file_start_number = max(numbering) + 1

    # start_low 설정.
    if file_start_number != 1:
        start_low = (file_start_number-1)*(LOAD_SIZE*SAVE_CYCLE)+1

def add_info(save_dict, product_dict):
    """제품을 정리하여 딕셔너리에 추가하는 함수"""
    product_name = product_dict['PRDLST_NM']
    product_number = product_dict['PRDLST_REPORT_NO']
    material_names = tuple(product_dict['RAWMTRL_NM'].split(','))
    company_name = product_dict['BSSH_NM']
    save_dict[product_number] = product_name, material_names, company_name

def save_and_clear(obj, file_name):
    """dict를 pickle 파일로 저장하고 비우는 함수"""
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    obj.clear()

def get_data(url_fmt, start_low, end_low):
    """API 서버에서 json 데이터를 dict로 변환하여 가져오는 함수. 가져오기에 실패했다면 None을 반환한다."""
    try:
        data = requests.get(url_fmt.format(start_low, end_low)).json()
        return data
    except json.decoder.JSONDecodeError:
        return None



# .py 파일이 직접적으로 실행될 때
if __name__ == '__main__':

    # 환경 설정 함수를 실행한다.
    default_setting()

    # 실행에 필요한 변수들을 선언한다.
    informations = {}    # 제품이 담길 딕셔너리
    counting = 0    # SAVE_CYCLE을 조회하기 위한 값
    
    # 다운로드를 반복한다.
    while True:

        # API 서버에서 데이터를 정상적으로 받아올 때까지 반복한다.
        while True:
            data = get_data(URL_FMT, start_low, start_low+LOAD_SIZE)
            if data != None:
                print("    Complite.")
                break
            else:
                print("    JSONDecodeError, retry...")
        
        # API의 메세지에 따라 분기하여 처리한다.
        message = data['C002']['RESULT']['CODE']
        if message != "INFO-000":    
            if message == 'INFO-200':    # 파일 저장이 모두 완료되었을 때
                print("All Complete. 종료.")
                break
            else:   # 기타 에러일 때
                print("MESSAGE: {}\n{}".format(message, API_MESSAGE[message]))
                break
        else:    # 정상적으로 불러왔을 때
            products = data['C002']['row']
            for pro_dict in products:
                add_info(informations, pro_dict)
        
        # API 조회 인덱스를 변경한다.
        start_low += LOAD_SIZE

        # SAVE_CYCLE에 따라 분할하여 딕셔너리를 저장한다.
        counting += 1
        if counting == SAVE_CYCLE:   
            save_and_clear(informations, FILE_NAME.format(file_start_number))
            print("    Create file '{}'.".format(FILE_NAME.format(file_start_number)))
            file_start_number += 1
            counting = 0
