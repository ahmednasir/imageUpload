from flask import Flask, request, json
from PIL import  Image
from utils import image_util
import os
import uuid
import  datetime as dt
import pymongo
from flask_cors import CORS

client = pymongo.MongoClient("mongodb+srv://nasir:Q7N39tZUwSPJjAX@cluster0-zakdw.mongodb.net/test?retryWrites=true&w=majority")
db = client["Image"]
col = db["ImageMetaData"]

STORAGE_PATH = "/Users/nasirahmed/project/typito/uploads/"
IP_ADDRESS = "http://localhost:3000/"
app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload', methods=['POST'])
def upload():
    try:
        files = request.files.getlist('filesfld')
        print(files)
        file_path_dir = []
        root_dir = os.getcwd()

        image_arr = []
        for file in files:
            f_name = STORAGE_PATH + (str(uuid.uuid4().hex)) + file.filename

            f_name2 = STORAGE_PATH+"240/" + (str(uuid.uuid4().hex)) + file.filename
            f_name3 = STORAGE_PATH+"720/" + (str(uuid.uuid4().hex)) + file.filename

            # file_path = root_dir + f_name
            # path2 = root_dir + f_name2
            # path3 = root_dir + f_name3
            file.save(f_name)
            # file_path_dir.append(file_path)
            image = Image.open(f_name)

            image_status = image_util.format_image(image, f_name2, f_name3)
            if not image_status:
                continue
            obj = {
                "name": file.filename,
                "file1": f_name.replace(STORAGE_PATH,'uploads/'),
                "file2": f_name2.replace(STORAGE_PATH,'uploads/'),
                "file3": f_name3.replace(STORAGE_PATH,'uploads/'),
                "timestamp": dt.datetime.now()
            }
            col.insert_one(obj)
            obj1 = {
                "name": file.filename,
                "file1": f_name.replace(STORAGE_PATH,IP_ADDRESS),
                "file2": f_name2.replace(STORAGE_PATH,IP_ADDRESS),
                "file3": f_name3.replace(STORAGE_PATH,IP_ADDRESS),
                "timestamp": dt.datetime.now()
            }

            image_arr.append(obj1)
            print(obj1)
        resp_dict = {}
        resp_dict[dt.date.today().strftime("%d-%m-%y")]= image_arr
        print(resp_dict)
        response = app.response_class(
            response=json.dumps(resp_dict),
            status=200,
            mimetype='application/json'
        )
        return response
    except Exception as ex:
        print(ex)
        return app.response_class(
            response=json.dumps({}),
            status=200,
            mimetype='application/json'
        )




if __name__ == '__main__':
    app.run()
