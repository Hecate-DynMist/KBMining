# KB Miner

## 技术主题

本项目通过机器之心kb数据库的关联挖掘，根据技术词提取机构及机构关联名录返回给用户。使用该项目需安装Neo4j，并导入机器之心的kb dump数据。

### Get Started

- 安装依赖

```
pip install -r requirements.txt
```

- 参数设置，在config.py上修改
```
base = pd.read_excel('./Inputs/Base.xlsx') # 输出技术词词源，填写词源本地路径。其中列名必须包含Key和Score，详情参照运行说明
graph = Graph("bolt://localhost:7687", user="neo4j",password="lene1111") # 输入本地neo4j数据库端口，用户名和密码，保持neo4j运行的状态。此外，neo4j数据库无密码时用户必须要设置密码。
# techbase以下两项二选一，没被选的注释掉。
techbase = base # 使用源技术词匹配
techbase = techexpand('n') # 根据kb技术词
```

- 主函数（四个）
=======
- 主函数（四个）在main.py上修改
>- 技术相关的机构及其关联：tech2institution(检索参数，输出属性参数，输出关联实体参数)
  - 技术相关的解决方案及其关联：tech2solution(检索参数，输出属性参数，输出关联实体参数)
  - 技术相关的应用案例及其关联：tech2businesscase(检索参数，输出属性参数，输出关联实体参数)
  - 技术相关的行业和智能领域分布：tech2IndustryAifield()
- 前三个主函数参数分为检索参数，输出属性参数和输出关联实体参数
- 脚本运行

```
python main.py
```

### **运行说明**

#### 输入文件格式要求

输入的 Base.xlsx 文件放在 input 目录中，并包含Key和Score两个字段（可在模板文件中直接保留第一行列名，将词和分数替换掉）。Key为客户提供的技术词，或分析师根据客户需求定制技术词，Score为技术词的权重。其中技术词若为英文则不区分大小写，如没提供Score的分数，则全填1，视为每个词权重一样。

#### 机构及其关联参数选择

调用函数为tech2institution（检索参数，输出属性参数，输出关联实体参数）。所有参数需严格按照表格提供的字段填写，大小写也是区分的。

| 检索参数              | 备注                                     | 检索方式                  |
| --------------------- | ---------------------------------------- | ------------------------- |
| summary               | 根据技术词与机构描述匹配结果             | 机构属性直接关联          |
| desc                  | 根据技术词与机构描述详细匹配结果         | 机构属性直接关联          |
| advantage_tech        | 根据机构-技术词的advantage_tech关系链路  | 机构技术词直接关联        |
| additional_info       | 根据机构-技术词的additional_info关系链路 | 机构技术词直接关联        |
| indexed_by            | 根据机构-技术领域的indexed_by关系链路    | 机构技术词直接关联        |
| Solution_summary      | 根据技术词-解决方案的描述-机构关联       | 解决方案属性一级关联      |
| Solution              | 根据技术词-解决方案-机构关联             | 解决方案一级关联          |
| BusinessCase          | 根据技术词-应用案例-机构关联             | 应用案例一级关联          |
| BusinessCase-Solution | 根据技术词-应用案例-解决方案-机构关联    | 应用案例-解决方案二级关联 |

输出参数为通过检索参数得出的机构列表进一步输出机构关联信息，其中属性参数为机构本身的属性，关联实体参数为机构所关联的其他实体。

属性参数。不需要输出任何属性则填'none'，只输出机构名。若需要输出机构相关属性，将'none'替换为以下属性参数或属性参数的组合：

- uuid：输出关联机构的uuid
- roles：输出关联机构的产业链角色
- founded_at：输出关联机构的成立时间
- core_member：输出关联机构的核心成员
- summary：输出关联机构的描述
- financing_round：输出关联机构的融资轮次

关联实体参数。不需要输出任何机构关联实体则填'none'，只输出机构名。若需要输出机构相关实体，将'none'替换为以下关联实体参数或关联实体参数的组合：

- Solution：输出相关机构及其关联的解决方案
- BusinessCase：输出相关机构及其关联的方案
- Scenario：输出相关机构及其关联的业务场景
- Industry：输出相关机构及其关联的行业
- AiField：输出相关机构及其关联的智能领域

调用函数为tech2institution。其中3项参数为均字符串，里面具体字段可以任意顺序组合，以逗号分隔。示例：tech2institution('BusinessCase-Solution,BusinessCase,Solution_summary', 'uuid,roles', 'Solution,BusinessCase')。

#### 解决方案及其关联参数选择

调用函数为tech2solution（检索参数，输出属性参数，输出关联实体参数）。所有参数需严格按照表格提供的字段填写，大小写也是区分的。

| 检索参数                 | 备注                                         | 检索方式               |
| ------------------------ | -------------------------------------------- | ---------------------- |
| summary                  | 根据技术词与解决方案描述匹配结果             | 解决方案属性直接关联   |
| desc                     | 根据技术词与解决方案描述详细匹配结果         | 解决方案属性直接关联   |
| core_tech                | 根据解决方案-技术词的advantage_tech关系链路  | 解决方案技术词直接关联 |
| serves                   | 根据解决方案-技术词的additional_info关系链路 | 解决方案技术词直接关联 |
| indexed_by               | 根据解决方案-技术领域的indexed_by关系链路    | 解决方案技术词直接关联 |
| Institution_summary      | 根据技术词-机构的描述-解决方案关联           | 机构属性一级关联       |
| Institution              | 根据技术词-机构-解决方案关联                 | 机构一级关联           |
| BusinessCases            | 根据技术词-方案-解决方案关联                 | 应用案例一级关联       |
| BusinessCase-Institution | 根据技术词-应用案例-机构-解决方案关联        | 应用案例-机构二级关联  |

输出参数为通过检索参数得出的解决方案列表进一步输出解决方案关联信息，其中属性参数为解决方案本身的属性，关联实体参数为解决方案所关联的其他实体。

属性参数。不需要输出任何属性则填'none'，只输出解决方案名。若需要输出解决方案相关属性，将'none'替换为以下属性参数或属性参数的组合：

- uuid：输出关联解决方案的uuid
- summary：输出关联解决方案的描述

关联实体参数。不需要输出任何机构关联实体则填'none'，只输出解决方案名。若需要输出解决方案相关实体，将'none'替换为以下关联实体参数或关联实体参数的组合：

- Institution：输出相关解决方案及其关联的机构
- BusinessCase：输出相关解决方案及其关联的应用案例
- Scenario：输出相关解决方案及其关联的业务场景
- Industry：输出相关解决方案及其关联的行业
- AiField：输出相关解决方案及其关联的智能领域

调用函数为tech2solution。其中3项参数为均字符串，里面具体字段可以任意顺序组合，以逗号分隔。示例：tech2solution('summary,serves,Institution_summary,Institution,BusinessCase', 'uuid','BusinessCase,Institution')

#### 应用案例及其关联参数选择

调用函数为tech2businesscase（检索参数，输出属性参数，输出关联实体参数）。所有参数需严格按照表格提供的字段填写，大小写也是区分的。

| 检索参数             | 备注                                         | 检索方式               |
| -------------------- | -------------------------------------------- | ---------------------- |
| core_tech            | 根据应用案例-技术词的core_tech关系链路       | 应用案例技术词直接关联 |
| applies_to           | 根据应用案例-技术词的applies_to关系链路      | 应用案例技术词直接关联 |
| additional_info      | 根据应用案例-技术词的additional_info关系链路 | 应用案例技术词直接关联 |
| indexed_by           | 根据应用案例-技术领域的indexed_by关系链路    | 应用案例技术词直接关联 |
| Institution_summary  | 根据技术词-机构的描述-应用案例关联           | 机构属性一级关联       |
| Solution_summary     | 根据技术词-解决方案的描述-应用案例关联       | 解决方案属性一级关联   |
| Solution             | 根据技术词-解决方案-应用案例关联             | 解决方案一级关联       |
| Institution          | 根据技术词-机构-应用案例关联                 | 机构一级关联           |
| Institution-Solution | 根据技术词-机构-解决方案-应用案例关联        | 机构-解决方案二级关联  |
| Solution-Institution | 根据技术词-解决方案-机构-应用案例关联        | 解决方案-机构二级关联  |

输出参数为通过检索参数得出的应用案例列表进一步输出应用案例关联信息，其中属性参数为应用案例本身的属性，关联实体参数为应用案例所关联的其他实体。

属性参数。不需要输出任何属性则填'none'，只输出应用案例名。若需要输出应用案例相关属性，将'none'替换为以下属性参数或属性参数的组合：

- uuid：输出关联解决方案的uuid

关联实体参数。不需要输出任何机构关联实体则填'none'，只输出解决方案名。若需要输出解决方案相关实体，将'none'替换为以下关联实体参数或关联实体参数的组合：

- Institution：输出相关应用案例及其关联的机构
- Solution：输出相关应用案例及其关联的解决方案
- Scenario：输出相关应用案例及其关联的业务场景
- Industry：输出相关应用案例及其关联的行业
- AiField：输出相关应用案例及其关联的智能领域

调用函数为tech2solution。其中3项参数为均字符串，里面具体字段可以任意顺序组合，以逗号分隔。示例：tech2businesscase('Institution_summary,core_tech,Solution_summary,Institution,Solution,Solution-Institution,Institution-Solution', 'uuid', 'Solution,Institution,Industry,AiField,Scenario')

#### 输出

输出文件在outputs文件夹，根据需输出的不同实体列表，文件名分别为Tech-Institution.xlsx、Tech-Solution.xlsx、Tech-BusinessCase.xlsx。输出文件包括一个总的结果和以技术词源分组的结果，对应sheet_name为‘all’和具体技术词名称。



## 行业和技术领域主题

该主题只需要调用index2entity(索引类别参数，索引名称参数，输出实体参数，关联实体参数)

#### 索引类别参数

- Industry：根据客户提供的行业进行索引
- TechField：根据客户提供的技术领域进行索引

索引名称参数为类别参数对应的具体名称，如Industry为地产

#### 输出实体参数

- Institution：输出和索引关联的机构
- Solution：输出和索引关联的解决方案
- BusinessCase：输出和索引关联的应用案例

#### 行业关联实体参数

- TechField：输出实体关联的技术领域
- Industry：输出实体关联的行业


行业索引示例：index2entity('Industry','地产,公共服务','Institution,Solution','TechField')；
技术领域索引示例：index2entity('TechField','元学习,物联网技术','Institution,BusinessCase','AiField,Industry')

#### 输出

输出文件在outputs文件夹，根据索引不同，如地产和公共服务的行业索引结果文件名为Industry(地产,公共服务).xlsx；元学习和物联网技术的技术领域索引结果的文件名为TechField(元学习,物联网技术).xlsx。



