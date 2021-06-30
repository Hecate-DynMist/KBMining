import time
import pandas as pd
from tqdm import tqdm
from collections import Counter
from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher


def init_neo4j():
    return Graph('http://localhost:7474', username='neo4j', password='4572')


def preprocess(item):
    if len(item) == 0:
        return None
    else:
        temp = []
        for i in item:
            for k, v in i.items():
                temp.append(v)
        temp = list(set(temp))
        return temp


def preprocess_2(item):
    temp = []
    if item:
        for i in item:
            for k, v in i.items():
                try:
                    for j in eval(str(v)):
                        temp.append(j)
                except:
                    pass
        temp = list(set(temp))
    return temp


def timestamp2str(timestamp):
    if timestamp:
        timeArray = time.localtime(timestamp)
        styledTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return styledTime[:4]


def 分析一():
    案例表 = pd.DataFrame()
    解决方案表 = pd.DataFrame()
    机构表 = pd.DataFrame()
    行业表 = pd.DataFrame()
    智能领域表 = pd.DataFrame()
    方案形态表 = pd.DataFrame()
    产业链角色表 = pd.DataFrame()
    成立年份表 = pd.DataFrame()

    print('获取案例...')
    行业列表 = []
    智能领域列表 = []
    方案形态列表 = []
    产业链角色列表 = []
    成立年份列表 = []
    案例 = graph.run(
        "MATCH (a:BusinessCase)-[r:indexed_by]-(b:TechField) where b.name='物联网技术' RETURN a.name as 案例, a.uuid as uuid").data()
    for i in tqdm(案例):
        行业 = graph.run(
            "MATCH (a:BusinessCase)-[]-(b:Industry) where a.uuid='{}' RETURN b.name as 行业".format(i['uuid'])).data()
        智能领域_1 = graph.run(
            "MATCH (a:BusinessCase)-[]-(b:AiField) where a.uuid='{}' RETURN b.name as 智能领域".format(i['uuid'])).data()
        智能领域_2 = graph.run(
            "MATCH (a:BusinessCase)-[]-(b:Solution)-[]-(c:AiField) where a.uuid='{}' RETURN c.name as 智能领域".format(i['uuid'])).data()
        智能领域 = 智能领域_1 + 智能领域_2
        s = pd.Series({
            '研究主体': '案例',
            '案例名称': i['案例'],
            '案例UUID': i['uuid'],
            '相关行业': preprocess(行业),
            '智能领域': preprocess(智能领域)
        })
        案例表 = 案例表.append(s, ignore_index=True)
        if preprocess(行业):
            行业列表 += preprocess(行业)
        if preprocess(智能领域):
            智能领域列表 += preprocess(智能领域)
    print('获取解决方案...')
    解决方案 = graph.run(
        "MATCH (a:Solution)-[r:indexed_by]-(b:TechField) where b.name='物联网技术' RETURN a.name as 解决方案, a.uuid as uuid").data()
    for i in tqdm(解决方案):
        行业 = graph.run(
            "MATCH (a:Solution)-[]-(b:Industry) where a.uuid='{}' RETURN b.name as 行业".format(i['uuid'])).data()
        智能领域 = graph.run(
            "MATCH (a:Solution)-[]-(b:AiField) where a.uuid='{}' RETURN b.name as 智能领域".format(i['uuid'])).data()
        方案形态 = graph.run(
            "MATCH (a:Solution)-[r:format_of]-(b:ApplyFormat) where a.uuid='{}' RETURN b.name as 方案形态".format(i['uuid'])).data()
        s = pd.Series({
            '研究主体': '解决方案',
            '解决方案名称': i['解决方案'],
            '解决方案UUID': i['uuid'],
            '相关行业': preprocess(行业),
            '智能领域': preprocess(智能领域),
            '方案形态': preprocess(方案形态)
        })
        解决方案表 = 解决方案表.append(s, ignore_index=True)
        if preprocess(行业):
            行业列表 += preprocess(行业)
        if preprocess(智能领域):
            智能领域列表 += preprocess(智能领域)
        if preprocess(方案形态):
            方案形态列表 += preprocess(方案形态)
    print('获取机构...')
    机构 = graph.run(
        "MATCH (a:Institution)-[r:indexed_by]-(b:TechField) where b.name='物联网技术' RETURN a.name as 机构, a.uuid as uuid").data()
    for i in tqdm(机构):
        行业 = graph.run(
            "MATCH (a:Institution)-[]-(b:Industry) where a.uuid='{}' RETURN b.name as 行业".format(i['uuid'])).data()
        智能领域_1 = graph.run(
            "MATCH (a:Institution)-[]-(b:AiField) where a.uuid='{}' RETURN b.name as 智能领域".format(i['uuid'])).data()
        智能领域_2 = graph.run(
            "MATCH (a:Institution)-[]-(b:Solution)-[]-(c:AiField) where a.uuid='{}' RETURN c.name as 智能领域".format(i['uuid'])).data()
        产业链角色 = graph.run(
            "MATCH (a:Institution) where a.uuid='{}' RETURN a.roles as 产业链角色".format(i['uuid'])).data()
        成立年份 = graph.run(
            "MATCH (a:Institution) where a.uuid='{}' RETURN a.founded_at as 成立时间".format(i['uuid'])).data()
        成立年份 = timestamp2str(成立年份[0]['成立时间'])
        成立年份列表.append(成立年份)
        智能领域 = 智能领域_1 + 智能领域_2
        s = pd.Series({
            '研究主体': '机构',
            '机构名称': i['机构'],
            '机构UUID': i['uuid'],
            '相关行业': preprocess(行业),
            '智能领域': preprocess(智能领域),
            '产业链角色': preprocess_2(产业链角色),
            '成立年份': 成立年份
        })
        机构表 = 机构表.append(s, ignore_index=True)
        if preprocess(智能领域):
            智能领域列表 += preprocess(智能领域)
        if preprocess(产业链角色):
            产业链角色列表 += preprocess(产业链角色)
    print('获取行业分布...')
    行业列表 = list(set(行业列表))
    for i in tqdm(行业列表):
        IOT案例 = graph.run(
            "MATCH (a:Industry)-[]-(b:BusinessCase)-[r:indexed_by]-(c:TechField) where c.name='物联网技术' and a.name='{}' RETURN b.name as 案例".format(i)).data()
        KB案例 = graph.run(
            "MATCH (a:BusinessCase)-[]-(b:Industry) where b.name='{}' RETURN a.name as 案例".format(i)).data()
        IOT解决方案 = graph.run(
            "MATCH (a:Industry)-[]-(b:Solution)-[r:indexed_by]-(c:TechField) where c.name='物联网技术' and a.name='{}' RETURN b.name as 解决方案".format(i)).data()
        KB解决方案 = graph.run(
            "MATCH (a:Solution)-[]-(b:Industry) where b.name='{}' RETURN a.name as 解决方案".format(i)).data()
        # IOT机构 = graph.run(
        #     "MATCH (a:Industry)-[]-(b:Institution)-[r:indexed_by]-(c:TechField) where c.name='物联网技术' and a.name='{}' RETURN b.name as 机构".format(i)).data()
        # KB机构 = graph.run(
        #     "MATCH (a:Institution)-[]-(b:Industry) where b.name='{}' RETURN a.name as 机构".format(i)).data()
        s = pd.Series({
            '行业': i,
            'IOT案例数量': len(IOT案例),
            '全KB案例数量': len(KB案例),
            'IOT解决方案数量': len(IOT解决方案),
            '全KB解决方案数量': len(KB解决方案)
            # 'IOT机构数量': len(IOT机构),
            # '全KB机构数量': len(KB机构)
        })
        行业表 = 行业表.append(s, ignore_index=True)
    print('获取智能领域分布...')
    智能领域列表 = list(set(智能领域列表))
    for i in tqdm(智能领域列表):
        IOT案例 = graph.run(
            "MATCH (a:AiField)-[]-(b:BusinessCase)-[r:indexed_by]-(c:TechField) where c.name='物联网技术' and a.name='{}' RETURN b.name as 案例".format(i)).data()
        KB案例 = graph.run(
            "MATCH (a:BusinessCase)-[]-(b:AiField) where b.name='{}' RETURN a.name as 案例".format(i)).data()
        IOT解决方案 = graph.run(
            "MATCH (a:AiField)-[]-(b:Solution)-[r:indexed_by]-(c:TechField) where c.name='物联网技术' and a.name='{}' RETURN b.name as 解决方案".format(i)).data()
        KB解决方案 = graph.run(
            "MATCH (a:Solution)-[]-(b:AiField) where b.name='{}' RETURN a.name as 解决方案".format(i)).data()
        IOT机构 = graph.run(
            "MATCH (a:AiField)-[]-(b:Institution)-[r:indexed_by]-(c:TechField) where c.name='物联网技术' and a.name='{}' RETURN b.name as 机构".format(i)).data()
        KB机构 = graph.run(
            "MATCH (a:Institution)-[]-(b:AiField) where b.name='{}' RETURN a.name as 机构".format(i)).data()
        s = pd.Series({
            '智能领域': i,
            'IOT案例数量': len(IOT案例),
            '全KB案例数量': len(KB案例),
            'IOT解决方案数量': len(IOT解决方案),
            '全KB解决方案数量': len(KB解决方案),
            'IOT机构数量': len(IOT机构),
            '全KB机构数量': len(KB机构)
        })
        智能领域表 = 智能领域表.append(s, ignore_index=True)
    print('获取方案形态分布...')
    方案形态列表 = list(set(方案形态列表))
    for i in tqdm(方案形态列表):
        IOT解决方案 = graph.run(
            "MATCH (a:ApplyFormat)-[r:format_of]-(b:Solution)-[i:indexed_by]-(c:TechField) where c.name='物联网技术' and a.name='{}' RETURN b.name as 解决方案".format(i)).data()
        KB解决方案 = graph.run(
            "MATCH (a:Solution)-[r:format_of]-(b:ApplyFormat) where b.name='{}' RETURN a.name as 解决方案".format(i)).data()
        s = pd.Series({
            '方案形态': i,
            'IOT解决方案数量': len(IOT解决方案),
            '全KB解决方案数量': len(KB解决方案)
        })
        方案形态表 = 方案形态表.append(s, ignore_index=True)
    print('获取产业链角色分布...')
    temp = []
    for i in 产业链角色列表:
        if i:
            for j in eval(i):
                temp.append(j)
    产业链角色列表 = list(set(temp))
    for i in tqdm(产业链角色列表):
        # IOT案例 = graph.run(
        #     "MATCH (a:Institution)-[]-(b:BusinessCase)-[r:indexed_by]-(c:TechField) where c.name='物联网技术' and a.roles Contains '{}' RETURN b.name as 案例".format(i)).data()
        # KB案例 = graph.run(
        #     "MATCH (a:BusinessCase)-[]-(b:Institution) where b.roles Contains '{}' RETURN a.name as 案例".format(i)).data()
        # IOT解决方案 = graph.run(
        #     "MATCH (a:Institution)-[]-(b:Solution)-[r:indexed_by]-(c:TechField) where c.name='物联网技术' and a.roles Contains '{}' RETURN b.name as 解决方案".format(i)).data()
        # KB解决方案 = graph.run(
        #     "MATCH (a:Solution)-[]-(b:Institution) where b.roles Contains '{}' RETURN a.name as 解决方案".format(i)).data()
        IOT机构 = graph.run(
            "MATCH (a:Institution)-[r:indexed_by]-(c:TechField) where c.name='物联网技术' and a.roles Contains '{}' RETURN a.name as 机构".format(i)).data()
        KB机构 = graph.run(
            "MATCH (a:Institution) where a.roles Contains '{}' RETURN a.name as 机构".format(i)).data()
        s = pd.Series({
            '产业链角色': i,
            # 'IOT案例数量': len(IOT案例),
            # '全KB案例数量': len(KB案例),
            # 'IOT解决方案数量': len(IOT解决方案),
            # '全KB解决方案数量': len(KB解决方案),
            'IOT机构数量': len(IOT机构),
            '全KB机构数量': len(KB机构)
        })
        产业链角色表 = 产业链角色表.append(s, ignore_index=True)
    counter = Counter(成立年份列表)
    成立年份表['成立时间'] = counter.keys()
    成立年份表['分布'] = counter.values()
    writer = pd.ExcelWriter('分析一.xlsx')
    案例表顺序 = ['研究主体', '案例名称', '相关行业', '智能领域', '案例UUID']
    案例表 = 案例表[案例表顺序]
    解决方案表顺序 = ['研究主体', '解决方案名称', '相关行业', '智能领域', '方案形态', '解决方案UUID']
    解决方案表 = 解决方案表[解决方案表顺序]
    机构表顺序 = ['研究主体', '机构名称', '相关行业', '智能领域', '产业链角色', '成立年份', '机构UUID']
    机构表 = 机构表[机构表顺序]
    行业表顺序 = ['行业', 'IOT案例数量', '全KB案例数量', 'IOT解决方案数量', '全KB解决方案数量']
    行业表 = 行业表[行业表顺序]
    智能领域表顺序 = ['智能领域', 'IOT案例数量', '全KB案例数量',
               'IOT解决方案数量', '全KB解决方案数量', 'IOT机构数量', '全KB机构数量']
    智能领域表 = 智能领域表[智能领域表顺序]
    方案形态表顺序 = ['方案形态', 'IOT解决方案数量', '全KB解决方案数量']
    方案形态表 = 方案形态表[方案形态表顺序]
    产业链角色表顺序 = ['产业链角色', 'IOT机构数量', '全KB机构数量']
    产业链角色表 = 产业链角色表[产业链角色表顺序]
    成立年份表顺序 = ['成立时间', '分布']
    成立年份表 = 成立年份表[成立年份表顺序]
    案例表.to_excel(writer, sheet_name='案例', index=False)
    解决方案表.to_excel(writer, sheet_name='解决方案', index=False)
    机构表.to_excel(writer, sheet_name='机构', index=False)
    行业表.to_excel(writer, sheet_name='行业', index=False)
    智能领域表.to_excel(writer, sheet_name='智能领域', index=False)
    方案形态表.to_excel(writer, sheet_name='方案形态', index=False)
    产业链角色表.to_excel(writer, sheet_name='产业链角色', index=False)
    成立年份表.to_excel(writer, sheet_name='成立年份表', index=False)
    writer.save()


def 分析一_技术词频():
    技术 = graph.run(
        "MATCH (a:Technology) RETURN a.name as 技术").data()
    技术 = preprocess(技术)
    技术词频表 = pd.DataFrame()
    print('获取技术词频...')
    error = 0
    for i in tqdm(技术):
        try:
            解决方案_1 = graph.run(
                'MATCH (a:Solution)-[r:indexed_by]-(b:TechField) where b.name="物联网技术" and (a.summary =~".*{0}.*" or a.desc =~".*{0}.*") RETURN a.name as 解决方案'.format(i)).data()
        except:
            解决方案_1 = []
            error += 1
        try:
            解决方案_2 = graph.run(
                'MATCH (a:Solution)-[r:indexed_by]-(b:TechField)-[]-(c:Technology) where b.name="物联网技术" and c.name="{}" RETURN a.name as 解决方案'.format(i)).data()
        except:
            解决方案_2 = []
            error += 1
        try:
            机构_1 = graph.run(
                'MATCH (a:Institution)-[r:indexed_by]-(b:TechField) where b.name="物联网技术" and (a.summary =~".*{0}.*" or a.desc =~".*{0}.*") RETURN a.name as 解决方案'.format(i)).data()
        except:
            机构_1 = []
            error += 1
        try:
            机构_2 = graph.run(
                'MATCH (a:Institution)-[r:indexed_by]-(b:TechField)-[]-(c:Technology) where b.name="物联网技术" and c.name="{} RETURN a.name as 解决方案'.format(i)).data()
        except:
            机构_2 = []
            error += 1
        if len(解决方案_1) or len(解决方案_2) or len(机构_1) or len(机构_2):
            s = pd.Series({
                '技术名称': i,
                '解决方案': len(解决方案_1) + len(解决方案_2),
                '机构': len(机构_1) + len(机构_2)
            })
            技术词频表 = 技术词频表.append(s, ignore_index=True)
    技术词频表.to_excel('分析一-技术词频表.xlsx', index=False)


def 分析二():
    def 客户案例(domain):
        客户案例总数 = pd.DataFrame()
        客户业务场景 = pd.DataFrame()
        客户业务场景['业务场景'] = ''
        客户业务场景['Count'] = ''
        客户智能领域 = pd.DataFrame()
        客户智能领域['智能领域'] = ''
        客户智能领域['Count'] = ''
        业务场景 = []
        智能领域 = []
        源数据 = pd.read_excel('汇总_0417.xlsx', '智能化案例')
        if domain:
            客户案例 = 源数据[源数据['适用行业'] == domain]
        else:
            客户案例 = 源数据
        if domain == '公共':
            客户案例 = 源数据[源数据['适用行业'].isin(['公共设施', '公共服务'])]
        writer = pd.ExcelWriter('分析二-{}客户案例.xlsx'.format(domain))
        for idx, val in enumerate(客户案例['案例应用的业务场景']):
            if not pd.isnull(val):
                if '[' in str(val):
                    业务场景 += eval(val)
                else:
                    业务场景 += str(val).split('？')
        for idx, val in enumerate(客户案例['案例应用的智能领域']):
            if not pd.isnull(val):
                if '[' in str(val):
                    智能领域 += eval(val)
                else:
                    智能领域 += str(val).split('？')
            else:
                if not pd.isnull(客户案例['解决方案的智能领域'].iloc[idx]):
                    if '[' in str(val):
                        智能领域 += eval(val)
                    else:
                        智能领域 += str(val).split('？')
        客户案例总数['客户案例总数'] = [len(客户案例)]
        客户案例总数.to_excel(writer, '客户案例总数', index=False)
        业务场景 = Counter(业务场景)
        客户业务场景['业务场景'] = 业务场景.keys()
        客户业务场景['Count'] = 业务场景.values()
        客户业务场景 = 客户业务场景.sort_values(by=['Count'], ascending=False)
        客户业务场景.to_excel(writer, '业务场景', index=False)
        智能领域 = Counter(智能领域)
        客户智能领域['智能领域'] = 智能领域.keys()
        客户智能领域['Count'] = 智能领域.values()
        客户智能领域 = 客户智能领域.sort_values(by=['Count'], ascending=False)
        客户智能领域.to_excel(writer, '智能领域', index=False)
        writer.save()

    def AIOT创业公司(domain):
        AIOT创业公司总数 = pd.DataFrame()
        AIOT创业公司智能领域 = pd.DataFrame()
        AIOT创业公司智能领域['智能领域'] = ''
        AIOT创业公司智能领域['Count'] = ''
        AIOT创业公司产业链角色 = pd.DataFrame()
        AIOT创业公司产业链角色['产业链角色'] = ''
        AIOT创业公司产业链角色['Count'] = ''
        AIOT创业公司成立年份 = pd.DataFrame()
        AIOT创业公司成立年份['成立年份'] = ''
        AIOT创业公司成立年份['Count'] = ''
        智能领域 = []
        产业链角色 = []
        成立年份 = []
        源数据 = pd.read_excel('汇总_0417.xlsx', 'AIOT创业公司')
        if domain:
            AIOT创业公司 = 源数据[源数据['适用行业'] == domain]
        else:
            AIOT创业公司 = 源数据
        if domain == '公共':
            AIOT创业公司 = 源数据[源数据['适用行业'].isin(['公共设施', '公共服务'])]
        writer = pd.ExcelWriter('分析二-{}AIOT创业公司.xlsx'.format(domain))
        for idx, val in enumerate(AIOT创业公司['供应商的智能领域']):
            if not pd.isnull(val):
                if '[' in str(val):
                    智能领域 += eval(val)
                else:
                    智能领域 += str(val).split('？')
            else:
                if not pd.isnull(AIOT创业公司['解决方案的智能领域'].iloc[idx]):
                    if '[' in str(val):
                        智能领域 += eval(val)
                    else:
                        智能领域 += str(val).split('？')
        for idx, val in enumerate(AIOT创业公司['供应商产业链角色']):
            if not pd.isnull(val):
                if '[' in str(val):
                    产业链角色 += eval(val)
                else:
                    产业链角色 += str(val).split('？')
        for idx, val in enumerate(AIOT创业公司['成立年份']):
            if not pd.isnull(val):
                if '[' in str(val):
                    成立年份 += eval(val)
                else:
                    成立年份 += str(val).split('？')
        AIOT创业公司总数['AIOT创业公司总数'] = [len(AIOT创业公司)]
        AIOT创业公司总数.to_excel(writer, 'AIOT创业公司总数', index=False)
        智能领域 = Counter(智能领域)
        AIOT创业公司智能领域['智能领域'] = 智能领域.keys()
        AIOT创业公司智能领域['Count'] = 智能领域.values()
        AIOT创业公司智能领域 = AIOT创业公司智能领域.sort_values(by=['Count'], ascending=False)
        AIOT创业公司智能领域.to_excel(writer, '智能领域', index=False)
        产业链角色 = Counter(产业链角色)
        AIOT创业公司产业链角色['产业链角色'] = 产业链角色.keys()
        AIOT创业公司产业链角色['Count'] = 产业链角色.values()
        AIOT创业公司产业链角色 = AIOT创业公司产业链角色.sort_values(
            by=['Count'], ascending=False)
        AIOT创业公司产业链角色.to_excel(writer, '产业链角色', index=False)
        成立年份 = Counter(成立年份)
        AIOT创业公司成立年份['成立年份'] = 成立年份.keys()
        AIOT创业公司成立年份['Count'] = 成立年份.values()
        AIOT创业公司成立年份 = AIOT创业公司成立年份.sort_values(by=['Count'], ascending=False)
        AIOT创业公司成立年份.to_excel(writer, '成立年份', index=False)
        writer.save()

    def 解决方案(domain):
        解决方案总数 = pd.DataFrame()
        解决方案业务场景 = pd.DataFrame()
        解决方案业务场景['业务场景'] = ''
        解决方案业务场景['Count'] = ''
        解决方案智能领域 = pd.DataFrame()
        解决方案智能领域['智能领域'] = ''
        解决方案智能领域['Count'] = ''
        解决方案技术领域 = pd.DataFrame()
        解决方案技术领域['技术领域'] = ''
        解决方案技术领域['Count'] = ''
        解决方案方案形态 = pd.DataFrame()
        解决方案方案形态['方案形态'] = ''
        解决方案方案形态['Count'] = ''
        业务场景 = []
        智能领域 = []
        技术领域 = []
        方案形态 = []
        源数据 = pd.read_excel('汇总_0417.xlsx', '行业解决方案')
        if domain:
            解决方案 = 源数据[源数据['适用行业'] == domain]
        else:
            解决方案 = 源数据
        if domain == '公共':
            解决方案 = 源数据[源数据['适用行业'].isin(['公共设施', '公共服务'])]
        writer = pd.ExcelWriter('分析二-{}行业解决方案.xlsx'.format(domain))
        for idx, val in enumerate(解决方案['解决方案的业务场景']):
            if not pd.isnull(val):
                if '[' in str(val):
                    业务场景 += eval(val)
                else:
                    业务场景 += str(val).split('？')
        for idx, val in enumerate(解决方案['解决方案的智能领域']):
            if not pd.isnull(val):
                if '[' in str(val):
                    智能领域 += eval(val)
                else:
                    智能领域 += str(val).split('？')
        for idx, val in enumerate(解决方案['解决方案的技术领域']):
            if not pd.isnull(val):
                if '[' in str(val):
                    技术领域 += eval(val)
                else:
                    技术领域 += str(val).split('？')
        for idx, val in enumerate(解决方案['方案形态']):
            if not pd.isnull(val):
                if '[' in str(val):
                    方案形态 += eval(val)
                else:
                    方案形态 += str(val).split('？')
        解决方案总数['解决方案总数'] = [len(解决方案)]
        解决方案总数.to_excel(writer, '解决方案总数', index=False)
        业务场景 = Counter(业务场景)
        解决方案业务场景['业务场景'] = 业务场景.keys()
        解决方案业务场景['Count'] = 业务场景.values()
        解决方案业务场景 = 解决方案业务场景.sort_values(by=['Count'], ascending=False)
        解决方案业务场景.to_excel(writer, '业务场景', index=False)
        智能领域 = Counter(智能领域)
        解决方案智能领域['智能领域'] = 智能领域.keys()
        解决方案智能领域['Count'] = 智能领域.values()
        解决方案智能领域 = 解决方案智能领域.sort_values(by=['Count'], ascending=False)
        解决方案智能领域.to_excel(writer, '智能领域', index=False)
        技术领域 = Counter(技术领域)
        解决方案技术领域['技术领域'] = 技术领域.keys()
        解决方案技术领域['Count'] = 技术领域.values()
        解决方案技术领域 = 解决方案技术领域.sort_values(by=['Count'], ascending=False)
        解决方案技术领域.to_excel(writer, '技术领域', index=False)
        方案形态 = Counter(方案形态)
        解决方案方案形态['方案形态'] = 方案形态.keys()
        解决方案方案形态['Count'] = 方案形态.values()
        解决方案方案形态 = 解决方案方案形态.sort_values(by=['Count'], ascending=False)
        解决方案方案形态.to_excel(writer, '方案形态', index=False)
        writer.save()

    客户案例(None)
    AIOT创业公司(None)
    解决方案(None)
    客户案例('地产')
    AIOT创业公司('地产')
    解决方案('地产')
    客户案例('公共设施')
    AIOT创业公司('公共设施')
    解决方案('公共设施')
    客户案例('公共服务')
    AIOT创业公司('公共服务')
    解决方案('公共服务')
    客户案例('公共')
    AIOT创业公司('公共')
    解决方案('公共')


def 分析二_技术词频():
    def 获取词频(keyword):
        print('获取{}...'.format(keyword))
        技术词频表 = pd.DataFrame()
        技术 = graph.run(
            "MATCH (a:Technology) RETURN a.name as 技术").data()
        技术 = preprocess(技术)
        error = 0
        for i in tqdm(技术):
            if keyword == '公共':
                try:
                    解决方案_1 = graph.run(
                        'MATCH (a:Solution)-[]-(b:Industry) where (b.name="公共服务" or b.name="公共设施") and (a.summary =~".*{0}.*" or a.desc =~".*{0}.*") RETURN a.name as 解决方案'.format(i, keyword)).data()
                except:
                    解决方案_1 = []
                    error += 1
                try:
                    解决方案_2 = graph.run(
                        'MATCH (a:Solution)-[]-(b:Industry)-[]-(c:Technology) where (b.name="公共服务" or b.name="公共设施") and (c.name="{}") RETURN a.name as 解决方案'.format(i)).data()
                except:
                    解决方案_2 = []
                    error += 1
                try:
                    机构_1 = graph.run(
                        'MATCH (a:Institution)-[]-(b:Industry) where (b.name="公共服务" or b.name="公共设施") and (a.summary =~".*{0}.*" or a.desc =~".*{0}.*") RETURN a.name as 解决方案'.format(i, keyword)).data()
                except:
                    机构_1 = []
                    error += 1
                try:
                    机构_2 = graph.run(
                        'MATCH (a:Institution)-[]-(b:Industry)-[]-(c:Technology) where (b.name="公共服务" or b.name="公共设施") and (c.name="{}") RETURN a.name as 解决方案'.format(i)).data()
                except:
                    机构_2 = []
                    error += 1
            else:
                try:
                    解决方案_1 = graph.run(
                        'MATCH (a:Solution)-[]-(b:Industry) where b.name="{1}" and (a.summary =~".*{0}.*" or a.desc =~".*{0}.*") RETURN a.name as 解决方案'.format(i, keyword)).data()
                except:
                    解决方案_1 = []
                    error += 1
                try:
                    解决方案_2 = graph.run(
                        'MATCH (a:Solution)-[]-(b:Industry)-[]-(c:Technology) where b.name="{1}" and (c.name="{0}") RETURN a.name as 解决方案'.format(i, keyword)).data()
                except:
                    解决方案_2 = []
                    error += 1
                try:
                    机构_1 = graph.run(
                        'MATCH (a:Institution)-[]-(b:Industry) where b.name="{1}" and (a.summary =~".*{0}.*" or a.desc =~".*{0}.*") RETURN a.name as 解决方案'.format(i, keyword)).data()
                except:
                    机构_1 = []
                    error += 1
                try:
                    机构_2 = graph.run(
                        'MATCH (a:Institution)-[]-(b:Industry)-[]-(c:Technology) where b.name="{1}" and (c.name="{0}") RETURN a.name as 解决方案'.format(i, keyword)).data()
                except:
                    机构_2 = []
                    error += 1
            if len(解决方案_1) or len(解决方案_2) or len(机构_1) or len(机构_2):
                s = pd.Series({
                    '技术名称': i,
                    '解决方案': len(解决方案_1) + len(解决方案_2),
                    '机构': len(机构_1) + len(机构_2)
                })
                技术词频表 = 技术词频表.append(s, ignore_index=True)
        技术词频表.to_excel('{}技术词频表.xlsx'.format(keyword), index=False)
    获取词频('地产')
    获取词频('公共服务')
    获取词频('公共设施')
    获取词频('公共')


def 分析三():
    地产_标签 = pd.read_excel('【标签匹配】新闻汇总-AIOT+地产+公共.xlsx', '地产')
    地产_关键词 = pd.read_excel('【关键词匹配】新闻汇总-AIOT+地产+公共.xlsx', '地产')
    公共_标签 = pd.read_excel('【标签匹配】新闻汇总-AIOT+地产+公共.xlsx', '公共')
    公共_关键词 = pd.read_excel('【关键词匹配】新闻汇总-AIOT+地产+公共.xlsx', '公共')
    地产 = pd.concat([地产_标签, 地产_关键词], sort=False)
    地产.drop_duplicates(['新闻标题'], keep='first', inplace=True)
    公共 = pd.concat([公共_标签, 公共_关键词], sort=False)
    公共.drop_duplicates(['新闻标题'], keep='first', inplace=True)
    articles = pd.read_csv('articles.csv')
    dailies = pd.read_csv('dailies.csv')
    eigen_sources = pd.read_csv('eigen_sources.csv')
    lut = {
        'article': articles,
        'daily': dailies,
        'eigen': eigen_sources
    }
    地产['时间'] = ''
    公共['时间'] = ''
    print('获取地产...')
    for idx, val in tqdm(enumerate(地产['id'])):
        content = lut[地产['新闻分类'].iloc[idx]]
        content = content[content['id'] == val]
        地产['时间'].iloc[idx] = content['created_at'].iloc[0].split(' ')[0]
    print('获取公共...')
    for idx, val in tqdm(enumerate(公共['id'])):
        content = lut[公共['新闻分类'].iloc[idx]]
        content = content[content['id'] == val]
        公共['时间'].iloc[idx] = content['created_at'].iloc[0].split(' ')[0]
    taggings = pd.read_csv('taggings.csv')
    tags = pd.read_excel('tags.xlsx')
    print('获取地产...')
    地产['相关技术领域'] = ''
    for idx, val in tqdm(enumerate(地产['相关技术领域'])):
        news_id = 地产['id'].iloc[idx]
        temp_taggings = taggings[taggings['taggable_id'] == news_id]
        if not temp_taggings.empty:
            institution = []
            for a, b in enumerate(temp_taggings['tag_id']):
                temp_tags = tags[tags['id'] == b]
                if not temp_tags.empty:
                    for c in temp_tags['name']:
                        institution.append(c)
        地产['相关技术领域'].iloc[idx] = list(set(institution))
    地产.to_excel('地产.xlsx', index=False)
    print('获取公共...')
    公共['相关技术领域'] = ''
    for idx, val in tqdm(enumerate(公共['相关技术领域'])):
        news_id = 公共['id'].iloc[idx]
        temp_taggings = taggings[taggings['taggable_id'] == news_id]
        if not temp_taggings.empty:
            institution = []
            for a, b in enumerate(temp_taggings['tag_id']):
                temp_tags = tags[tags['id'] == b]
                if not temp_tags.empty:
                    for c in temp_tags['name']:
                        institution.append(c)
        公共['相关技术领域'].iloc[idx] = list(set(institution))
    公共.to_excel('公共.xlsx', index=False)


def 分析三_技术():
    技术 = graph.run(
        "MATCH (a:Technology) RETURN a.name as 技术").data()
    技术 = preprocess(技术)
    地产 = pd.read_excel('地产.xlsx')
    公共 = pd.read_excel('公共.xlsx')
    地产['技术'] = ''
    公共['技术'] = ''
    print('获取地产...')
    for idx, val in enumerate(地产['新闻标题']):
        temp = []
        for i in 技术:
            if i in str(val):
                temp.append(i)
        temp = list(set(temp))
        地产['技术'].iloc[idx] = temp
    print('获取公共...')
    for idx, val in enumerate(公共['新闻标题']):
        temp = []
        for i in 技术:
            if i in str(val):
                temp.append(i)
        temp = list(set(temp))
        公共['技术'].iloc[idx] = temp
    地产.to_excel('地产.xlsx', index=False)
    公共.to_excel('公共.xlsx', index=False)


def 分析三_分布():
    地产 = pd.read_excel('地产.xlsx')
    公共 = pd.read_excel('公共.xlsx')

    def 时间分布():
        地产_时间 = []
        公共_时间 = []
        地产时间分布表 = pd.DataFrame()
        公共时间分布表 = pd.DataFrame()
        for idx, val in enumerate(地产['时间']):
            time = val.split('/')
            if len(time[1]) == 1:
                地产_时间.append('{}-0{}'.format(time[2], time[1]))
            else:
                地产_时间.append('{}-{}'.format(time[2], time[1]))
        地产_counter = Counter(地产_时间)
        for idx, val in enumerate(公共['时间']):
            time = val.split('/')
            if len(time[1]) == 1:
                公共_时间.append('{}-0{}'.format(time[2], time[1]))
            else:
                公共_时间.append('{}-{}'.format(time[2], time[1]))
        公共_counter = Counter(公共_时间)
        地产时间分布表['时间'] = 地产_counter.keys()
        地产时间分布表['新闻数量分布'] = 地产_counter.values()
        公共时间分布表['时间'] = 公共_counter.keys()
        公共时间分布表['新闻数量分布'] = 公共_counter.values()
        地产时间分布表.to_excel('地产时间分布表.xlsx', index=False)
        公共时间分布表.to_excel('公共时间分布表.xlsx', index=False)

    def 技术领域分布():
        时间 = ['2017-06', '2017-07', '2017-08', '2017-09', '2017-10', '2017-11', '2017-12', '2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06',
              '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12', '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12', '2020-01', '2020-02', '2020-03']
        地产_技术领域 = []
        地产技术领域分布表 = pd.DataFrame()
        for idx, val in enumerate(地产['相关技术领域']):
            for i in eval(val):
                地产_技术领域.append(i)
        地产_技术领域列表 = list(set(地产_技术领域))
        地产_时间_技术领域 = {i: {} for i in 时间}
        for idx, val in enumerate(地产['时间']):
            time = val.split('/')
            if len(time[1]) == 1:
                地产['时间'].iloc[idx] = '{}-0{}'.format(time[2], time[1])
            else:
                地产['时间'].iloc[idx] = '{}-{}'.format(time[2], time[1])
        for k, v in 地产_时间_技术领域.items():
            for i in 地产_技术领域列表:
                v[i] = 0
        for k, v in 地产_时间_技术领域.items():
            for i in 地产_技术领域列表:
                temp = 地产[(地产['时间'] == k) & (地产['相关技术领域'].str.contains(i))]
                v[i] = len(temp)
        地产技术领域分布表 = pd.DataFrame.from_dict(地产_时间_技术领域)
        地产技术领域分布表.to_excel('地产技术领域分布表.xlsx')

        公共_技术领域 = []
        公共技术领域分布表 = pd.DataFrame()
        for idx, val in enumerate(公共['相关技术领域']):
            for i in eval(val):
                公共_技术领域.append(i)
        公共_技术领域列表 = list(set(公共_技术领域))
        公共_时间_技术领域 = {i: {} for i in 时间}
        for idx, val in enumerate(公共['时间']):
            time = val.split('/')
            if len(time[1]) == 1:
                公共['时间'].iloc[idx] = '{}-0{}'.format(time[2], time[1])
            else:
                公共['时间'].iloc[idx] = '{}-{}'.format(time[2], time[1])
        for k, v in 公共_时间_技术领域.items():
            for i in 公共_技术领域列表:
                v[i] = 0
        for k, v in 公共_时间_技术领域.items():
            for i in 公共_技术领域列表:
                temp = 公共[(公共['时间'] == k) & (公共['相关技术领域'].str.contains(i))]
                v[i] = len(temp)
        公共技术领域分布表 = pd.DataFrame.from_dict(公共_时间_技术领域)
        公共技术领域分布表.to_excel('公共技术领域分布表.xlsx')
    
    def 技术分布():
        时间 = ['2017-06', '2017-07', '2017-08', '2017-09', '2017-10', '2017-11', '2017-12', '2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06',
              '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12', '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12', '2020-01', '2020-02', '2020-03']
        地产_技术 = []
        地产技术表 = pd.DataFrame()
        for idx, val in enumerate(地产['技术']):
            for i in eval(val):
                地产_技术.append(i)
        地产_技术列表 = list(set(地产_技术))
        地产_时间_技术 = {i: {} for i in 时间}
        for idx, val in enumerate(地产['时间']):
            time = val.split('/')
            if len(time[1]) == 1:
                地产['时间'].iloc[idx] = '{}-0{}'.format(time[2], time[1])
            else:
                地产['时间'].iloc[idx] = '{}-{}'.format(time[2], time[1])
        for k, v in 地产_时间_技术.items():
            for i in 地产_技术列表:
                v[i] = 0
        for k, v in 地产_时间_技术.items():
            for i in 地产_技术列表:
                temp = 地产[(地产['时间'] == k) & (地产['技术'].str.contains(i))]
                v[i] = len(temp)
        地产技术分布表 = pd.DataFrame.from_dict(地产_时间_技术)
        地产技术分布表.to_excel('地产技术分布表.xlsx')

        公共_技术 = []
        公共技术分布表 = pd.DataFrame()
        for idx, val in enumerate(公共['技术']):
            for i in eval(val):
                公共_技术.append(i)
        公共_技术列表 = list(set(公共_技术))
        公共_时间_技术 = {i: {} for i in 时间}
        for idx, val in enumerate(公共['时间']):
            time = val.split('/')
            if len(time[1]) == 1:
                公共['时间'].iloc[idx] = '{}-0{}'.format(time[2], time[1])
            else:
                公共['时间'].iloc[idx] = '{}-{}'.format(time[2], time[1])
        for k, v in 公共_时间_技术.items():
            for i in 公共_技术列表:
                v[i] = 0
        for k, v in 公共_时间_技术.items():
            for i in 公共_技术列表:
                temp = 公共[(公共['时间'] == k) & (公共['技术'].str.contains(i))]
                v[i] = len(temp)
        公共技术分布表 = pd.DataFrame.from_dict(公共_时间_技术)
        公共技术分布表.to_excel('公共技术分布表.xlsx')
    时间分布()
    技术领域分布()
    技术分布()


def 分析二改进():

    def 过滤空格(x):
        x = str(x)
        x = x.replace(' ', '')
        x = x.replace('；', ';')
        x = x.replace(',', ';')
        x = x.replace('，', ';')
        if '[' in x and ';' in x:
            x = x.replace(';', ',')
        return x

    def 客户案例(domain, subject):
        客户案例总数 = pd.DataFrame()
        客户业务场景 = pd.DataFrame()
        客户业务场景['业务场景'] = ''
        客户业务场景['Count'] = ''
        客户智能领域 = pd.DataFrame()
        客户智能领域['智能领域'] = ''
        客户智能领域['Count'] = ''
        客户产业链角色 = pd.DataFrame()
        客户产业链角色['产业链角色'] = ''
        客户产业链角色['Count'] = ''
        客户应用场景 = pd.DataFrame()
        客户应用场景['应用场景'] = ''
        客户应用场景['Count'] = ''
        客户技术任务 = pd.DataFrame()
        客户技术任务['技术任务'] = ''
        客户技术任务['Count'] = ''
        客户AIOT层级 = pd.DataFrame()
        客户AIOT层级['AIOT层级'] = ''
        客户AIOT层级['Count'] = ''
        业务场景 = []
        智能领域 = []
        产业链角色 = []
        应用场景 = []
        技术任务 = []
        AIOT层级 = []
        源数据 = pd.read_excel('【0422_V4】AIoT项目数据汇总_Mos(1).xlsx', '汇总')
        if domain:
            客户案例 = 源数据[(源数据['适用行业'] == domain) & (源数据['研究主体类别'] == subject)]
        else:
            客户案例 = 源数据
        if domain == '公共':
            客户案例 = 源数据[(源数据['适用行业'].isin(['公共设施', '公共服务', '公共'])) & (源数据['研究主体类别'] == subject)]
        if subject == 'AIOT创业公司':
            客户案例 = 源数据[(源数据['适用行业'] == domain) & (源数据['研究主体类别'].isin([subject, 'AIoT机构']))]
            if domain == '公共':
                客户案例 = 源数据[(源数据['适用行业'].isin(['公共设施', '公共服务', '公共'])) & (源数据['研究主体类别'].isin([subject, 'AIoT机构']))]
        writer = pd.ExcelWriter('分析二改进-{}{}.xlsx'.format(domain, subject))
        客户案例['案例应用的业务场景'] = 客户案例['案例应用的业务场景'].map(过滤空格)
        for idx, val in enumerate(客户案例['案例应用的业务场景']):
            if not pd.isnull(val):
                if '[' in str(val):
                    业务场景 += eval(val)
                elif ';' in str(val):
                    业务场景 += str(val).split(';')
                else:
                    业务场景 += str(val).split('？')
        客户案例['解决方案的智能领域'] = 客户案例['解决方案的智能领域'].map(过滤空格)
        for idx, val in enumerate(客户案例['解决方案的智能领域']):
            if not pd.isnull(val):
                if '[' in str(val):
                    智能领域 += eval(val)
                elif ';' in str(val):
                    智能领域 += str(val).split(';')
                else:
                    智能领域 += str(val).split('？')
        客户案例['供应商产业链角色'] = 客户案例['供应商产业链角色'].map(过滤空格)
        for idx, val in enumerate(客户案例['供应商产业链角色']):
            if not pd.isnull(val):
                if '[' in str(val):
                    产业链角色 += eval(val)
                elif ';' in str(val):
                    产业链角色 += str(val).split(';')
                else:
                    产业链角色 += str(val).split('？')
        客户案例['解决方案应用场景'] = 客户案例['解决方案应用场景'].map(过滤空格)
        for idx, val in enumerate(客户案例['解决方案应用场景']):
            if not pd.isnull(val):
                if '[' in str(val):
                    应用场景 += eval(val)
                elif ';' in str(val):
                    应用场景 += str(val).split(';')
                else:
                    应用场景 += str(val).split('？')
        客户案例['解决方案技术任务'] = 客户案例['解决方案技术任务'].map(过滤空格)
        for idx, val in enumerate(客户案例['解决方案技术任务']):
            if not pd.isnull(val):
                if '[' in str(val):
                    技术任务 += eval(val)
                elif ';' in str(val):
                    技术任务 += str(val).split(';')
                else:
                    技术任务 += str(val).split('？')
        客户案例['AIOT所处层级'] = 客户案例['AIOT所处层级'].map(过滤空格)
        for idx, val in enumerate(客户案例['AIOT所处层级']):
            if not pd.isnull(val):
                if '[' in str(val):
                    AIOT层级 += eval(val)
                elif ';' in str(val):
                    AIOT层级 += str(val).split(';')
                else:
                    AIOT层级 += str(val).split('？')
        客户案例总数['{}总数'.format(subject)] = [len(客户案例)]
        客户案例总数.to_excel(writer, '{}总数'.format(subject), index=False)
        业务场景 = Counter(业务场景)
        客户业务场景['业务场景'] = 业务场景.keys()
        客户业务场景['Count'] = 业务场景.values()
        客户业务场景 = 客户业务场景.sort_values(by=['Count'], ascending=False)
        客户业务场景.to_excel(writer, '业务场景', index=False)
        智能领域 = Counter(智能领域)
        客户智能领域['智能领域'] = 智能领域.keys()
        客户智能领域['Count'] = 智能领域.values()
        客户智能领域 = 客户智能领域.sort_values(by=['Count'], ascending=False)
        客户智能领域.to_excel(writer, '智能领域', index=False)
        产业链角色 = Counter(产业链角色)
        客户产业链角色['产业链角色'] = 产业链角色.keys()
        客户产业链角色['Count'] = 产业链角色.values()
        客户产业链角色 = 客户产业链角色.sort_values(by=['Count'], ascending=False)
        客户产业链角色.to_excel(writer, '产业链角色', index=False)
        应用场景 = Counter(应用场景)
        客户应用场景['应用场景'] = 应用场景.keys()
        客户应用场景['Count'] = 应用场景.values()
        客户应用场景 = 客户应用场景.sort_values(by=['Count'], ascending=False)
        客户应用场景.to_excel(writer, '应用场景', index=False)
        技术任务 = Counter(技术任务)
        客户技术任务['技术任务'] = 技术任务.keys()
        客户技术任务['Count'] = 技术任务.values()
        客户技术任务 = 客户技术任务.sort_values(by=['Count'], ascending=False)
        客户技术任务.to_excel(writer, '技术任务', index=False)
        AIOT层级 = Counter(AIOT层级)
        客户AIOT层级['AIOT层级'] = AIOT层级.keys()
        客户AIOT层级['Count'] = AIOT层级.values()
        客户AIOT层级 = 客户AIOT层级.sort_values(by=['Count'], ascending=False)
        客户AIOT层级.to_excel(writer, 'AIOT层级', index=False)
        writer.save()
        
    客户案例('地产', '智能化案例')
    客户案例('地产', '行业解决方案')
    客户案例('地产', 'AIOT创业公司')
    客户案例('公共设施', '智能化案例')
    客户案例('公共设施', '行业解决方案')
    客户案例('公共设施', 'AIOT创业公司')
    客户案例('公共服务', '智能化案例')
    客户案例('公共服务', '行业解决方案')
    客户案例('公共服务', 'AIOT创业公司')
    客户案例('公共', '智能化案例')
    客户案例('公共', '行业解决方案')
    客户案例('公共', 'AIOT创业公司')


def 分析一改进():
    
    def 查找UUID():
        for idx, val in enumerate(案例['案例名称']):
            if pd.isnull(案例['案例UUID'].iloc[idx]):
                UUID = graph.run("MATCH (a:BusinessCase) where a.name='{}' return a.uuid as uuid".format(val)).data()
                if len(UUID):
                    print(len(UUID))
        for idx, val in enumerate(解决方案['解决方案名称']):
            if pd.isnull(解决方案['解决方案UUID'].iloc[idx]):
                UUID = graph.run("MATCH (a:Solution) where a.name='{}' return a.uuid as uuid".format(val)).data()
                if len(UUID):
                    print(len(UUID))
        for idx, val in enumerate(机构['机构名称']):
            if pd.isnull(机构['机构UUID'].iloc[idx]):
                UUID = graph.run("MATCH (a:Institution) where a.name='{}' return a.uuid as uuid".format(val)).data()
                if len(UUID):
                    print(len(UUID))
    
    def 去重():
        案例 = pd.read_excel('分析一[合并].xlsx', sheet_name='案例')
        解决方案 = pd.read_excel('分析一[合并].xlsx', sheet_name='解决方案')
        机构 = pd.read_excel('分析一[合并].xlsx', sheet_name='机构')
        writer = pd.ExcelWriter('分析一改进.xlsx')
        案例UUID = [i for i in 案例['案例UUID'] if not pd.isnull(i)]
        案例UUID = Counter(案例UUID)
        重复案例 = pd.DataFrame()
        for k, v in 案例UUID.items():
            if v > 1:
                print(k, v)
                重复案例 = 重复案例.append({}, ignore_index=True)
                重复案例 = 重复案例.append(案例[案例['案例UUID'] == k], ignore_index=True)
        案例.drop_duplicates(['案例UUID'], keep=False, inplace=True)
        案例 = pd.concat([案例, 重复案例])
        案例顺序 = ['研究主体', '案例名称', '相关行业', '智能领域', '案例UUID']
        案例 = 案例[案例顺序]
        案例.to_excel(writer, '案例', index=False)

        解决方案UUID = [i for i in 解决方案['解决方案UUID'] if not pd.isnull(i)]
        解决方案UUID = Counter(解决方案UUID)
        重复解决方案 = pd.DataFrame()
        for k, v in 解决方案UUID.items():
            if v > 1:
                print(k, v)
                重复解决方案 = 重复解决方案.append({}, ignore_index=True)
                重复解决方案 = 重复解决方案.append(解决方案[解决方案['解决方案UUID'] == k], ignore_index=True)
        解决方案.drop_duplicates(['解决方案UUID'], keep=False, inplace=True)
        解决方案 = pd.concat([解决方案, 重复解决方案])
        解决方案顺序 = ['研究主体', '解决方案名称', '相关行业', '智能领域', '方案形态', '解决方案UUID']
        解决方案 = 解决方案[解决方案顺序]
        解决方案.to_excel(writer, '解决方案', index=False)

        机构UUID = [i for i in 机构['机构UUID'] if not pd.isnull(i)]
        机构UUID = Counter(机构UUID)
        重复机构 = pd.DataFrame()
        for k, v in 机构UUID.items():
            if v > 1:
                print(k, v)
                重复机构 = 重复机构.append({}, ignore_index=True)
                重复机构 = 重复机构.append(机构[机构['机构UUID'] == k], ignore_index=True)
        机构.drop_duplicates(['机构UUID'], keep=False, inplace=True)
        机构 = pd.concat([机构, 重复机构])
        机构顺序 = ['研究主体', '机构名称', '相关行业', '智能领域', '产业链角色', '成立年份', '机构UUID']
        机构 = 机构[机构顺序]
        机构.to_excel(writer, '机构', index=False)
        writer.save()
    
    def 分布():
        案例 = pd.read_excel('分析一[合并].xlsx', sheet_name='案例')
        解决方案 = pd.read_excel('分析一[合并].xlsx', sheet_name='解决方案')
        机构 = pd.read_excel('分析一[合并].xlsx', sheet_name='机构')
        案例行业 = []
        案例智能领域 = []
        解决方案行业 = []
        解决方案智能领域 = []
        解决方案方案形态 = []
        机构行业 = []
        机构智能领域 = []
        机构产业链角色 = []
        机构成立年份 = []
        for idx, val in enumerate(案例['相关行业']):
            if not pd.isnull(val):
                try:
                    for i in eval(str(val)):
                        案例行业.append(i)
                except:
                    案例行业.append(val)
        案例行业 = Counter(案例行业)
        for idx, val in enumerate(案例['智能领域']):
            if not pd.isnull(val):
                try:
                    for i in eval(str(val)):
                        案例智能领域.append(i)
                except:
                    案例智能领域.append(val)
        案例智能领域 = Counter(案例智能领域)

        for idx, val in enumerate(解决方案['相关行业']):
            if not pd.isnull(val):
                try:
                    for i in eval(str(val)):
                        解决方案行业.append(i)
                except:
                    解决方案行业.append(val)
        解决方案行业 = Counter(解决方案行业)
        for idx, val in enumerate(解决方案['智能领域']):
            if not pd.isnull(val):
                try:
                    for i in eval(str(val)):
                        解决方案智能领域.append(i)
                except:
                    if '；' in val:
                        for j in val.split('；'):
                            解决方案智能领域.append(j)
                    else:
                        解决方案智能领域.append(val)
        解决方案智能领域 = Counter(解决方案智能领域)
        for idx, val in enumerate(解决方案['方案形态']):
            if not pd.isnull(val):
                try:
                    for i in eval(str(val)):
                        解决方案方案形态.append(i)
                except:
                    解决方案方案形态.append(val)
        解决方案方案形态 = Counter(解决方案方案形态)

    分布()





if __name__ == '__main__':
    graph = init_neo4j()
    # 分析一()
    # 分析一_技术词频()
    # 分析二()
    # 分析二_技术词频()
    # 分析三()
    # 分析三_技术()
    # 分析三_分布()
    分析二改进()
    # 分析一改进()
