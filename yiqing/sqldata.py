import pymysql


def mysql():
    db = pymysql.connect(host='localhost', user='root', password='输入你的密码', database='covid', charset='utf8')
    cur = db.cursor()
    return db, cur


def close(db, cur):
    cur.close()
    db.close()


def query(sql: str, *args):
    db, cur = mysql()
    cur.execute(sql, args)
    result = cur.fetchall()
    close(db, cur)
    return result


# 一个时间区间内，累计确诊、治愈、死亡人数
def get_l1_data():
    sql = """
    select 时间,确诊人数,治愈人数,死亡人数 from 历史数据
    """
    return query(sql)


# 一个时间区间内，新增确诊和治愈情况
def get_l2_data():
    sql = """
    select 时间,新增确诊,新增治愈 from 历史新增数据
    """
    return query(sql)


# 全国累计确诊人数、新增确诊、累计治愈、累计死亡人数
def get_c1_data():
    sql = """
    select 确诊人数,新增确诊,治愈人数,死亡人数 from 关键数据
    """
    return query(sql)[0]


# 全国以省级为单位的 新增确诊信息
def get_c2_data():
    sql = """
    select 省份,sum(新增确诊) from 当日数据
    group by 省份
    """
    return query(sql)


# 省/直辖市当日的新增确诊 前五
def get_r1_data():
    # 此语句筛选出当日，每个城市的累计确诊情况，不易观察，故作废
    # sql = """
    # select 城市,确诊人数 from
    # (
    # select 城市,确诊人数 from 当日数据
    # where 省份 not in ("北京","上海","天津","重庆")
    # union all
    # select 省份 as 城市,sum(确诊人数) as 确诊人数 from 当日数据
    # where 省份 in ("北京","上海","天津","重庆")
    # group by 省份
    # )
    # as 城市现有确诊
    # order by 确诊人数 desc limit 5
    # """

    # 此语句筛选出每个省份或直辖市，当日的新增总数
    sql = """
    select 省份,sum(新增确诊) as 新增确诊 from 当日数据
    group by 省份
    order by 新增确诊 desc limit 5
    """
    return query(sql)


# 江苏省各城市当日现有确诊人数
def get_r2_data():
    sql = """
    select 城市,确诊人数 from 当日数据
    where 省份='江苏' and 城市 not in ('地区待确认','境外输入')
    order by 新增确诊 
    """
    return query(sql)

