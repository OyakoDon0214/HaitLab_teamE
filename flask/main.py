import os
from flask import Flask, request, redirect, url_for,render_template,flash
from werkzeug.utils import secure_filename
from flask import send_from_directory
from PIL import Image
from ConvertReceipt import ConvertReceipt

UPLOAD_FOLDER = './uploads'
# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['png', 'jpg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ファイルを受け取る方法の指定
@app.route('/', methods=['GET', 'POST'])
def uploads_file():
    # リクエストがポストかどうかの判別
    if request.method == 'POST':
        file = request.files['file']
        # ファイルのチェック
        if file and allwed_file(file.filename):
            # 危険な文字を削除（サニタイズ処理）
            filename = secure_filename(file.filename)
            # ファイルの保存
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image=Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            r=ConvertReceipt.ConvertReceipt(image)
            dict=r.convert()
            shop=dict["shop"]

            # アップロード後のページに転送
            return render_template('result.html')
    elif request.method == 'GET':        
        return '''
        <!doctype html>
        <html>
            <head>
                <meta charset="UTF-8">
                <title>
                    ファイルをアップロード
                </title>
            </head>
            <body>
                <h1>
                    ファイルをアップロード
                </h1>
                <form method = post enctype = multipart/form-data>
                <p><input type=file name = file>
                <input type = submit value = Upload>
                </form>
            </body>
    '''

@app.route('/uploads/<filename>')
# ファイルを表示する
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

app.run()
