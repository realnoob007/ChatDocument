from flask import Flask, request, Response, stream_with_context, redirect, render_template
from model import chat_completions
import requests

app = Flask(__name__)


# 从请求头中提取token
def extract_token_from_headers():
    return request.headers.get('Authorization').split(' ')[1]

def extract_url_from_headers():
    data = request.get_json()
    document_url = data['messages'][0]['content']
    return document_url

@app.route('/v1/chat/completions', methods=['POST'])
def send_message():
    data = request.json
    model_name = data["model"]
    question = None
    for message in reversed(data['messages']):
        if message['role'] == 'user':
            question = message['content']
            break

    key = extract_token_from_headers().strip()
    document_url = extract_url_from_headers().strip()

    if model_name == "chatdocument":  # 添加自定义模型的名称

        response = Response(stream_with_context(chat_completions(key, question, document_url)), content_type='text/event-stream')
        return response
    else:
        return "模型不存在"

@app.route('/')
def upload_form():
    return render_template("upload.html")

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        response = upload_to_endpoint(file)
        return response.text

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'md', 'doc', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_endpoint(file):
    url = "https://rustypaste.shuttleapp.rs"
    files = {'file': (file.filename, file.read())}
    response = requests.post(url, files=files)
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)