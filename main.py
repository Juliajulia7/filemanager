import requests
import hashlib
import os
from pathlib import Path
from flask import Flask, render_template, request,  send_from_directory


def hashFor(data):
    # Prepare the project id hash
    hashId = hashlib.md5()
    hashId.update(repr(data).encode('utf-8'))
    return hashId.hexdigest()

def get(url):
    return requests.get(url)

def pathFile(hashname):
    dir1 = hashname[0:2]  # ??
    # pathdir='/storage/'+'dir1' + '/' #./
    pathdir = 'C:/Users/yuliya.kudasova/PycharmProjects/test' + '/storage/' + dir1 + '/'
    path = pathdir + hashname
    print(path)
    Path(pathdir).mkdir(parents=True, exist_ok=True)
    return path


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("mainpage.html")

@app.route("/upload", methods=['POST'])
def upload():
    for file in request.files.getlist("file"):
        hashfile = hashFor(file)
        filename= pathFile(hashfile)
        print(filename)
        file.save(filename)
    return render_template("complete.html", hashfile=hashfile)

@app.route('/download', methods=['POST'])
def download_file():
    if request.method == 'POST':
        filename = request.form.get('namefile')
        pathdir = 'C:/Users/yuliya.kudasova/PycharmProjects/test/storage/' + filename[0:2]
    return send_from_directory(pathdir, filename, as_attachment=True)

@app.route('/delete', methods=['POST'])
def delete_file():
    if request.method == 'POST':
        filename = request.form.get('deletefile')
        print(filename)
        path = pathFile(filename)
        print(path)
        try:
            os.remove(path)
        except OSError as e:
            pass
    return render_template("mainpage.html")

if __name__ == "__main__":
    app.run()