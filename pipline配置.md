1.如果想本地跑 LanguageModelFeaturizer，去下面网址下载 bert-base-chinese 模型，主要需要

config.json

pytorch_model.bin

tf_model.h5

tokenizer_config.json

vocab.txt

https://huggingface.co/bert-base-chinese

然后更改 pipline：

```
  - name: LanguageModelFeaturizer
    model_name: "bert"
    model_weights: "pipline/bert-base-chinese"
```

2.如果使用 Mitie 流程，请下载或自己训练 total_word_feature_extractor_zh.dat
然后 pipline 如下：

```
  - name: MitieNLP
    model: "pipline/total_word_feature_extractor_zh.dat"
  - name: JiebaTokenizer
    dictionary_path: "pipline/jieba_userdict"
  - name: MitieEntityExtractor
  - name: EntitySynonymMapper
  - name: RegexFeaturizer
  - name: MitieFeaturizer
  - name: DIETClassifier
    epochs: 100
  - name: DucklingEntityExtractor
    dimensions: ["number"]
  - name: ResponseSelector
    epochs: 100
  - name: FallbackClassifier
    threshold: 0.3
```

但个人觉得不如我调整好的这一套 pipline

3.稍做修改的 jieba 分词组件
在 rasa shell nlu 命令的输出中，可以显示词性标注的结果

为了实现这一功能，改用了 jieba.posseg

扩展 rasa.nlu.tokenizers.tokenizer.Token 类以添加一个新属性来存储词性信息。用于在输出中观察到词性标注信息

（本来想使用自定义消息类覆盖掉原有的 text tokens 字段，但失败了(:з」∠)\_）

分词组件是比较简单的自定义组件，可以照着官网的例子试着写写

使用：

```
  - name: components.jieba_tokenizer.JiebaTokenizer   #对应的文件夹.文件名.类名
    dictionary_path: "pipline/jieba_userdict"
```

23/5/17 更新：
在训练数据中如果有中英文混杂的情况，经常会报这个错误：

```
Node: 'gradient_tape/rasa_sequence_layer_text/rasa_feature_combining_layer_text/concatenate_sparse_dense_features_text_sequence/ConcatOffset'
All dimensions except 2 must match. Input 1 has shape [63 8 768] and doesn't match input 0 with shape [63 10 128].
         [[{{node gradient_tape/rasa_sequence_layer_text/rasa_feature_combining_layer_text/concatenate_sparse_dense_features_text_sequence/ConcatOffset}}]] [Op:__inference_train_function_56448]
```

来自 Rasa 的 Issue： https://github.com/RasaHQ/rasa/issues/7910

```
JiebaTokenizer is meant for Chinese only text. When multiple languages are used in the same sentence, the tokenizer adds an extra whitespace token in between two chinese and english tokens. For example,
text: 如何才能在下载和安装google app
Tokens output by the tokenizer will be: ['如何', '才能', '在', '下载', '和', '安装', ' ', 'google', 'app']
```

目前采用在 tokenize 中：在生成 Token 对象之前，先检查分词的结果是否只包含空格。如果是，那么就跳过这个分词，不生成对应的 Token 对象。然后，使用 find 方法来查找每个分词在原始文本中的实际位置，而不是简单地使用 jieba 分词器生成的位置。
这个解决方案仍然是一个折衷的方案，它可能无法处理所有的边缘情况。如果你发现这个解决方案仍然无法满足你的需求，那么你可能需要寻找一个更适合处理中英文混合文本的分词器，或者直接修改 jieba 分词器的源代码。
