# 训练

`rasa train --domain domain`

# 使用

`rasa shell`

# 验证数据

`rasa data validate`

# 拆分 nlu 数据

`rasa data split nlu`

# 测试数据集

`rasa test nlu --nlu train_test_split/test_data.yml`

# 交叉验证测试数据集

`rasa test nlu --nlu data/nlu.yml --cross-validation`

# 对比 nlu 管道

`rasa test nlu --nlu data/nlu.yml --config config_1.yml config_2.yml`

# 开启 api 服务器

`rasa run --enable-api --cors "*" --debug`

# 查看 DIET 训练日志

`tensorboard --logdir ./log `

# 简单前端界面

`python server/start_services.py `
功能多一点的：[Title](https://github.com/lyirs/rasa_web)
