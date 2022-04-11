from flask import Flask, render_template, jsonify
import sqldata

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')


@app.route('/l1')
def get_data_l1():
    data = sqldata.get_l1_data()
    # 将日期，确诊，治愈，死亡人数写入列表，并返回json格式
    date, confirm, heal, dead = [], [], [], []
    for i, j, m, n in data:
        date.append(i)
        confirm.append(j)
        heal.append(m)
        dead.append(n)
    return jsonify({
        'date': date,
        'confirm': confirm,
        'heal': heal,
        'dead': dead
    })


@app.route('/l2')
def get_data_l2():
    data = sqldata.get_l2_data()

    date, confirm_add, heal_add = [], [], []
    for i, j, k in data:
        date.append(i)
        confirm_add.append(j)
        heal_add.append(k)
    return jsonify({
        'date': date,
        'confirm_add': confirm_add,
        'heal_add': heal_add
    })


@app.route('/c1')
def get_data_ci():
    confirm, suspect, heal, dead = sqldata.get_c1_data()
    return jsonify({
        'confirm': confirm,
        'suspect': suspect,
        'heal': heal,
        'dead': dead
    })


@app.route('/c2')
def get_data_c2():
    data = sqldata.get_c2_data()
    result = []
    for item in data:
        result.append({'name': item[0], 'value': int(item[1])})
    return jsonify({
        'key_data': result
    })


@app.route('/r1')
def get_data_r1():
    data = sqldata.get_r1_data()
    province, confirm_add = [], []
    for i, j in data:
        province.append(i)
        confirm_add.append(int(j))
    return jsonify({
        'province': province,
        'confirm_add': confirm_add
    })


@app.route('/r2')
def get_data_r2():
    data = sqldata.get_r2_data()
    city, confirm = [], []
    for i, j in data:
        city.append(i)
        confirm.append(j)
    return jsonify({
        'city': city,
        'confirm': confirm
    })


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, threaded=True)
