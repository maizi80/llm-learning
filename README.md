## 简介
利用大型模型为用户提供一个学习技能的平台，用户能够输入其用户名，并输入所希望学习的技能，例如Java、Python等，以生成相应的学习路径。用户在完成路径的保存后，该路径将出现在左侧的栏目中，展示已保存的学习资料。用户亦可继续点击左侧的链接，深入学习各个子项目。此外，用户还可以通过阅读模式获取更详尽的学习资料。

## 技术栈
使用了python的Flask web框架，前端使用HTML。
使用的是通义千问大模型

### 安装
  保证已安装python3，开发使用 3.12.5版本,并且已安装pip(可选安装python3.12的步骤)
    
  ```code
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt-get update
  sudo apt-get install python3.12
  ```
  - 安装MySQL（如已安装跳过）
    `apt install mysql-server`
    

  - 克隆项目

  `git clone https://github.com/maizi80/llm-learning.git`

  - 进入目录

  `cd llm-learning`

  - 依次运行命令安装python模块

    ```code
      pip install Flask
      pip install flask-sqlalchemy
      pip install markdown-it-py
      pip install markdown
      pip install cryptography
      pip install dashscope
      pip install pymysql
      pip install jsonpickle
    ```
  - 创建数据库

    `mysql -u root -p`

    `create database llm_learning;`
  - 导入数据库文件
    
    `mysql -u root -p llm_learning < /www/llm-learning/llm-learn.sql`
    
### 配置通义千问key
  在电脑的命令行键入设置`export DASHSCOPE_API_KEY="sk-xxx"` (sk-xxx 需要替换成你自己的key)
  
### 新建数据并导入sql文件
  在mysql新建一个数据库llm-learn，并且导入项目根目录llm-learn.sql文件

### 配置文件
  配置根目录 __init__.py 的数据库配置
  username:password@host/dbname

### 运行
  在项目根目录，运行命令行输入 `python run.py`
  