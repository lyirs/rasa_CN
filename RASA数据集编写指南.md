# RASA 训练数据集使用指南

## 一、基础使用

### 1.自然语言理解（NLU）文件

nlu 文件是实体识别和意图识别两个任务的基石，在这个文件中，我们需要定义一些规则和示例，帮助机器人识别用户的意图（用户想要做什么）和实体（用户提到的关键信息）。

举个例子，假设你正在与一个旅游预订的聊天系统交流。当你说：“我想订明天去巴黎的机票。”时，NLU 文件就会帮助机器人识别你的意图是预订机票，同时捕捉到实体：明天（时间）和巴黎（目的地）。然后，系统就能为你提供相应的信息或服务。

#### _示例 nlu.yml_

```
# nlu文件
version: "3.1"

nlu:
- intent: greet
  examples: |
    - 你好
    - 你好啊
    - 早上好
    - 晚上好
- intent: goodbye
  examples: |
    - goodbye
    - bye
    - bye bye
    - 88
```

#### 需要注意的点：

- 严格遵循缩进规则进行对齐。否则将破坏 yml 文件的正确性。 [验证 yml 文件工具](https://yamlchecker.com/)
- *intent*键代表了意图，必须使用英文
- *examples*键中包含了上述意图可能的用户输入，输入语句以-开头，后面紧跟一个空格，再之后为输入
- yml 文件中以#开头的一行为注释行，不参与训练

### 2.域（domain）文件

域文件可以看作是一个蓝图或者地图，它为聊天机器人提供了整体的架构和范围。它包含了机器人需要了解和使用的所有信息，以便根据用户输入进行恰当的回应。

_示例 domain.yml_

```
version: "3.1"

intents:
  - greet
  - goodbye

responses:
  utter_greet:
    - text: Hey! How are you?
    - text: Hello!
  utter_goodbye:
    - text: 再见~
    - text: 拜拜~
  utter_default:
    - text: 没有听懂~

session_config:
  session_expiration_time: 60
  carry_over_slots_to_new_session: true

```

在域（domain）文件中，需要以下几类重要信息：

- Intents（意图）：这是一个列表，包含了所有用户可能表达的需求。例如，查询天气、订购披萨等。
- Entities（实体）：这是用户输入中可能包含的重要信息，如地点、日期等。实体帮助机器人提取关键数据以便进行更精确的响应。这里暂且不谈。
- Slots（槽位）：槽位可以看作是机器人的记忆单元，用于存储实体等关键信息。这些信息可以在后续对话中使用，以提供个性化和上下文相关的回应。这里暂且不谈。
- Actions（动作）：这是一个列表，包含了机器人可能采取的回应行为。动作可以是简单的文本回复，也可以是执行复杂任务，如查询数据库、调用 API 等。这里暂且不谈。
- Responses（响应）：这是一个预定义的回复模板库，用于在特定情况下生成机器人的文本回应。可以包括变量，如用户的名字或其他关键信息，以便创建个性化的回答。
- Forms（表单）：表单用于引导用户提供完整和详细的信息，以完成特定任务。例如，在订购披萨的过程中，表单可以收集用户关于披萨类型、尺寸、送货地址等的选择。这里暂且不谈。

**对于一个基础的聊天系统，我们只需关注 intents 与 responses 两个键。**

#### 需要注意的点：

- 严格遵循缩进规则进行对齐。
- 每一个在 nlu.yml 文件中定义的意图均需包含在 intents 键中。
- responses 键每一种意图回复以 **_utter\__** 开头，并且严格对应意图，例如在 nlu 文件中定义的意图 greet，回复中键就是 utter_greet
- responses 键每一种意图可以包含多个回复，系统会随机选取一个进行回复。
- utter_default 键表示了当用户的消息没有检测到对应的意图时系统的回复。
- 回复可以是图片，格式如下：

```
  utter_cheer_up:
  - image: https://i.imgur.com/nGF1K8f.jpg
    text: "Here is something to cheer you up:"
```

## 二、FAQ 型任务配置

多数对话系统都需要简单的 FAQ（常见问题解答）和 chitchat（闲聊）功能，而不用关注上下文，在一般情况下，FAQ 的问答数量众多，如果想用一个意图来表示一个 FAQ 并为之配备对应的动作组件，那么故事写起来会非常繁琐。对此，这里提供了更加简单的配置手段。

### 1.定义用户问题

#### _示例 nlu.yml_

```
version: "3.1"

nlu:
- intent: chitchat/ask_name
  examples: |
    - 你是谁？
    - 你叫啥？
- intent: chitchat/ask_weather
  examples: |
    - 你那里天气如何？
    - 天气怎么样？
```

可以看出，训练数据除了意图名称具有独特的格式（group/intent）外，其余部分与普通意图的训练格式完全一致。

上例中的意图 chitchat/ask_name 与 chitchat/ask_weather 均属于检索意图 chitchat

### 2.定义用户答案

对于 FAQ，我们可以直接使用 responses 文件来定义回复。

#### _示例 responses.yml_

```
version: "3.1"

responses:
  utter_chitchat/ask_name:
    - text: 我的名字是XXX。
  utter_chitchat/ask_weather:
    - text: 天气很好。
    - text: 天气很不错。
```

同时需要定义一个 rules 文件，包含对应的名字（rule 键，可以使用中文），步骤以及步骤中相应的检索意图 intent 键（group/intent 中的 group，这里为**chitchat**）以及对应的回复 action 键（以**utter\_**开头，这里为**utter_chitchat**）：

#### _示例 rules.yml_

```
version: "3.1"

rules:

- rule: respond to FAQs
  steps:
  - intent: chitchat
  - action: utter_chitchat
```

这个时候，域（domain）文件包含对应的检索意图（group/intent 中的 group，这里为**chitchat**），以及对应的动作（以**respond\_**开头，这里为**respond_chitchat**）格式应如下：

```
version: "3.1"

intents:
  - chitchat

actions:
  - respond_chitchat
```

### 3.例子

这里提供了一个完整的 FAQ 例子。

- 首先是 nlu 文件

#### _示例 travel_nlu.yml_

```
version: "3.1"

nlu:
# 周边景点
- intent: travel/surrounging_scenic_spots
  examples: |
    - 神武门周边都有哪些好玩的地方啊？
    - 东岳庙周边有其他景点吗？
# 游玩时间
- intent: travel/time_to_visit
  examples: |
    - 知道东岳庙可以玩多久不？
    - 你好，可以帮我查一下东岳庙能玩多久吗？
```

- 对应的规则（rules）文件

#### _示例 travel_rules.yml_

```
version: "3.1"

rules:

- rule: respond to FAQs
  steps:
  - intent: travel
  - action: utter_travel
```

- 对应的域（domain）文件

#### _示例 travel_domain.yml_

```
version: "3.1"

intents:
  - travel

actions:
  - respond_travel
```

## 三、上下文联系

在聊天系统的使用场景中，很多情况下对话是多轮次的，并且其中可能会穿插别的会话，所以需要一种方法记忆用户之前对话的信息。

### 1.nlu 中的实体识别

在 nlu 文件的 example 键，可以通过[ ]标注实体。

#### _示例 travel_nlu.yml_

```
version: "3.1"

nlu:
# 景点信息
- intent: information
  examples: |
    - 对[百雅轩798艺术中心](location_slot)有了解吗
    - 你知道[百雅轩798艺术中心](location_slot)吗
    - 知道[排云殿](location_slot)吗
    - 知道[排云殿](location_slot)吗？
```

上述例子中，通过[ ]标记了名为 location_slot 的实体。当用户提问“知道排云殿吗”时，系统就会提取出“排云殿”并将其存储在实体“location_slot”中。

#### _示例 express_nlu.yml_

```
version: "3.1"

nlu:
- intent: search_express
  examples: |
    - 快递
    - 查询快递
    - 帮我查快递信息
    - 我想知道[中通](express)快递的信息
    - 查下[顺丰](express)快递到哪里了
    - 帮我差下[中通](express)快递
```

上述例子中，通过[ ]标记了名为 express 的实体。

### 2.在域文件中定义词槽

#### _示例 travel_domain.yml_

```
version: '3.1'

intents:
  - information

entities:
  - location_slot

slots:
  location_slot:
    type: text
    initial_value: null
    influence_conversation: true
    mappings:
    - type: from_entity
      entity: location_slot

responses:
  utter_information:
    - text: "有些了解，{location_slot}位于北京798艺术区，创办于2003年。"
    - text: "嗯，{location_slot}曾经是718联合厂（798前身）的公共大食堂和活动礼堂。"

session_config:
  session_expiration_time: 60
  carry_over_slots_to_new_session: true

```

对比前面的域文件，可以看出来这里新增了两个键：entities 与 slots。

entities 即实体，在 nlu 文件中我们已经用[ ]进行标注，在这个键中，我们需要提供所有的实体名称，注意，实体名称只能为英文。

词槽（slots）定义了系统在对话过程中需要跟踪（记忆）的信息。这是系统理解上下文信息的基础保障。

在 slots 键中，第一行就是词槽的名称，一般与对应的实体名相同，这里为 location_slot，之后，type 定义了词槽的类型，这里为 text（文本）。

- text：存储文本值，适合作为通用实体的存储
- bool：只存储 true 或 false 的值，适合作为信号处理（如抢票是否成功）
- category：只能存储指定的有限个值，如性别情况
- float：存储浮点数
- list：存储多个任意值
- any：存储值对动作预测无影响，用于存放一些无关系统运行状态的值

initial_value 代表了词槽的初始值， mappings（映射）指定了在对话过程中如何自动地为这个词槽赋值，一个词槽可以有多个映射，在每一个映射中，type 给出了这个词槽的类型，其余键为这个类型的参数。上述例子中，只有一个映射，这个映射的 type 为 from_entity，表示将读取某个实体的值来赋值词槽，具体使用哪个实体，将由参数 entity 决定，这里为 location_slot。

在 responses 键中，我们就可以使用词槽来讲之前提供的实体嵌入回复中，注意，这里使用的是{ }，在训练数据后，系统接收用户问题并为词槽赋值后，会自动替换回复中对应的值。

#### 需要注意的点：

- responses 键中的回复可以不用引号框起，但是，如果使用了{词槽}则必须使用，并且为英文英号（半角引号）。

## 四、故事（stories）

Rasa 通过学习故事的方式来学习对话管理知识。

故事是一种在较高语义层次上记录对话过程的方式，不仅需要记录用户的语义表达，还需要记录系统内部正确的状态变化。
下面是一个故事示例：

```
用户：hello
系统：Hey! How are you?
```

#### _示例 stories.yml_

```
version: "3.1"

stories:
  - story: happy path
    steps:
      - intent: greet
      - action: utter_greet
```

- 故事本身的结构是字典，必须有 story 与 steps 键。
- story 键给出了故事的名称或者说备注，可以使用中文。
- 故事的主体存储在 steps 键对应的内容中，通过列表线性地表示用户和机器人之间的交互。

### 1. 动作

在训练和测试对话管理系统时，Rasa 并不会真正地执行相关的动作，所以无法获得动作运行的结果（也就是事件）是什么，需要在故事中明确给出。动作部分可以分为机器人动作名与动作返回事件。

- 机器人动作名： 在上例中 action: utter_greet 就是机器人动作名
  - 对于复杂的故事，可能在用户请求一次后系统连续执行多个动作的情况，

```
用户：你好
系统：你好啊
系统：你是谁？
```

#### _示例 stories.yml_

```
version: "3.1"

stories:
  - story: happy path
    steps:
      - intent: greet
      - action: utter_greet
      - action: utter_ask_name
```

- 动作返回事件
  - 常见事件包括词槽事件和 active_loop 事件
  - 词槽事件就是能对词槽状态进行更改的事件
  - active_loop 事件主要负责激活和取消激活表单（form），这些将在之后的内容介绍

### 2. 检查点符号

检查点（checkpoint）用于减少故事中的重复部分，名字相同的检查点之间可以互相跳转。

#### _示例 story.yml_

```
version: "3.1"

stories:
  - story: 流程开始
    steps:
      - intent: greet
      - action: action_ask_user_question
      - checkpoint: check_asked_question

  - story: 处理用户确认
    steps:
      - checkpoint: check_asked_question
      - intent: affirm
      - action: action_handle_affirmation
      - checkpoint: check_flow_finished

  - story: 处理用户否认
    steps:
      - checkpoint: check_asked_question
      - intent: deny
      - action: action_handle_denial
      - checkpoint: check_flow_finished

  - story: 流程完成
    steps:
      - checkpoint: check_flow_finished
      - intent: goodbye
      - action: utter_goodbye
```

一个故事结束时的检查点可以和另一个故事开始时的名字相同的检查点连接，形成新的故事。上例中，“流程开始”可以通过检查点“check_asked_question”与“处理用户确认”、“处理用户否认”两个故事连接起来，这两个故事又可以通过“check_flow_finished”与“流程完成”故事连接，形成新的故事。

- 使用检查点可以有效减少类似情节的重复编写
- 过多使用检查点会导致故事可读性变差或逻辑混乱

### 3. or

or 语句可以用于精简故事。

#### _示例 stories.yml_

```
version: "3.1"

stories:
  - story: or示例
    steps:
      - intent: ask_confirm
      - action: utter_ask_confirm
      - or:
        - intent: affirm
        - intent：thankyou
      - action: action_handle_affirmation
```

上面的例子通过 or 构造了两个故事，两个故事绝大部分相同，仅有的区别是其中一个步骤用户的意图不一致。

#### 需要注意的点：

- FAQ 系统中不需要配置故事，这部分功能由规则（rules）代替，见第二节。

## 五、规则（rules）

rules 文件是一个 Rasa 的一个重要组成部分，它用于定义对话管理的一些固定模式，以确保在特定情况下，对话按预期进行，在之前的 FAQ 系统中，我们已经接触过这个文件。
使用 rules 文件有以下几个主要目的：

- 明确的对话路径：Rules 允许您为特定场景定义明确的对话路径，以确保在某些情况下聊天机器人始终提供正确且一致的响应。
- 自动操作触发：您可以使用 Rules 触发特定操作，如槽填充、外部 API 调用或执行自定义动作。
- 指南对话：Rules 可以确保对话按照预期的顺序进行，从而遵循特定的对话逻辑。
  以下是一个简单的 rules 文件示例：

#### _示例 rules.yml_

```
version: "3.1"
rules:
- rule: Greet user
  steps:
  - intent: greet
  - action: utter_greet

- rule: Say goodbye
  steps:
  - intent: goodbye
  - action: utter_goodbye

- rule: Handle user information form
  steps:
  - intent: provide_user_information
  - action: user_information_form
  - active_loop: user_information_form

- rule: Close user information form
  condition:
  - active_loop: user_information_form
  steps:
  - action: user_information_form
  - active_loop: null
  - action: utter_thanks_for_user_information
```

在这个例子中，我们定义了四条规则：

1.当用户问候时（意图为 greet），回复问候（动作为 utter_greet）。

2.当用户告别时（意图为 goodbye），回复告别（动作为 utter_goodbye）。

3.当用户提供个人信息时（意图为 provide_user_information），激活用户信息表单（动作为 user_information_form，并将表单设为活跃循环）。

4.当用户信息表单完成时，关闭表单（将活跃循环设为 null），并感谢用户提供信息（动作为 utter_thanks_for_user_information）。

在 rasa 中，规则与故事都适用于定义和训练对话管理器的方法，描述了在不同场景下聊天系统应如何与用户互动，然而，它们之间存在一些关键区别：

- 规则（Rules）：
  - 规则描述了在特定情况下应始终遵循的对话路径。当满足规则中定义的条件时，聊天机器人将始终按照规则执行。
  - 规则主要用于处理固定对话逻辑，如问候、告别、槽填充、触发自定义动作等。
  - 规则不涉及预测，因此它们不会影响到机器人的对话策略学习。
  - 规则适用于需要确保一致性和精确控制的场景。
- 故事（Stories）： - 故事提供了用户和聊天机器人之间的典型对话示例。它们用于训练对话管理器，以便在实际对话中预测下一步的最佳动作。 - 故事包含一系列用户意图和聊天机器人响应，描述了不同场景和上下文下可能的对话路径。 - 故事用于训练对话策略，通过这些示例，机器人可以学习如何根据当前对话状态选择最佳动作。 - 故事适用于需要更多灵活性和泛化能力的场景。
  总之，规则和故事在 Rasa 中具有不同的作用。规则用于定义固定的对话路径，确保特定场景下的一致响应；而故事提供了典型对话示例，用于训练聊天机器人的对话策略。在实际项目中，通常需要结合使用规则和故事，以实现准确、灵活且可扩展的对话管理。

## 六、进阶：动作（action）

### 1. 回复动作

回复动作与域文件中的回复（response）关联在一起，以 **utter\_** 开头。

### 2. 表单

表单（form）是一种结构化的对话管理机制，用于从用户那里收集一系列相关的信息。表单通常用于处理涉及多个输入信息的任务，如预订、注册或填写调查问卷等。当使用表单时，聊天机器人会引导用户按顺序提供所需的信息，直到收集齐所有必要的数据。

表单的工作原理如下：

1.激活表单：当用户触发某个与表单相关的意图（intent）时，表单会被激活。例如，当用户表达预订餐厅的意图时，一个预订餐厅的表单就可以被激活。

2.填充槽（slots）：表单中定义了一组需要收集的槽。当表单被激活时，Rasa 会逐个询问用户以填充这些槽。用户的回答会被提取并存储在对应的槽中。

3.验证：在某些情况下，用户提供的信息可能需要验证。例如，确保用户输入的电子邮件地址是有效的。你可以为表单定义自定义验证逻辑，对用户提供的信息进行检查，并在验证失败时提示用户重新输入。

4.提交：当所有槽都被成功填充和验证后，表单会执行一个提交操作。通常，在这个阶段，你可以调用自定义动作（action）来处理收集到的数据，如预订餐厅或发送电子邮件等。

#### （1）定义表单

#### _示例 domain.yml_

```
version: "3.1"

intents:
  - search_express

entities:
  - express
  - number

slots:
  express:
    type: text
    initial_value: null
    influence_conversation: true
    mappings:
    - type: from_entity
      entity: express
  number:
    type: text
    initial_value: null
    influence_conversation: true
    mappings:
    - type: from_entity
      entity: number

responses:
  utter_ask_express:
    - text: 请输入需要查询的快递公司,目前只支持顺丰,中通,圆通
  utter_ask_number:
    - text: 请输入要查询的{express}快递单号
  utter_search_stop_number:
    - text: 关于{express}快递单号{number}查找结束。

actions:
  - action_search_express

forms:
  action_search_express_form:
    required_slots:
      - express
      - number
```

在域文件中，我们可以看出新增了一个键：forms，用于定义表单。表单的名称为“action_search_express_form”，注意不能为中文。
在上面的例子中，我们规定为了完成这个表单，有两个必须的词槽：express 与 number

#### （2）激活表单

当表单要求的词槽全部获得时，就可以执行表单任务了，这个在规则文件中设定。

#### _示例 rules.yml_

```
version: "3.1"

rules:
- rule: Activate express Form
  steps:
  - intent: search_express
  - action: action_search_express_form
  - active_loop: action_search_express_form

- rule: Submit express form
  condition:
    - active_loop: action_search_express_form
  steps:
  - action: action_search_express_form
  - active_loop: null
  - slot_was_set:
    - requested_slot: null
  - action: action_search_express
  - action: utter_search_stop_number
```

这个 Rasa 规则文件包含了两个规则，分别用于激活表单和提交表单。

- 第一个表单：
  - \- rule: Activate express Form：定义一个名为"Activate express Form"的规则，用于激活表单。
  - steps:规定该规则包含的步骤序列。
  - \- intent: search_express：当用户表示"search_express"意图时，触发该规则。
  - \- action: action_search_express_form：执行名为"action_search_express_form"的自定义表单动作,这个动作我们已经在域文件中定义。
  - \- active_loop: action_search_express_form：激活名为"action_search_express_form"的表单循环，开始收集用户信息。
- 第二个表单： - \- rule: Submit express form：定义一个名为"Submit express form"的规则，用于提交表单。 - condition:定义触发该规则所需满足的条件。 - \- active_loop: action_search_express_form：当名为"action_search_express_form"的表单处于活跃状态时，满足该条件。 - steps:规定该规则包含的步骤序列。 - \- action: action_search_express_form：执行名为"action_search_express_form"的自定义表单动作 - \- active_loop: null：结束名为"action_search_express_form"的表单循环。 - \-slot_was_set: 表示一个槽的值被设置。 - \- requested_slot: null：将"requested_slot"设置为 null，表示表单已完成，不再请求更多信息。 - \-action: action_search_express：执行名为"action_search_express"的动作，通常是一个自定义动作，用于处理收集到的表单数据。 - \-action: utter_search_stop_numberinfo：执行名为"utter_search_stop_numberinfo"的动作，通常是一个预定义的回复模板，向用户提供快递查询结果或相关信息。
  总的来说，就是在激活表单规则中，我们激活了“action_search_express_form”这个表单，进入对应的填槽-询问循环过程（active_loop），一旦当所有词槽提供完成（active_loop: null，requested_slot: null），执行对应动作。前文已经说过，词槽的提供来源于用户语句中的实体。

注意三点：

- 表单动作事件（例如 - action: action_search_express_form）在第一次启动表单时被使用，也在表单已经激活时恢复表单动作时被使用。
- 一个表单激活事件（例如 - active_loop: action_search_express_form）紧随第一个表单动作事件之后使用。
- 一个表单停用事件（例如 - active_loop: null），用于停用表单。

#### _示例 nlu.yml_

```
version: "3.1"

nlu:
- intent: search_express
  examples: |
    - 帮我查个快递
    - 查快递
    - 查下快递
    - 我要查快递
    - 看下快递
    - 快递
    - 查询快递
    - 帮我查快递信息
    - 我想知道[中通](express)快递的信息
    - 查下[顺丰](express)快递到哪里了
    - 帮我差下[中通](express)快递
    - 我想查询[圆通](express)快递,单号[YT9372128558055](number)
    - 帮我查下单号为[YT5078273557325](number)的[圆通](express)快递
    - 我需要知道单号[YT5075532844265](number)的[圆通](express)
```

- 如果用户提问 “帮我查个快递” ，触发意图“search*express”，激活表单，但这里并没有提供 express 与 number 两个实体的值，所以系统会继续提问，当表单的词槽没有被满足时，Rasa 会使用提问模板（\*\*\*utter_ask***_）向用户提问以获取相应信息。提问模板通常在 domain.yml 文件中的 responses 部分定义，表单中的每个词槽都应该有一个与之关联的提问模板。提问模板的命名约定是 _**utter*ask*{slot_name}**_，其中 _**{slot_name}\*\*\*是对应词槽的名称。

```
responses:
  utter_ask_express:
    - text: 请输入需要查询的快递公司,目前只支持顺丰,中通,圆通
  utter_ask_number:
    - text: 请输入要查询的{express}快递单号
  utter_search_stop_number:
    - text: 关于{express}快递单号{number}查找结束。
```

当表单激活时，如果某个词槽没有被填充，Rasa 会根据提问模板自动询问用户以获取相应信息。在收集到用户回答后，Rasa 会将提取的实体值存储在对应的词槽中，然后继续处理表单中的其他词槽。如果所有词槽都已填充，表单会结束，并执行相应的操作。

综上，完成一个表单，在数据集方面至少需要完善以下几个文件：

- nlu 用于提供实体的标注
- rules 用于规定表单流程
- domain 用于定义提问模板与定义表单
  当然，我们也可以定义故事，以下是个故事示例：

```
用户： 我想查询中通快递,单号75416807218275。
系统： 时间：2023-03-22 物料状态： .....
```

对应的故事为：

#### _示例 stories.yml_

```
version: "3.1"
stories:
- story: interactive_story_1
  steps:
  - intent: search_express
    entities:
    - express: 中通
    - number: '75416807218275'
  - slot_was_set:
    - express: 中通
  - slot_was_set:
    - number: '75416807218275'
  - action: action_search_express_form
  - active_loop: action_search_express_form
  - slot_was_set:
    - express: 中通
  - slot_was_set:
    - number: '75416807218275'
  - slot_was_set:
    - requested_slot: null
  - active_loop: null
  - action: action_search_express
  - action: utter_search_stop_number
```

### 3. 默认动作

Rasa 提供的默认动作，例如：

- action_listen 停止预测动作，等待用户输入
- action_restart 重启对话过程，清理对话历史与词槽
- action_deactivate_loop 停止当前已经激活的 active_loop，并重置 requested_slot 词槽
- action_two_stage_fallback 处理 nlu 得分较低时触发的 fallback 逻辑
- action_default_ask_affirmation 被 action_two_stage_fallback 使用，要求用户确认他们的意图
- action_default_ask_rephrase 被 action_two_stage_fallback 使用，要求用户重新表述
  默认动作可以被同名自定义动作替代。

### 4. 自定义动作

利用 python 满足各种后端交互与计算需求。

## 七、同义词（synonym）与查找表（lookup）

- 在 Rasa NLU 文件中，可以使用 synonym 来定义不同表达方式的实体在处理时具有相同的含义。这在实际对话场景中非常有用，因为用户可能使用不同的术语来表达相同的意思。通过使用 synonym，可以将这些不同的表达方式映射到一个统一的表示。
- 查找表主要用于帮助 Rasa 识别某一类实体中的特定值。查找表通常用于处理具有大量预定义值的实体，例如地名、产品名称等。查找表可以帮助 Rasa 更准确地识别这些实体，尤其是在它们的形式相似或有规律可循时。

#### _示例 nlu.yml_

```
version: "3.1"

nlu:
- intent: search_express
  examples: |
    - 帮我查个快递
    - [中通](express)快递单号为[75417089889012](number)
    - [中通](express)快递
    - [顺丰](express)
    - 查询[顺丰](express)快递信息,[SF1102336663230](number)
    - [顺丰](express)单号[SF1406050054883](number)

- synonym: 顺丰
  examples: |
    - 顺丰
    - 顺丰快递
    - shunfeng
- synonym: 圆通
  examples: |
    - 圆通
    - 圆通快递
- synonym: 中通
  examples: |
    - 中通
    - 中通快递

- lookup: express
  examples: |
    - 顺丰
    - 中通
    - 圆通
```

## 八、实体分组

在 Rasa 中，实体分组（entities group）是一种处理实体层次结构的方法。有些情况会出现多组实体，每组实体描述一个子任务，这个时候就需要细分词体。
例如，在车票订票系统中：

#### _示例 nlu.yml_

```
# nlu文件
version: "3.1"

nlu:
- intent: ticket
  examples: |
    - 帮我订一张[北京](city)到[上海](city)的机票
```

上例中，北京与上海都会被识别为类型为“city”的实体，但并不清楚每个实体的语义角色：“出发地”还是“目的地”

当然可以通过标注不同的实体名称来避免这种情况：

#### _示例 nlu.yml_

```
# nlu文件
version: "3.1"

nlu:
- intent: ticket
  examples: |
    - 帮我订一张[北京](departure)到[上海](destination)的机票
```

但相似的实体太多会导致逻辑混乱等问题。

rasa 提供了实体分组这一特性来解决这一问题。

#### _示例 nlu.yml_

```
# nlu文件
version: "3.1"

nlu:
- intent: ticket
  examples: |
    - 帮我订一张[北京]{"entity": "city", "role": "departure"}到[上海]{"entity": "city", "role": "destination"}的机票
```

这个时候，域文件的相应词槽定义如下:

#### _示例 domain.yml_

```
···
entities:
   - city:
       roles:
       - departure
       - destination

slots:
  departure:
    type: text
    mappings:
    - type: from_entity
      entity: city
      role: departure
  destination:
    type: text
    mappings:
    - type: from_entity
      entity: city
      role: destination
···
```

还可以通过在实体标签旁边指定组标签来对不同的实体进行分组。例如，组标签可用于定义不同的订单。在下面的示例中，组标签指定了哪些配料与哪些比萨饼搭配，以及每个比萨饼的大小：

#### _示例 nlu.yml_

```
# nlu文件
version: "3.1"

nlu:
- intent: ticket
  examples: |
    - 给我一份[小份]{"entity": "size", "group": "1"}[蘑菇]{"entity": "topping", "group": "1"}披萨以及一份[大份]{"entity": "size", "group": "2"}[香肠]{"entity": "topping", "group": "2"}披萨
```

---

---

以上就是关于数据集的编写基础指南，总的来说，一套完整的数据集应包括 nlu、stories、rules、domain，加上 FAQ 使用的 responses 五种文件，格式均为 yml，以下是其他可能需要注意到的点：

- 除了上述提到的允许使用中文的情况，一律使用英文，
- 出去 intent 中的示例，以及 responses 或 domain 中的回复中，中文表达可以正常使用中文符号外，所有的标点符号均应为英文格式下的符号（半角）。
- 意图的划分应尽量准确，避免相似表达映射到不同的意图上。
- 意图的命名可以使用\_连接单词，来追求更准确地表达。
- 不涉及多轮对话的，尽量使用 FAQ 形式构建。
- 数据集中缺少多样的语言表达可能会降低模型的泛化能力，尽可能多考虑潜在的用户语言表达形式。
- 避免只种事单个句子的理解和生成，对话的整体流程与自然性同样重要，在编写回复与故事、规则的时候注意。
