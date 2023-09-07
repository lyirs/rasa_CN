<h1 align="center">基于RASA的中文任务型机器人</h1>
<div align="center">

[![Static Badge](https://img.shields.io/badge/rasa-3.6-blue)](https://github.com/RasaHQ/rasa)
![Static Badge](https://img.shields.io/badge/python-3.8-orange)

</div>

<div align="center">

2022/6/8 后 rasa-x 不再免费 直接安装 rasa 即可

</div>

<hr />

<h3 align="center">

💡 **文件说明** 💡

</h3>

| 文件         | 描述                                                                                     |
| ------------ | ---------------------------------------------------------------------------------------- |
| actions      | 自定义动作服务器                                                                         |
| components   | 自定义组件                                                                               |
| data/nlu     | Rasa NLU 的训练数据                                                                      |
| data/rules   | Rasa 规则数据                                                                            |
| data/stories | Rasa 故事数据                                                                            |
| domain       | 领域指定了 rasa 应该知道的意图、实体、插槽、响应、表单和动作。它还定义了会话会话的配置。 |
| models       | 训练的模型数据                                                                           |
| pipline      | 流水线组件配置                                                                           |
| server       | 前后端服务                                                                               |
| source       | RASA 源代码，只是用来调试 DIET 的*(:з」∠)*                                               |
| .env         | 相关环境变量，主要用于 API                                                               |

<hr/>

<h3 align="center">

💡 **目前的功能** 💡

</h3>

| 功能   | 描述       | API 来源                               | 数据来源 |
| ------ | ---------- | -------------------------------------- | -------- |
| 闲聊   | 简易打招呼 |                                        | -        |
| 任务型 | 查询天气   | [心知天气](https://www.seniverse.com/) | -        |
| 任务型 | 查询快递   | [快递网](http://www.kuaidi.com/)       | -        |
| 任务型 | 查询车票   | [12306](https://kyfw.12306.cn/)        | smp2019  |
| 任务型 | 查询新闻   | [聚合](https://www.juhe.cn/)           | -        |
| 任务型 | 微博热搜   | [天行](https://www.tianapi.com/)       | -        |
| 任务型 | 今日头条   | [天行](https://www.tianapi.com/)       | -        |
| 任务型 | 查询汇率   | [聚合](https://www.juhe.cn/)           | -        |
| 任务型 | 食物营养   | [天行](https://www.tianapi.com/)       | -        |

<hr/>

<h3 align="center">

💡 **基本使用** 💡

</h3>

## 依赖安装

`pip install -r requirements.txt`

## 训练

`rasa train --domain domain`

### 多线程训练

`rasa train --domain domain --num-threads 12`

## 开启 action 服务器

`rasa run actions`

## 使用

`rasa shell`

<hr />

<h3 align="center">

💡 **其他命令** 💡

</h3>

### 查看模型从文本中提取的意图和实体

`rasa shell nlu`

### 交互式对话

`rasa interactive --domain domain`

### 故事可视化

`rasa visulize`

### 验证数据

`rasa data validate`

### 拆分 nlu 数据

`rasa data split nlu`

### 测试数据集

`rasa test nlu --nlu train_test_split/test_data.yml`

### 交叉验证测试数据集

`rasa test nlu --nlu data/nlu.yml --cross-validation`

### 对比 nlu 管道

`rasa test nlu --nlu data/nlu.yml --config config_1.yml config_2.yml`

### 开启 api 服务器

`rasa run --enable-api --cors "*" --debug`

### 查看 DIET 训练日志

`tensorboard --logdir ./log `

<hr />

<h3 align="center">

💡 **简单前端页面** 💡

</h3>

`python server/start_services.py `

功能多一点的：[rasa 简易前端](https://github.com/lyirs/rasa_web)

<hr />

<h3 align="center">

💡 **推荐使用 python 虚拟环境进行管理** 💡

</h3>

<div align="center">

[![Static Badge](https://img.shields.io/badge/Miniconda-blue)](https://conda.io/en/latest/miniconda.html)

</div>

### 创建 python 虚拟环境

`conda create -n py38_rasa python=3.8`

### 激活虚拟环境

`conda activate py38_rasa`

<hr />

<h3 align="center">

📚 **问题** 📚

</h3>

- 有些依赖库需要 Microsoft Visual C++ 14.0 以上的环境 可在 visual studio 中进行安装
  ,或使用 Microsoft C++ Build Tools [![Static Badge](https://img.shields.io/badge/visual_cpp_build_tools-blue)](https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/)

- 安装速渡过慢

```
pip install -i https://pypi.douban.com/simple module # 使用豆瓣源
pip install -i http://mirrors.aliyun.com/pypi/simple/ module # 阿里云
pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ module # 中国科技大
pip install -i http://pypi.douban.com/simple/ module # 豆瓣(douban)
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ module # 清华大学
pip install -i http://pypi.mirrors.ustc.edu.cn/simple/ module # 中国科学技术大学
```

- fatal: unable to access ‘https://github.com/xxx‘: OpenSSL SSL_connect: SSL_ERROR_SYSCALL in connecti-

```
git config --global --add remote.origin.proxy ""
git config --global http.sslBackend "openssl"
```

- ERROR:pip install xmlsec 安装失败

```
 × Building wheel for xmlsec (pyproject.toml) did not run successfully.
 │ exit code: 1
 ╰─> [13 lines of output]
     running bdist_wheel
     running build
     running build_py
     creating build
     creating build/lib.linux-x86_64-cpython-38
     creating build/lib.linux-x86_64-cpython-38/xmlsec
     copying src/xmlsec/py.typed -> build/lib.linux-x86_64-cpython-38/xmlsec
     copying src/xmlsec/constants.pyi -> build/lib.linux-x86_64-cpython-38/xmlsec
     copying src/xmlsec/tree.pyi -> build/lib.linux-x86_64-cpython-38/xmlsec
     copying src/xmlsec/template.pyi -> build/lib.linux-x86_64-cpython-38/xmlsec
     copying src/xmlsec/__init__.pyi -> build/lib.linux-x86_64-cpython-38/xmlsec
     running build_ext
     error: xmlsec1 is not installed or not in path.
     [end of output]
    note: This error originates from a subprocess, and is likely not a problem with pip.
    ERROR: Failed building wheel for xmlsec
```

安装依赖库：

```
apt-get install -y libxml2-dev libxmlsec1-dev libxmlsec1-openssl
```

<h3 align="center">

💡 **Docker** 💡

</h3>

Dockerfire 参考:

```
FROM python:3.8.15
WORKDIR /rasa
COPY . /rasa
RUN apt-get update && \
    apt-get install -y libxml2-dev libxmlsec1-dev libxmlsec1-openssl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/ && \
    pip install \
    xmlsec==1.3.13 \
    tensorflow==2.12.0 \
    scikit_learn==1.1.3 \
    matplotlib==3.5.3 \
    protobuf==3.20.3 \
    -i http://mirrors.aliyun.com/pypi/simple/  --trusted-host mirrors.aliyun.com && \
    pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/  --trusted-host mirrors.aliyun.com
```

本仓库 docker 下载

```
docker push lyirs/rasa:1.0
docker run -it lyirs/rasa
```
