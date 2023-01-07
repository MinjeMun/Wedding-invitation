import math
import datetime
from flask_pymongo import PyMongo
from flask import Flask, render_template, request, redirect
# request - 사용자로부터 받은 요청에 대한 정보를 가지고 옴
# redirect - 페이지 이동 (경로 변경)

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/local"
mongo = PyMongo(app)

@app.route('/write', methods=["POST"])
def write():
    name = request.form.get('name')
    content = request.form.get('content')

    mongo.db['wedding'].insert_one({ # 방명록 작성 - db 연결
        "name": name,
        "content": content
    })

    return redirect('/')

@app.route('/')
def index():
    now = datetime.datetime.now()
    wedding = datetime.datetime(2023, 12, 26, 0, 0, 0)
    diff = (wedding - now).days # 남은 일수

    page = int(request.args.get('page', 1)) # 사용자가 요청한 주소에 대한 값 가지고 옴(pagination)
    limit = 3
    skip = (page - 1) * limit

    count = mongo.db['wedding'].count_documents({}) # 데이터 개수 (빈 딕셔너리 변수 삽입)
    max_page = math.ceil(count / limit) # 필요한 최대 페이지 수
    pages = range(1, max_page+1) # 페이지 수 저장 변수

    guestbooks = mongo.db['wedding'].find().limit(3).skip(skip) # 방명록 목록 갖고오기

    return render_template(
        'index.html', 
        diff=diff, 
        guestbooks=guestbooks,
        pages = pages
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80') # host='0.0.0.0' - 모든 주소 접속 가능, port='80' 웹 사이트 기본 포트 번호