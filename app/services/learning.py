from flask import jsonify, json
from markdown_it import MarkdownIt
from markdown_it.token import Token
from ..models import learn
import dashscope
from dashscope import Generation
import jsonpickle

def get_from_llm(course, readonly, pid=0):
    messages = [
        {'role': 'system',
         'content': '你是程序语言学习指导专家。你的任务是为编程语言生成一个结构化的学习路径。所有建议和路径都必须以事实为基础，切实可行。'},
        {'role': 'user', 'content': course}
    ]
    print(messages)
    response = Generation.call(
        model="qwen-turbo",
        messages=messages,
        temperature=0.8,
        result_format='message'
    )
    answer = response.output.choices[0].message.content
    content = answer
    if readonly == '1':
        return content
    else:
        return parse_markdown(content, pid)

def parse_markdown(md_text, pid):
    md = MarkdownIt()
    tokens = md.parse(md_text)
    def traverse_tokens(tokens):
        tree = []
        i = 1
        current_parent = {
            'id': 0,
            'pid': pid,
            'level': 0,
            'title': '',
            'head_id': 0,
            'order_id': 0,
            'bullet_id': 0,
            'children': [],
        }

        def process_list(token, is_ordered):
            nonlocal i
            nonlocal current_parent
            if is_ordered:
                current_parent['order_id'] = i
            else:
                current_parent['bullet_id'] = i

        for token in tokens:
            if token.type.startswith('ordered_list_open'):
                process_list(token, True)

            if token.type.startswith('ordered_list_close'):
                process_list(token, False)
                current_parent['order_id'] = 0
                current_parent['bullet_id'] = 0

            if token.type.startswith('bullet_list_open'):
                process_list(token, False)

            if token.type.startswith('bullet_list_close'):
                process_list(token, False)
                current_parent['bullet_id'] = 0

            if token.type == 'inline':
                current_parent['id'] = i
                current_parent['title'] = token.content
                current_parent['level'] = token.level
                # if i == 34:
                #     print(current_parent)
                tree.append(current_parent.copy())
                i += 1
        # return tree
        tr = h = b = c = []
        children = []
        for node in tree:
            if node['order_id'] == 0 and node['bullet_id'] == 0:
                b = []
                node['children'] = b
                h.append(node)
            if node['order_id'] != 0 and node['bullet_id'] == 0:
                c = []
                node['children'] = c
                b.append(node)

            if node['order_id'] != 0 and node['bullet_id'] != 0:
                c.append(node)

        return h
    return traverse_tokens(tokens)

def create_post(learns, user, pid):
    # 先删除再添加
    # 删除具有特定 pid 值的所有记录
    try:
        learn.Learn.query.filter_by(pid=int(pid), user=user).delete()
        learn.db.session.commit()
    except Exception as e:
        learn.db.session.rollback()
        response = {
            'error': str(e)
        }
        return jsonify(response), 500
    for item in learns:
        hid, oid, bid, sid = item.split('_')
        post = learn.Learn(user=user, pid=int(pid), hid=int(hid), oid=int(oid), bid=int(bid), sid=int(sid))
        learn.db.session.add(post)
    learn.db.session.commit()
    return post

# 获取列表
def get_user_learn(user, subject):
    learns = learn.Learn.query.filter_by(user=user).all()
    learns_dicts = [l.to_dict() for l in learns]
    tree = build_tree(learns_dicts, subject)
    return tree

def build_tree(learns, subject):

    s = {}
    for item in subject:
        # 使用stage_id作为键，title作为值
        s[item['stage_id']] = item['title']
    h = c = []
    for l in learns:
        o = {
            'id': l['sid'],
            'title': s[l['sid']],
            'oid': l['oid'],
            'children': [],
        }
        if l['oid'] == 0 and l['bid'] == 0:
            b = []
            o['children'] = b
            h.append(o)
        if l['oid'] != 0 and l['bid'] == 0:
            c = []
            o['children'] = c
            b.append(o)
        if l['oid'] != 0 and l['bid'] != 0:
            c.append(o)
    return h
