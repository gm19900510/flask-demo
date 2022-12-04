from flask import Flask, render_template, request, Response, send_file
import argparse
from sqlalchemy import create_engine
import pandas as pd
from io import BytesIO
from urllib.parse import quote
import xlwt
import pymysql
from flask_cors import CORS

app = Flask(__name__)
# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(app, resources=r'/*')

engine = create_engine('mysql+pymysql://adbonline:!Mtt2020@****/adb')


# 利用create_engine和pd查询数据库数据返回查询结果
def engine_select_db():
    file = BytesIO()
    df = pd.read_sql_query(
        "select shop_name as '门店名称',shop_code as '门店编号'  from ods_api_shop where brand_region_naming like '%%苏南%%'",
        engine)
    writer = pd.ExcelWriter(file, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.save()  # 这个save不会落盘
    return file.getvalue()


@app.route("/export")  # 利用pd生成Excel文件并流式导出
def export():
    file_io_value = engine_select_db()
    return Response(
        file_io_value, mimetype="application/octet-stream",
        headers={"Content-Disposition": "attachment;filename={0}".format(quote("测试导出.xlsx"))}
    )


# 利用pymysql查询数据库数据，返回列名和查询结果
def pymysql_select_db():
    # 数据库连接对象
    conn = pymysql.connect(host='****', port=3306, user='adbonline',
                           password="!Mtt2020", db="adb")
    # 游标对象
    cur = conn.cursor()
    # sql语句
    sql = "select shop_name as '门店名称',shop_code as '门店编号'  from ods_api_shop"
    cur.execute(sql)
    # 获取表格的字段信息
    fields = cur.description
    # 获取所有数据
    rows = cur.fetchall()
    # 移动指针到某一行.如果mode='relative',则表示从当前所在行移动value条,如果mode='absolute',则表示从结果集的第一 行移动value条.
    cur.scroll(0, mode='absolute')
    cur.close()
    conn.close()
    return fields, rows


@app.route("/download")  # 利用worksheet生成Excel文件并下载
def download():
    # 创建一个workbook对象，就相当于创建了一个Excel文件
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)  # encoding:设置编码，可写中文；style_compression:是否压缩，不常用
    # 创建一个sheet对象，相当于创建一个sheet页
    worksheet = workbook.add_sheet('这是sheet1', cell_overwrite_ok=True)  # cell_overwrite_ok:是否可以覆盖单元格，默认为False
    # 向sheet页中添加数据：worksheet.write(行,列,值)

    # 更多样式设置请见：https://www.w3cschool.cn/python3/python-xlwt.html

    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 创建字体样式
    # 指定字体的具体属性(仅列出常用属性)
    font.name = "微软雅黑" # 指定字体
    font.height = 300  # 和excel字体大小比例是1:20（15号大小）
    font.bold = True  # 字体是否加粗
    font.underline = False  # 字体是否下划线
    font.struck_out = False  # 字体是否有横线
    font.italic = True  # 是否斜体字
    font.colour_index = 4  # 字体颜色


    # 创建对其格式的对象 Create Alignment
    alignment = xlwt.Alignment()
    # 水平居中 May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED,
    # HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    # 我上下对齐 May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
    alignment.vert = xlwt.Alignment.VERT_CENTER

    style.font = font  # 把字体添加到样式中
    # 将格式Alignment对象加入到样式对象Add Alignment to Style
    style.alignment = alignment
    '''
    worksheet.write(0, 0, "姓名")
    worksheet.write(0, 1, "性别")
    worksheet.write(0, 2, "年龄")
    worksheet.write(1, 0, "张三")
    worksheet.write(1, 1, "男")
    worksheet.write(1, 2, "18")
    '''
    fields, rows = pymysql_select_db()
    for field in range(len(fields)):
        worksheet.write(0, field, fields[field][0], style)

    # 结果写入excle
    for row in range(1, len(rows) + 1):
        for col in range(len(fields)):
            worksheet.write(row, col, rows[row - 1][col])

    worksheet.col(0).width = 500 * 20  # 设计第0列宽度
    worksheet.col(1).width = 250 * 20  # 设计第1列宽度

    f = BytesIO()
    workbook.save(f)
    f.seek(0)
    filename = quote("测试下载.xlsx")  # 将单个字符串编码转化为 %xx%xx 的形式
    rv = send_file(f, as_attachment=True, attachment_filename=filename)
    rv.headers['Content-Disposition'] += "; filename*=utf-8''{}".format(filename)
    rv.headers['Cache-Control'] = 'no-store'  # 重点在这句
    return rv


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='简单web服务')
    parser.add_argument('-main_host', '--main_host', default='127.0.0.1', help='')
    parser.add_argument('-web_port', '--web_port', default=8881, help='')
    args = parser.parse_args()

    app.run(host=args.main_host, port=args.web_port)
