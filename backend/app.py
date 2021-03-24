from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import os,json
import argparse
import base64
import example
import sys
app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = r"./uploadFiles/pictures"
app.config['UPLOAD_FOLDER'] = sys.path[0]+'/../uploadFiles/pictures'
#CORS(app, resources={r'/*': {'origins': '*'}})
CORS(app)
'''data=request.args.get('keyword')
    print('keyword',data)'''


def return_img_stream(img_local_path):
  """
  工具函数:
  获取本地图片流
  :param img_local_path:文件单张图片的本地绝对路径
  :return: 图片流
  """

  img_stream = ''
  with open(img_local_path, 'rb') as img_f:
    img_stream = img_f.read()
    img_stream = base64.b64encode(img_stream).decode()
  return img_stream


# 测试代码
@app.route('/', methods=['POST', 'GET'])
def pingg_pong():
  if request.method == 'GET':
    # get请求是网上复制的代码，没修改过，目前只使用POST
    graph = request.read_json("static/data/miserables.json")
    return graph
  if request.method == 'POST':
    print(jsonify('{1:‘a’,2:‘b’,3:‘c’}'))
    data = request.get_json(silent=True)
    print(data)
    for i in range(100000):
      print(i)
      a = i
    # a=1
    # return jsonify('{1:‘a’,2:‘b’,3:‘c’}')     #（jsonify返回一个json格式的数据
    return jsonify({1: a})

@app.route('/uploadFile', methods=['POST'])
def upload():
  if request.method =='POST':
    #name = request.form.get("name")
    # #description = request.form.get("description")
    file = request.files.get("file")
    print(dir(file))
    print(file.filename)
    print(file.filename.split('.')[1])
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], "temp." + file.filename.split('.')[1])
    file.save(file_path)
    img_stream = return_img_stream(file_path)
    os.remove(file_path)
    return img_stream


@app.route('/face_forgery', methods=['POST'])
def face_forgery():
  if request.method == 'POST':
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], "temp.jpg")
    picurl = request.form.get("picurl")
    picture = base64.b64decode(picurl)
    file = open(file_path, "wb")
    file.write(picture)
    file.close()

    method = 'df'
    path = file_path[:-17]
    prob =example.main(method,path)
    print(prob)
    data = {'probability': prob}
    os.remove(file_path)
    return data

if __name__ == '__main__':
  app.run(host='0.0.0.0')
