from flask import Blueprint, Response, render_template, request
from sqlalchemy import create_engine
import pandas as pd
from io import BytesIO
from urllib.parse import quote

pandas_export_app = Blueprint('pandas_export', __name__)

engine = create_engine('mysql+pymysql://adbonline:!Mtt2020@am-2zergx17v1uk99z1w90650o.ads.aliyuncs.com/adb')


# 利用create_engine和pd查询数据库数据返回查询结果
def engine_select_db(date):
    file = BytesIO()
    sql = '''       
        with display_tab as (
            select shop_id,style,color,date,
                max(if(display_location = '1','Y','N')) '模特',
                max(if(display_location = '2','Y','N')) '橱窗',
                max(if(display_location = '3','Y','N')) '正挂',
                max(if(display_location = '4','Y','N')) '侧挂'
            from ods_app_display_daily_details where date='{}' group by shop_id,style,color,date order by shop_id,style,color
        ), 
        event_tab as (
            select * from ods_app_event_daily_details where date='{}'
        ),
        sample_tab as (
            select * from ods_app_sample_daily_details where date='{}'
        )
        select shop_code,shop_name,st.theme,st.style,st.color,IFNULL(sample,0) as '出样',
            IFNULL(touch,0) as '触摸',
            IFNULL(try,0) as '试穿',
            IFNULL(模特,'N') as 模特,
            IFNULL(橱窗,'N') as 橱窗,
            IFNULL(正挂,'N') as 正挂,
            IF(模特 is null and 橱窗 is null and 侧挂 is null and 侧挂 is null,'Y',侧挂) as 侧挂
        from sample_tab st 
        left join event_tab et on st.shop_id=et.shop_id and st.style=et.style and st.color=et.color
        left join display_tab dt on st.shop_id=dt.shop_id and st.style=dt.style and st.color=dt.color
        left join ods_api_shop shop on st.shop_id=shop.id   
        order by st.shop_id,st.theme,st.style,st.color asc
    '''
    sql = sql.format(date, date, date)
    df = pd.read_sql_query(sql, engine)
    writer = pd.ExcelWriter(file, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.save()  # 这个save不会落盘
    return file.getvalue()


@pandas_export_app.route("/export")  # 利用pd生成Excel文件并流式导出
def export():
    # 接收处理json数据请求
    date = request.args.get('date')
    file_io_value = engine_select_db(date)
    return Response(
        file_io_value, mimetype="application/octet-stream",
        headers={"Content-Disposition": "attachment;filename={0}".format(quote(date + "数据.xlsx"))}
    )

@pandas_export_app.route("/export/page")  #调整导出页面
def export_page():
    return render_template("export_page.html")  # 默认首页
