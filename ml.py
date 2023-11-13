import pandas as pd
from urllib.parse import urlparse
import difflib

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

# 주소 비교 및 가장 유사한 주소 찾기
best_match = None
best_match_diff = None

for target_address in df['홈페이지 주소']:
    # 입력한 주소와 대상 주소 사이의 차이를 계산
    differ = difflib.Differ()
    diff = list(differ.compare(user_domain, target_address.lower()))

    # 불일치 부분 계산
    mismatch_count = len([s for s in diff if s.startswith('- ')])

    # 불일치 부분이 없는 경우 (완전히 일치)
    if mismatch_count == 0:
        best_match = target_address
        break

    # 현재까지 찾은 최적의 일치 주소 업데이트
    if best_match is None or mismatch_count < best_match_diff:
        best_match = target_address
        best_match_diff = mismatch_count

# 비교 결과 출력
if best_match:
    if mismatch_count == 0:
        print("실제로 있는 홈페이지입니다.")
    else:
        print(f"가장 비슷한 홈페이지: {best_match}")
        print(f"다른 부분: {''.join([s[2:] for s in diff if s.startswith('- ')])}")
        print("가짜 홈페이지입니다.")
else:
    print("입력한 주소와 일치하는 홈페이지가 없습니다.")
