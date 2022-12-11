from flask import Blueprint, render_template, request, current_app, Response
from werkzeug.utils import secure_filename
import os
from utils.type_tools import get_filetype_by_stream
from sqlalchemy import create_engine
import warnings

import pandas as pd
import json
from pypinyin import lazy_pinyin

warnings.filterwarnings('ignore')
sales_upload_app = Blueprint('sales_upload', __name__)

engine = create_engine('mysql+pymysql://adbonline:!Mtt2020@am-2zergx17v1uk99z1w90650o.ads.aliyuncs.com/adb')
connect = engine.connect()


@sales_upload_app.route('/sales/upload', methods=['GET', 'POST'])
def sales_upload():
    if request.method == 'GET':
        return render_template('sales_upload.html')
    else:
        f = request.files['file']
        filename = secure_filename(''.join(lazy_pinyin(f.filename)))
        if filename != '':
            file_ext = get_filetype_by_stream(f.stream)
            print(file_ext)
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                return "文件格式不正确，请重新选择格式上传", 400

        altsep = os.path.altsep
        dir_path = os.path.curdir + altsep + "uploads"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        f.save(os.path.join(dir_path, filename))

        dataset = pd.read_excel(f, header=0)
        dataset['销售日期'] = pd.to_datetime(dataset['销售日期']).dt.strftime('%Y-%m-%d')
        print(dataset.dtypes)
        print(dataset)
        dataset = dataset.query("销售金额>0", inplace=False)
        print(dataset)
        dataset.to_sql(name='ods_sunan_week_sales', con=connect, if_exists='append', index=False, chunksize=100)
        return Response(json.dumps({'result': 200, 'message': '文件上传成功'}), mimetype='application/json')
