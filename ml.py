import pandas as pd
from urllib.parse import urlparse

# CSV 파일에서 데이터 읽기
# 예시 CSV 파일 형태: "사이트 이름", "홈페이지 주소"
# example.com, https://www.example.com
# example2.com, https://www.example2.com
file_path = 'data.csv'
df = pd.read_csv(file_path)

# 사용자로부터 주소 입력 받기
user_input_address = input("홈페이지 주소를 입력하세요 (예: https://www.kipf.re.kr/):")

# 입력한 주소를 파싱하여 도메인 추출
user_domain = urlparse(user_input_address).netloc.lower()  # 도메인 비교 시 대소문자 구분 없이 비교

# 사용자 입력 주소 확인
print(f"사용자 입력 주소: {user_input_address}")

# CSV 파일의 각 주소를 파싱하여 도메인 추출하고, 도메인만을 비교하여 일치 여부 확인
matching = False
for target_address in df['홈페이지 주소']:
    target_domain = urlparse(target_address).netloc.lower()  # 도메인 비교 시 대소문자 구분 없이 비교
    if user_domain == target_domain:
        matching = True
        break

# CSV 파일 주소 확인
#print(f"CSV 파일 주소 목록:")
#for target_address in df['홈페이지 주소']:
#   print(target_address)

# 결과 출력
if matching:
    print("실제로 있는 홈페이지입니다.")
else:
    print("가짜 홈페이지입니다.")