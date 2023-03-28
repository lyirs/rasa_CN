# 验证数据
`rasa data validate`

# 拆分nlu数据
`rasa data split nlu`

# 测试数据集
`rasa test nlu --nlu train_test_split/test_data.yml`

# 交叉验证测试数据集
`rasa test nlu --nlu data/nlu.yml --cross-validation`

# 对比nlu管道
`rasa test nlu --nlu data/nlu.yml --config config_1.yml config_2.yml`

# 训练多个domain文件
`rasa train --domain domain`

# 开启 api 服务器
`rasa run --enable-api --cors "*" --debug`