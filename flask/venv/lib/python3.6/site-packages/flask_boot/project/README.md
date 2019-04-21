## Flask使用
### 请求数据使用marshmallow.fields
#### 单数据来源解析：
    ```
    from marshmallow.fields import Str, Int
    
    test_args = {
        'name': Str(required=True),
        'password': Int(required=True)
    }
    args = args_parser.parse(test_args)
    ```
#### 全部数据解析：
    ```
    args = args_parser.parse_all()
    ```
#### 项目启动：
    python manage.py runserver -p 6000
#### 或：
    gunicorn -w 4 -b 127.0.0.1:6000 wsgi:app
   
