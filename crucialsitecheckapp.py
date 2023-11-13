from flask import Flask, request, jsonify
from urllib.parse import urlparse
import difflib
import pandas as pd

app = Flask(__name__)

# CSV 파일에서 데이터 읽기
file_path = 'data.csv'
df = pd.read_csv(file_path)

@app.route('/compare_address', methods=['POST'])
def compare_address():
    try:
        # 클라이언트에서 주소 입력 받기
        user_input_address = request.json['user_input_address']

        # 입력한 주소를 파싱하여 도메인 추출
        user_domain = urlparse(user_input_address).netloc.lower()

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

        # 비교 결과 반환
        if best_match:
            if mismatch_count == 0:
                return jsonify({"result": "실제로 있는 홈페이지입니다."})
            else:
                response = {
                    "result": "가짜 홈페이지입니다.",
                    "best_match": best_match,
                    "mismatched_part": ''.join([s[2:] for s in diff if s.startswith('- ')])
                }
                return jsonify(response)
        else:
            return jsonify({"result": "입력한 주소와 일치하는 홈페이지가 없습니다."})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
