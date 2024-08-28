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
    # answer = {
    #     "code": "",
    #     "message": "",
    #     "output": {
    #         "choices": [
    #             {
    #                 "finish_reason": "stop",
    #                 "message": {
    #                     "content": "### Python 学习路径\n\n#### 初级阶段\n\n1. **Python 基础**\n   - 安装 Python（推荐使用 Anaconda 或者通过官方 Python 安装指南）\n   - 学习基本语法：变量、数据类型（整数、浮点数、字符串）、运算符、控制流（if, for, while）\n   - 函数与模块导入，如 `math` 和 `random`\n   - 文件操作：读写文件、处理文本文件\n\n2. **数据结构与算法**\n   - 列表、元组、字典、集合的操作与应用\n   - 字典推导式、列表推导式\n   - 常见排序算法（冒泡排序、选择排序、插入排序、快速排序）\n   - 简单的递归算法\n\n3. **面向对象编程**\n   - 类与对象的概念\n   - 封装、继承、多态\n   - 面向对象设计原则（SOLID）\n\n#### 中级阶段\n\n4. **函数式编程与装饰器**\n   - 使用高阶函数（如 map, filter, reduce）\n   - 装饰器的使用与实现\n   - Lambda 表达式\n\n5. **异常处理与调试**\n   - 异常捕获与自定义异常类\n   - 使用日志库（如 logging）进行错误记录与调试\n\n6. **文件与网络编程**\n   - 处理二进制文件与使用文件句柄\n   - HTTP 请求与响应处理（使用 requests 库）\n   - 基本的 socket 编程\n\n7. **Web 开发基础**\n   - 使用 Flask 或 Django 构建 Web 应用\n   - 模板系统（如 Jinja2）\n   - 数据库集成（使用 SQLAlchemy 或 Django ORM）\n\n#### 进阶阶段\n\n8. **数据处理与分析**\n   - 使用 pandas 进行数据清洗、转换、聚合与可视化\n   - 数据可视化工具（如 Matplotlib, Seaborn, Plotly）\n\n9. **机器学习与深度学习**\n   - 使用 scikit-learn 进行基本的机器学习模型构建\n   - TensorFlow 或 PyTorch 的基础使用\n   - 数据集处理与模型训练流程\n\n10. **性能优化与并发**\n    - 内存管理与垃圾回收\n    - 使用多线程或异步 I/O（asyncio）提高程序性能\n    - 使用 Redis 或其他缓存技术优化数据访问速度\n\n#### 实战项目\n\n- **个人项目**：选择一个兴趣领域（如数据科学、Web 开发、游戏开发等），使用 Python 完成一个完整的项目，例如：数据分析报告、小型网站、简单的游戏等。\n\n#### 持续学习与扩展\n\n- **参加在线课程**：Coursera、Udemy、edX 等平台提供的 Python 相关课程。\n- **阅读文档与社区资源**：深入学习 Python 标准库、第三方库的文档，并参与 Stack Overflow、GitHub 等社区交流。\n- **参与开源项目**：在 GitHub 上寻找感兴趣的开源项目贡献代码或问题解答，提升实战能力。\n\n通过以上步骤，你可以从零基础开始，逐步成长为熟练掌握 Python 的开发者。记得在学习过程中实践动手，将理论知识应用于实际项目中，这样才能更好地理解和掌握 Python 编程。",
    #                     "role": "assistant"
    #                 }
    #             }
    #         ],
    #         "finish_reason": "null",
    #         "text": "null"
    #     },
    #     "request_id": "0072a949-31f7-92b6-a814-e04b7a89fe84",
    #     "status_code": 200,
    #     "usage": {
    #         "input_tokens": 47,
    #         "output_tokens": 726,
    #         "total_tokens": 773
    #     }
    # }
    # content = answer['output']['choices'][0]['message']['content']
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
