## 简介
使用大模型给用户提供一个学习技能平台，用户可以输入用户名，输入学习技能，比如Java、python等
生成学习路径之后，用户可以保存自己的路径。保存好在左边栏就可以显示已保存的数据
还可以继续点击左边的链接继续深入学习各个子项目。还可以通过只读模式学习更详细
的资料

## 技术栈
使用了python的Flask web框架，前端使用HTML。
使用的是通义千问大模型

### 安装
  保证已安装python3，开发使用 3.12.5版本,并且已安装pip
  依次运行命令安装python模块
    
    pip install Flask
    pip install markdown-it-py
    pip install markdown
    pip install cryptography
    pip install dashscope
    
### 配置通义千问key
  在电脑的命令行键入设置key $env:DASHSCOPE_API_KEY = "sk-xxx" (sk-xxx 需要替换成你自己的key)
  
### 新建数据并导入sql文件
  在mysql新建一个数据库llm-learn，并且导入项目根目录llm-learn.sql文件

### 配置文件
  配置根目录 __init__.py 的数据库配置
  username:password@host/dbname

### 运行
  在项目根目录，运行命令行输入 `python run.py`
  