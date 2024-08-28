from flask import Blueprint, render_template, request, redirect, url_for
from __init__ import db
from .services import learning
from .services import subject


bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/learning', methods=['GET'])
def get_learn():
    user = request.args.get('user')
    subjects = subject.get_user_subject(user)
    learns = learning.get_user_learn(user, subjects)
    return learns

@bp.route('/learning', methods=['POST'])
def learn():
    course = request.form.get('language')
    readonly = request.form.get('readonly')
    data = learning.get_from_llm(course, readonly)
    return data

@bp.route('/learn_subject', methods=['get'])
def learn_subject():
    subject = request.args.get('subject')
    pid = request.args.get('pid')
    readonly = request.args.get('readonly')
    data = learning.get_from_llm(subject, readonly, pid)
    return data

@bp.route('/save_my_learn', methods=['POST'])
def create():
    data = request.json  # 获取 JSON 数据
    my_learn = data.get('my_learn', [])
    subjects = data.get('subject', {})
    user = data.get('user', '')
    pid = data.get('pid', 0)

    subject.create_post(subjects, user, pid)
    learning.create_post(my_learn, user, pid)

    return 'success'
