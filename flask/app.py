#encoding:utf-8

#import config
#from models import User
#from exts import db
#from flask import request,session
import os
from flask import Flask, render_template, flash, redirect, url_for

#db.init_app(app)
#app.config_from_object(config)
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


traveling = {
    'username': '本次旅游计划中可供选择的旅游地点',
    'bio': 'Alternative places to visit in this travel plan',
}

travels = [
    {'name': '香港澳门', 'time': '在城市游玩时间3天'},
    {'name': '广州', 'time': '在城市游玩时间3天'},
    {'name': '北京', 'time': '在城市游玩时间3天'},
    {'name': '上海', 'time': '在城市游玩时间4天'},
    {'name': '杭州', 'time': '在城市游玩时间4天'},
    {'name': '新疆', 'time': '在城市游玩时间2天'},
    {'name': '内蒙古', 'time': '在城市游玩时间2天'},
    {'name': '云南', 'time': '在城市游玩时间3天'},
    {'name': '山东', 'time': '在城市游玩时间3天'},
    {'name': '南京', 'time': '在城市游玩时间4天'},
]

@app.route('/watchlist')
def watchlist():
    return render_template('travel.html', user=traveling, movies=travels)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/watchlist2')
def watchlist_with_static():
    return render_template('travel--.html', user=traveling, movies=travels)

@app.route('/where/')
def where():
    return render_template('where.html')

@app.route('/answer/')
def answer():
    return render_template('answer.html')


@app.route('/flash')
def just_flash():
    flash('开发中目标留言版旅行小贴士随意留言')
    return redirect(url_for('index'))

@app.route('/login/')
def login():
    return render_template('login.html')

#@app.route('/login')
#def login():
#   if  request.method == 'GET'
#       return render_template('login.html')
#   else:
#       telephone = request.form.get('telephone')
#       username = request.form.get('username')
#       user = User.query.filter(User.telephone == telephone,User.password == password).first()
#       if user:
#           session['user_id'] = user.id
#           session.permanent = True
#           return redirect(url_for('index'))
#       else:
#           return u'手机号码或者密码错误，请确认后重新输入登录！'

@app.route('/regist/')
def regist():
    return render_template('regist.html')

#@app.route('/regist')
#def regist():
#   if  request.method == 'GET'
#       return render_template('regist.html')
#   else:
#       telephone = request.form.get('telephone')
#       username = request.form.get('username')
#       password1 = request.form.get('password1')
#       password2 = request.form.get('password2')
#       user = User.query.filter(User.telephone == telephone).first()
#       if user:
#           retutn '该手机号已被注册,请使用其它手机号码注册1'
#       else:
#           if password1 !=password2:
#               return u'两次密码不同，请重新输入密码和确认密码!'
#           else:
#               user = User(telephone=telephone,username=username,password=password1)
#               db.session.add(user)
#               db.session.commit()
#               return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500







