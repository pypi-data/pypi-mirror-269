## 一、目录说明
```
├── README.md               # 帮助文档
├── .gitignore              # 配置忽略不想被GIT管理的文件
├── .chargespot                # 项目根目录标识
├── config.yaml             # 配置文件
├── requirements.txt        # 项目依赖文件
├── report                  # 测试报告存放文件夹
├── api                     # api定义包
│   ├── __init__.py
│   ├── demo.py
│   └── ...
├── common                  # 通用工具包
│   ├── __init__.py
│   ├── assert_tools.py
│   └── ...
├── db                      # db包
│   ├── __init__.py
│   └── ...
└── test_suites             # 测试用例包
    ├── __init__.py
    ├── test_book_list.py
    ├── test_login.py
    └── ...
```
## 二、环境安装
```shell script
pip install -r requirements.txt
```

## 三、使用说明

### 2、运行单个用例
我们统一使用pytest单测框架，首先我们配置一下IDE，这里假设你使用的是widows版本pycharm,打开 ``File -> Setting -> Tools -> Python Integrated Tools``

在出现的界面中找到``Testing``，然后在``Default test runner``选项选择``pytest``，配置完成后，再打开测试用例文件(test_suites/test_login)，查看测试用例(类的方法)，左侧有绿色的按钮，点击即可运行

### 3、运行项目用例
在项目根目录下执行如下命令
```shell script
chargespot run
```

### 4、配置文件说明
配置文件名约定为``config``，可以使用``ini``、``json``、``yaml``，优先级为：``yaml > json > ini``

如果是多环境的话，可以在后面加上环境名，如``config-test.yaml``，需要有``.chargespot``中写入test标识，测试环境的配置大于默认配置，如有同名参数，测试环境配置会覆盖默认环境配置

所有配置加载完之后会放到变量``v``里，可以通过``[]``或``()``取值，如下示例：

假设有配置如下
```yaml
app:
  host: http://127.0.0.1:5000

user:
  account: admin@admin.com
  password: 111111

```
则可通过如下代码获取配置

```python
from chargespot import v

account = v['user.account'] # 通过[]取值
password = v('user.password') # 通过()取值

```