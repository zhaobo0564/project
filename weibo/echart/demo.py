import datetime

import pymysql

account = {
    'user' : 'root',
    'password' : 'zhaobo123..',
    'host' : 'localhost',
    'database' : 'python'
}



def mysqlConnect(account):
    connect = pymysql.connect(**account)
    return connect

def getMessage(cursor, month, day, year, phone, dianzan, zhuanfa, pinlun, textLength, dates):
    sql = 'select * from weibo ORDER BY created_at'
    cursor.execute(sql)
    row = cursor.fetchall()
    Day = {} #建立字典便于统计每天发送的微博
    Year = {}
    Month = {}
    for i in range(1, 32):
        Day[i] = 0
    for i in range(1, 13):
        Month[i] = 0
    for i in range(2013, 2021):
        Year[i] = 0

    for it in row:
        date = datetime.datetime.strptime(it['created_at'],  " %Y-%m-%d")
        Year[date.year] += 1
        Day[date.day] += 1
        Month[date.month] += 1
        phone.append(it['source'])
        dianzan.append(it['attitudes_count'])
        zhuanfa.append(it['reposts_count'])
        pinlun.append(it['comments_count'])
        textLength.append(it['textLength'])
        dates.append(it['created_at'])

    for i in range(1, 32):
        day.append(Day[i])
    for i in range(1, 13):
        month.append(Month[i])
    for i in range(2013, 2021):
        year.append(Year[i])



if __name__ == '__main__':
    month = []  # 按照月发送的微博
    year = []   # 按照年发送的微博
    day = []    # 按照日发送的微博
    phone = []  # 手机的种类
    dianzan = [] # 点赞数
    zhuanfa = [] # 转发数
    pinlun = [] # 评论数
    textLength = [] #发送微博长度
    dates = [] # 时间
    connect = mysqlConnect(account)
    cursor = connect.cursor(cursor=pymysql.cursors.DictCursor)
    getMessage(cursor, month, day, year, phone, dianzan, zhuanfa, pinlun, textLength, dates)
    # 数据可视化

    from pyecharts.charts import Bar
    from pyecharts import options as opts

    #按照日 发微博的个数
    xday = []
    for i in range(1, 32):
        xday.append(i)
    bar = (
        Bar()
            .add_xaxis(xday)
            .add_yaxis("每天发送的微博", day)
            .set_global_opts(title_opts=opts.TitleOpts(title="狗哥发微博统计"))
    )
    bar.render(path= 'day.html')
    # 按月
    xmonth = []
    for i in range(1, 13):
        xmonth.append(i)
    bar = (
        Bar()
            .add_xaxis(xmonth)
            .add_yaxis("每月发送的微博", month)
            .set_global_opts(title_opts=opts.TitleOpts(title="狗哥发微博统计"))
    )
    bar.render(path = 'month.html')
    # 按年
    xyear = []
    for i in range(2013, 2021):
        xyear.append(i)
    bar = (
        Bar()
            .add_xaxis(xyear)
            .add_yaxis("每年发送的微博", year)
            .set_global_opts(title_opts=opts.TitleOpts(title="狗哥发微博统计"))
    )
    bar.render(path='year.html')


    # 分析手机
    Phone = {}
    for it in phone:
        Phone[it] = 0
    for it in phone:
        Phone[it] += 1


    from pyecharts import options as opts
    from pyecharts.charts import Pie
    from pyecharts.faker import Faker

    c = (
        Pie()
            .add("", [list(z) for z in zip(Phone.keys(), Phone.values())])
            #.set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
            #.set_global_opts(title_opts=opts.TitleOpts(title="狗哥发微博的设备"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .render("phone.html")
    )

    # 分析按时间 点赞 评论 转发

    import pyecharts.options as opts
    from pyecharts.charts import Line
    from pyecharts.faker import Faker

    c = (
        Line()
            .add_xaxis(dates)
            .add_yaxis("点赞", dianzan, is_smooth=True)
            .add_yaxis("转发", zhuanfa, is_smooth=True)
            .add_yaxis("评论", pinlun, is_smooth=True)
            .add_yaxis("文章长度", textLength, is_smooth=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="狗哥微博转发点赞等数据"))
            .render("msg.html")
    )