from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def check_virustotal(image_url, virustotal_api_key):
    virustotal_url = "https://www.virustotal.com/vtapi/v2/url/report"
    params = {
        'apikey': virustotal_api_key,
        'resource': image_url
    }
    response = requests.get(virustotal_url, params=params)
    if response.status_code == 200:
        result = response.json()
        positives = result.get('positives', 0)
        
        # positives 값에 따라 상태 설정
        if positives >= 10:
            result['status'] = 'danger'
        elif positives >= 1:
            result['status'] = 'strange'
        else:
            result['status'] = 'safe'
            
        return result
    else:
        return {"error": "Virustotal과의 연결에 문제가 있습니다."}

@app.route('/check_url', methods=['POST'])
def check_url():
    data = request.json
    image_url = data.get("url")
    api_key = 'YOUR_VIRUSTOTAL_API_KEY'
    
    if image_url:
        result = check_virustotal(image_url, api_key)
        return jsonify(result)
    else:
        return jsonify({"error": "URL을 받지 못했습니다."})

if __name__ == '__main__':
    app.run(debug=True)
