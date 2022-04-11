import pymysql
import time
import requests
import json


def mysql():
    db = pymysql.connect(host='localhost', user='root', password='输入你的密码', database='covid', charset='utf8')
    cur = db.cursor()
    return db, cur


def get_json(url):
    headers = {
        'user - agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 80.0.3987.116Safari / 537.36'
    }
    response = requests.get(url=url, headers=headers).text
    data = json.loads(response)
    return data['data']


# 获取当日数据
def get_now(data):
    now = []
    data_time = str(data['diseaseh5Shelf']['lastUpdateTime'])  # 数据更新时间
    data_all = data['diseaseh5Shelf']['areaTree'][0]
    data_province_s = data['diseaseh5Shelf']['areaTree'][0]['children']

    # 获取全国今日新增、累计确诊、治愈人数、死亡人数
    confirms = data_all['total']['confirm']
    confirms_add = data_all['today']['confirm']
    heals = data_all['total']['heal']
    deads = data_all['total']['dead']

    # 获取每个省份的每个城市今日新增、累计确诊、治愈人数、死亡人数
    for data_province in data_province_s:
        province = data_province['name']  # 省份
        for data_city in data_province['children']:
            city = data_city['name']  # 城市
            confirm = data_city['total']['confirm']  # 确诊
            confirm_add = data_city['today']['confirm']  # 新增
            heal = data_city['total']['heal']  # 治愈
            dead = data_city['total']['dead']  # 死亡
            now.append((data_time, province, city, confirm_add, confirm, heal, dead))

    return confirms, confirms_add, heals, deads, now


# 获取历史数据
def get_past(data):
    past = {}
    for data_day in data:
        data_time = data_day['date']  # 获取最原始的时间
        time_deal = time.strptime(data_time, '%m.%d')  # 根据指定的格式把一个时间字符串解析为时间元组
        date = time.strftime('%m-%d', time_deal)  # 重新组成新的时间字符串
        past[date] = {
            'confirm': data_day['confirm'],  # 确诊
            'suspect': data_day['suspect'],  # 疑似
            'heal': data_day['heal'],  # 治愈
            'dead': data_day['dead']  # 死亡
        }

    return past


# 写入当日数据
def insert_now(now):
    db, cur = mysql()
    try:
        cur.execute("DROP TABLE IF EXISTS 当日数据")
        # 写创建表的sql语句
        set_sql_now = "create table 当日数据(时间 varchar(100),省份 varchar(50),城市 varchar(50),新增确诊 int(11)," \
                      "确诊人数 int(11),治愈人数 int(11),死亡人数 int(11))ENGINE=InnoDB DEFAULT CHARSET=utf8"
        # 执行sql语句
        cur.execute(set_sql_now)
        # 保存
        db.commit()
        # 写入数据库
        save_sql_now = "insert into 当日数据 values(%s,%s,%s,%s,%s,%s,%s)"
        cur.executemany(save_sql_now, now)  # now位置必须是个列表，列表里面的元素是数组
        db.commit()
        print('当日数据写入成功')
    except Exception as e:
        print('当日数据写入失败原因:%s' % e)


# 写入历史数据
def insert_past(past):
    db, cur = mysql()
    try:
        cur.execute("DROP TABLE IF EXISTS 历史数据")
        # 写创建表的sql语句
        set_sql_past = "create table 历史数据(时间 varchar(100),确诊人数 int(11),疑似病例 int(11),治愈人数 int(11)," \
                       "死亡人数 int(11))ENGINE=InnoDB DEFAULT CHARSET=utf8"
        # 执行sql语句
        cur.execute(set_sql_past)
        # 保存
        db.commit()
        # 写入历史数据
        for date, data in past.items():
            sql_past = f"insert into 历史数据 values('{date}',{data['confirm']},{data['suspect']},{data['heal']}," \
                       f"{data['dead']})"
            cur.execute(sql_past)
        db.commit()
        print('历史数据写入成功')
    except Exception as e:
        print('历史数据写入失败原因:%s' % e)


# 写入历史新增数据
def insert_past_add(past):
    db, cur = mysql()
    try:
        cur.execute("DROP TABLE IF EXISTS 历史新增数据")
        # 写创建表的sql语句
        set_sql_past = "create table 历史新增数据(时间 varchar(100),新增确诊 int(11),新增疑似 int(11),新增治愈 int(11)," \
                       "新增死亡 int(11))ENGINE=InnoDB DEFAULT CHARSET=utf8"
        # 执行sql语句
        cur.execute(set_sql_past)
        # 保存
        db.commit()
        # 写入历史数据
        for date, data in past.items():
            sql_past = f"insert into 历史新增数据 values('{date}',{data['confirm']},{data['suspect']},{data['heal']}," \
                       f"{data['dead']})"
            cur.execute(sql_past)
        db.commit()
        print('历史新增数据写入成功')
    except Exception as e:
        print('历史新增数据写入失败原因:%s' % e)


# 写入累计确诊等四个关键数据
def insert_main(confirm, confirm_add, heal, dead):
    db, cur = mysql()
    try:
        cur.execute("DROP TABLE IF EXISTS 关键数据")
        # 写创建表的sql语句
        set_sql_main = "create table 关键数据(确诊人数 int(11),新增确诊 int(11),治愈人数 int(11),死亡人数 int(11))" \
                       "ENGINE=InnoDB DEFAULT CHARSET=utf8"
        cur.execute(set_sql_main)
        db.commit()
        # 写入确诊人数、新增确诊、治愈人数、死亡人数的数据
        save_sql_main = f"insert into 关键数据 values({confirm},{confirm_add},{heal},{dead})"
        cur.execute(save_sql_main)
        db.commit()
        print('关键数据写入成功')
    except Exception as e:
        print('关键数据写入失败原因:%s' % e)


def main():
    # 用于请求获得每日最新数据
    url_1 = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=statisGradeCityDetail,diseaseh5Shelf'
    # 用于获取以前的历史数据
    url_2 = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,nowConfirmStatis,provinceCompare'
    data_1 = get_json(url_1)
    data_2 = get_json(url_2)
    data_3 = data_2['chinaDayList']
    data_4 = data_2['chinaDayAddList']
    # 数据筛选
    confirms, confirms_add, heals, deads, now = get_now(data_1)   # 当日数据筛选
    past = get_past(data_3)  # 历史累计数据筛选
    past_add = get_past(data_4)  # 历史每日数据筛选
    # 把数据插入到数据库
    insert_now(now)
    insert_past(past)
    insert_past_add(past_add)
    insert_main(confirms, confirms_add, heals, deads)


if __name__ == '__main__':
    main()
