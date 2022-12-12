from flask import Flask, render_template, request
import argparse
from flask_cors import CORS
from views.sales_upload import sales_upload_app
from views.sample_export import sample_export_app
from views.xlwt_export import xlwt_export_app

app = Flask(__name__)
# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(app, resources=r'/*')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['doc/xls', 'zip']
app.config['UPLOAD_PATH'] = 'uploads'

app.register_blueprint(sales_upload_app)
app.register_blueprint(sample_export_app)
app.register_blueprint(xlwt_export_app)


@app.route("/")  # 默认首页
def index():
    return render_template("login.html")  # 默认首页


@app.route("/login", methods=["post"])  # 登录
def login():
    username = request.form.get("username")
    pwd = request.form.get("pwd")
    if username == "admin" and pwd == "admin":  # 验证账户和密码
        return render_template("index.html")
    else:
        return "登陆失败"


@app.route("/index", methods=["get"])
def index_page():
    return render_template("index.html")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='简单web服务')
    parser.add_argument('-main_host', '--main_host', default='127.0.0.1', help='')
    parser.add_argument('-web_port', '--web_port', default=8881, help='')
    args = parser.parse_args()

    app.run(host=args.main_host, port=args.web_port)
