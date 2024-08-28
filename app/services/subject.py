from flask import jsonify, json

from ..models import subject

def create_post(subjects, user, pid):
    print(subjects)
    # 先删除再添加
    # 删除具有特定 pid 值的所有记录
    try:
        subject.Subject.query.filter_by(pid=int(pid), user=user).delete()
        subject.db.session.commit()
    except Exception as e:
        subject.db.session.rollback()
        response = {
            'error': str(e)
        }
        return jsonify(response), 500

    for sub_id, title in subjects.items():
        post = subject.Subject(user=user, pid=int(pid), stage_id=int(sub_id), title=title)
        subject.db.session.add(post)
    subject.db.session.commit()
    return post

def get_user_subject(user):
    subjects = subject.Subject.query.filter_by(user=user).all()
    subjects_dicts = [s.to_dict() for s in subjects]
    return subjects_dicts