from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

# .env 파일 로드
load_dotenv()

# 환경 변수에서 값 가져오기
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# 뉴스 검색 함수
def get_news(query, display=10, start=1):
    url = 'https://openapi.naver.com/v1/search/news.json'
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    params = {
        'query': query,
        'display': display,
        'start': start,
        'sort': 'date'
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# 메인 페이지 라우팅
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form['query']  # 사용자가 입력한 키워드 받기
        news_data = get_news(query)
        return render_template('index.html', news_data=news_data['items'], query=query)
    return render_template('index.html', news_data=None, query='')

if __name__ == '__main__':
    app.run(debug=True)
