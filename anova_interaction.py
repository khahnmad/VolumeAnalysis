import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import universal_functions as uf
import  pingouin as pg

data = uf.import_json('initial_subsample/output/subsample_keyword_count.json')
# data = uf.import_json('sample/output/sample_keyword_count.json')
partisanships = ['FarLeft', 'Left', 'CenterLeft', 'Center', 'CenterRight', 'Right', 'FarRight']

def num_keywords(data, cat:str):
    columns = ['article_id', 'num_unique_kw_per_art', 'num_keywords', 'month', 'year', 'partisanship']
    df = pd.DataFrame(data=data[cat][1:], columns=columns)


    p, t, value =  {'partisanship':[]},{'time':[]},{'num_articles':[]}

    for part in partisanships:
        for y in range(2016,2023):
            for m in range(1,13):
                v = df.loc[(df['month']==str(m)) & (df['year']==str(y)) & (df['partisanship']==part)]['num_keywords'].sum()

                p['partisanship'].append(part)
                t['time'].append(f"{m}/{y}")
                value['num_articles'].append(v)

    return p, t, value

def num_articles_w_keyword(data, cat:str):
    columns = ['article_id', 'num_unique_kw_per_art', 'num_keywords', 'month', 'year', 'partisanship']
    df = pd.DataFrame(data=data[cat][1:], columns=columns)


    p, t, value =  {'partisanship':[]},{'time':[]},{'num_articles':[]}

    for part in partisanships:
        for y in range(2016,2023):
            for m in range(1,13):
                v = len(df.loc[(df['month']==str(m)) & (df['year']==str(y)) & (df['partisanship']==part) & (df['num_keywords']>0)])

                p['partisanship'].append(part)
                t['time'].append(f"{m}/{y}")
                value['num_articles'].append(v)

    return p, t, value


def prep_variables(metric, data, category):
    ind1, ind2, depend = {}, {}, {}
    if metric == 'num_articles_w_keyword':
        ind1, ind2, depend = num_articles_w_keyword(data, category)
    if metric =='num_keywords':
        ind1, ind2, depend = num_keywords(data, cat=category)
    return ind1, ind2, depend

def perform_two_way_anova(ind_1:dict, ind_2:dict, dependent:dict):
    data = {}
    data.update(ind_1)
    data.update(ind_2)
    data.update(dependent)

    df = pd.DataFrame(data)

    # Stats model
    params = f'{list(dependent.keys())[0]} ~ C({list(ind_2.keys())[0]}) + C({list(ind_1.keys())[0]}) +C({list(ind_2.keys())[0]}):C({list(ind_1.keys())[0]})'
    model = ols(params,data=df).fit()
    # model = ols(
    #     'height ~ C(Fertilizer) + C(Watering) +\
    #     C(Fertilizer):C(Watering)', data=df).fit()
    # result = sm.stats.anova_lm(model, type=2)

    aov = pg.anova(data=df, dv=f'{list(dependent.keys())[0]}',
                   between=[f"{list(ind_1.keys())[0]}",f"{list(ind_2.keys())[0]}"],detailed=True)

    # Greatest Mean Squares
    try:
        max_ms = aov.sort_values(by=['MS'], ascending=False)[['Source','MS','np2']]
    except KeyError:
        max_ms =  aov.sort_values(by=['MS'], ascending=False)[['Source','MS']]
    print(max_ms)
    return aov

for m in ['num_articles_w_keyword','num_keywords']:
    for cat in data.keys():
        print(cat)
        i1, i2, dep = prep_variables(m, data, cat)
        perform_two_way_anova(i1, i2, dep)
