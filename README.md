![Static Badge](https://img.shields.io/badge/rasa-3.5-blue)
![Static Badge](https://img.shields.io/badge/python-3.8-orange)

# 训练

`rasa train --domain domain`

## 多线程训练

`rasa train --domain domain --num-threads 12`

# 开启 action 服务器

`rasa run actions`

# 使用

`rasa shell`

# 其他命令

### 查看模型从文本中提取的意图和实体

`rasa shell nlu`

### 交互式对话

`rasa interactive --domain domain`

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

# 简单前端界面

`python server/start_services.py `

功能多一点的：[rasa 简易前端](https://github.com/lyirs/rasa_web)
