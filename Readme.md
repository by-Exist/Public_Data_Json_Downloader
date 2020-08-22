# 무엇인가요?
공공데이터포털에서 REST API 형식으로 제공되는 Json 형식의 문자열을 파이썬에서 다루기 위해 짠 코드입니다.

## [api_downloader.py](https://github.com/by-Exist/Public_Data_Json_Downloader/blob/master/api_downloader.py)
  공공데이터포털에서 REST 형식으로 전달받은 json 문자열을 dict로 가공하여 pickle파일로 저장합니다.
  파일의 최상단에 설정을 위한 변수들이 몰려있어, 사용자가 설정해야 하는 부분을 최소화하였습니다.
  
## [api_reader.py](https://github.com/by-Exist/Public_Data_Json_Downloader/blob/master/api_reader.py)
  저장한 pickle파일들을 일괄적으로 불러와 데이터를 수정 및 가공할 수 있게 하나의 객체로 묶습니다.
  해당 객체를 바탕으로 데이터를 DB에 삽입하고, 가공하고, 삭제할 수 있습니다.


코드에 주석을 상세하게 달아놓았기에 코드를 보면서 이해할 수 있습니다.
