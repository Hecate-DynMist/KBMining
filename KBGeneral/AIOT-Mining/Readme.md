# AIOT+地产+公共 KB Mining

本项目为KB数据挖掘项目。

- sametag.py 提取数据库新闻标题中所有包含地产和公共字段的新闻及其和KB匹配到关联的公司实体，提取和AIOT涉及技术词的新闻和其AIOT层级，提取关键词和标签共有的数据
- add.py 添加地产，公共和AIOT的发布时间，id信息，及其关联的技术领域和相关技术主体
- kbmatch.py 匹配新闻标题中出现过的kb中所有技术词条，添加相关信息并清理数据
- dist.py 根据时间维度统计技术领域分布和高频技术词汇分布