import requests
import hashlib
import os
from pathlib import Path
from flask import Flask, render_template, request,  send_from_directory


def hashFor(data):
    hashId = hashlib.md5()
    hashId.update(repr(data).encode('utf-8'))
    return hashId.hexdigest()

def get(url):
    return requests.get(url)

def pathFile(hashname):
    if len(hashname) >= 2:
       dir1 = hashname[0:2]
    else:
        hashname=hashname + '0z'
    # pathdir='/storage/'+'dir1' + '/' #./
    pathdir = 'C:/Users/yuliya.kudasova/PycharmProjects/test' + '/storage/' + dir1 + '/'
    path = pathdir + hashname
    print(path)
    Path(pathdir).mkdir(parents=True, exist_ok=True)
    return path


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route("/")
def index():
    return render_template("mainpage.html")

@app.route("/managerfile", methods=['POST', 'GET', 'DELETE'])
def upload():
    if request.method == 'POST':
        file =request.files['file']
        hashfile = hashFor(file)
        filename= pathFile(hashfile)
        file.save(filename)
        return hashfile
    elif request.method == 'GET':
        filename = request.form.get('filename')
        if len(filename)>=2:
            pathdir = 'C:/Users/yuliya.kudasova/PycharmProjects/test/storage/' + filename[0:2]
            return send_from_directory(pathdir, filename, as_attachment=True)
        else:
            return "Name is not correct"
    elif request.method == 'DELETE':
        filename = request.form.get('filename')
        path = pathFile(filename)
        if os.path.exists(path):
            os.remove(path)
            return "Ok"
        else:
            return "File does not exist"


if __name__ == "__main__":
    app.run()