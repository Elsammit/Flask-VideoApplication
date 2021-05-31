#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, url_for, request, redirect
from camera import Camera
import cv2
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['mp4', 'wmv', 'avi', 'gif'])
UPLOAD_FOLDER = './uploads'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

#動画表示html
@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#動画データ送信
@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#動画開始
@app.route('/start', methods=["POST"])
def start_movie():
    print("start")
    Camera.rewindFlg = False
    Camera.stop = False
    Camera.speed = 0
    return Response("OK", 200)

#動画一時停止
@app.route('/pause', methods=["POST"])
def pause_movie():
    print("pause")
    Camera.stop = True
    return Response("OK", 200)

#動画停止
@app.route('/stop', methods=["POST"])
def stop_movie():
    print("stop")
    Camera.cap = cv2.VideoCapture(Camera.MoviePath)
    Camera.stop = False
    video_feed()

#早送りスピード調整
@app.route('/speed', methods=["POST"])
def changeSpeed():
    if Camera.rewindFlg == True:
        Camera.speed = 1
        Camera.rewindFlg = False
    else:
        Camera.speed = Camera.speed % 3 + 1
    Camera.stop = False
    print("speed:"+str(Camera.speed))
    return Response("OK", 200)

#巻き戻し
@app.route('/rewind', methods=["POST"])
def rewind_movie():
    if Camera.rewindFlg == False:
        Camera.speed = 1
        Camera.rewindFlg = True
    else:
        Camera.speed = Camera.speed % 3 + 1
    Camera.stop = False
    print("rewind:"+str(Camera.rewindFlg))
    return Response("OK", 200)

#動画進捗状況送信
@app.route('/progress', methods=["POST"])
def get_progress():
    return Response(str(Camera.progress), 200)

#動画取得
@app.route('/test', methods=["POST"])
def get_test():
     # ファイルがなかった場合の処理
    if 'file' not in request.files:
        print('ファイルがありません')
        return redirect('/')
    # データの取り出し
    file = request.files['file']
    # ファイル名がなかった時の処理
    if file.filename == '':
        print('ファイルがありません')
        return redirect("/")
    if file and allwed_file(file.filename):
        # 危険な文字を削除（サニタイズ処理）
        filename = secure_filename(file.filename)
        #filename = file.filename
        Camera.MoviePath = filename
        # ファイルの保存
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        Camera.cap = cv2.VideoCapture(Camera.MoviePath)
        # アップロード後のページに転送
        return redirect("/")
    else:
        print("not movie file")
        return redirect("/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
