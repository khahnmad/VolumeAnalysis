import universal_functions as uf
import matplotlib.pyplot as plt
import pandas as pd

# data = uf.import_json('initial_subsample/output/subsample_keyword_count.json')
data = uf.import_json('sample/output/sample_keyword_count.json')
partisanships = ['FarLeft', 'Left', 'CenterLeft', 'Center', 'CenterRight', 'Right', 'FarRight']
categories =['Immigration', 'Islamophobia', 'Transphobia', 'Anti-semitism']

def send_plot(cat, month, year, count,w_legend:bool=False):
    if w_legend==True:
        plt.legend()
    # plt.xticks(rotation=90)
    plt.xlabel('Partisanship')
    if count =='num_keywords':
        plt.ylabel("Number of Keywords")
        plt.title(f'Overall Number of Keywords By Partisanship ')
        # plt.title(f'Category: {cat}, Month: {month}, Year: {year}; {count} over partisanship')
    else:
        plt.ylabel("Number of Articles with Keywords")
        plt.title(f'Overall Number of Articles with Keywords By Partisanship ')
    plt.show()

def combine_data_dictionaries(data, columns):
    df = pd.DataFrame(data=data['Immigration'][1:], columns=columns)
    df['category'] = "Immigration"
    for k in list(data.keys())[1:]:
        next_df = pd.DataFrame(data=data[k][1:], columns=columns)
        next_df['category'] = k
        df = pd.concat([df, next_df])
    return df

def fetch_dataframe(category_type, data):
    columns = ['article_id', 'num_unique_kw_per_art', 'num_keywords', 'month', 'year', 'partisanship']

    if category_type == 'all':
        df = combine_data_dictionaries(data, columns)
    else:
        df = pd.DataFrame(data=data[category_type][1:], columns=columns)
    return df


def plot_count_over_partisanship(count_type:str,year:str, month:str, category:str):
    df = fetch_dataframe(category, data)


    if count_type == 'articles_w_keyword':
        if category=='all':
            if year=='all':
                if month=='all':
                    for c in categories:
                        x,y = [],[]
                        for p in partisanships:
                            v = len(df.loc[(df['category']==c) & (df['partisanship']==p) & (df['num_keywords']>0)])
                            x.append(p)
                            y.append(v)
                        plt.plot(x, y, label=c)
                    send_plot(category,month, year, count_type, w_legend=True)
                else:
                    for c in categories:
                        x,y = [],[]
                        for p in partisanships:
                            v = len(df.loc[(df['category']==c) & (df['partisanship']==p) & (df['num_keywords']>0) & (df['month']==month)])
                            x.append(p)
                            y.append(v)
                        plt.plot(x, y, label=c)
                    send_plot(category,month, year, count_type, w_legend=True)
            else:
                if month=='all':
                    for c in categories:
                        x, y = [], []
                        for p in partisanships:
                            v = len(df.loc[(df['category'] == c) & (df['partisanship'] == p) & (df['num_keywords'] > 0)
                                           & (df['year']==year)])
                            x.append(p)
                            y.append(v)
                        plt.plot(x, y, label=c)
                    send_plot(category,month, year, count_type, w_legend=True)
                else:
                    for c in categories:
                        x, y = [], []
                        for p in partisanships:
                            v = len(df.loc[(df['category'] == c) & (df['partisanship'] == p) & (df['num_keywords'] > 0) & (
                                        df['month'] == month) & (df['year']==year)])
                            x.append(p)
                            y.append(v)
                        plt.plot(x, y, label=c)
                    send_plot(category,month, year, count_type, w_legend=True)
        else:
            if year=='all':
                if month=='all':
                    x,y = [],[]
                    for p in partisanships:
                        v = len(df.loc[(df['category']==category) & (df['partisanship']==p) & (df['num_keywords']>0)])
                        x.append(p)
                        y.append(v)
                    plt.plot(x, y)
                    send_plot(category,month, year, count_type)
                else:
                    x,y = [],[]
                    for p in partisanships:
                        v = len(df.loc[(df['category']==category) & (df['partisanship']==p) & (df['num_keywords']>0) & (df['month']==month)])
                        x.append(p)
                        y.append(v)
                    plt.plot(x, y)
                    send_plot(category,month, year, count_type)
            else:
                if month=='all':
                    x, y = [], []
                    for p in partisanships:
                        v = len(df.loc[(df['category'] == category) & (df['partisanship'] == p) & (df['num_keywords'] > 0)
                                       & (df['year']==year)])
                        x.append(p)
                        y.append(v)
                    send_plot(category,month, year, count_type)
                else:
                    x, y = [], []
                    for p in partisanships:
                        v = len(df.loc[(df['category'] == category) & (df['partisanship'] == p) & (df['num_keywords'] > 0) & (
                                    df['month'] == month) & (df['year']==year)])
                        x.append(p)
                        y.append(v)
                    plt.plot(x, y)
                    send_plot(category,month, year, count_type)

    if count_type=='num_keywords':
        if category=='all':
            if year=='all':
                if month=='all':
                    for c in categories:
                        x,y = [],[]
                        for p in partisanships:
                            v = df.loc[(df['category']==c) & (df['partisanship']==p)][
                                'num_keywords'].sum()
                            x.append(p)
                            y.append(v)
                        plt.plot(x, y, label=c)
                    send_plot(category,month, year, count_type, w_legend=True)
                else:
                    for c in categories:
                        x,y = [],[]
                        for p in partisanships:
                            v = df.loc[(df['category']==c) & (df['partisanship']==p) & (df['num_keywords']>0) & (df['month']==month)][
                                'num_keywords'].sum()
                            x.append(p)
                            y.append(v)
                        plt.plot(x, y, label=c)
                    send_plot(category,month, year, count_type, w_legend=True)
            else:
                if month=='all':
                    for c in categories:
                        x, y = [], []
                        for p in partisanships:
                            v = df.loc[(df['category'] == c) & (df['partisanship'] == p) & (df['num_keywords'] > 0)
                                           & (df['year']==year)][
                                'num_keywords'].sum()
                            x.append(p)
                            y.append(v)
                        plt.plot(x, y, label=c)
                    send_plot(category,month, year, count_type, w_legend=True)
                else:
                    for c in categories:
                        x, y = [], []
                        for p in partisanships:
                            v = df.loc[(df['category'] == c) & (df['partisanship'] == p) & (df['num_keywords'] > 0) & (
                                        df['month'] == month) & (df['year']==year)][
                                'num_keywords'].sum()
                            x.append(p)
                            y.append(v)
                        plt.plot(x, y, label=c)
                    send_plot(category,month, year, count_type, w_legend=True)
        else:
            if year=='all':
                if month=='all':
                    x,y = [],[]
                    for p in partisanships:
                        v = df.loc[ (df['partisanship']==p) & (df['num_keywords']>0)][
                                'num_keywords'].sum()
                        x.append(p)
                        y.append(v)
                    plt.plot(x, y)
                    send_plot(category,month, year, count_type)
                else:
                    x,y = [],[]
                    for p in partisanships:
                        v = df.loc[(df['partisanship']==p) & (df['num_keywords']>0) & (df['month']==month)][
                                'num_keywords'].sum()
                        x.append(p)
                        y.append(v)
                    plt.plot(x, y)
                    send_plot(category, month, year, count_type)
            else:
                if month=='all':
                    x, y = [], []
                    for p in partisanships:
                        v = df.loc[(df['partisanship'] == p) & (df['num_keywords'] > 0)
                                       & (df['year']==year)][
                                'num_keywords'].sum()
                        x.append(p)
                        y.append(v)
                    plt.plot(x,y)
                    send_plot(category, month, year, count_type)
                else:
                    x, y = [], []
                    for p in partisanships:
                        v = df.loc[ (df['partisanship'] == p) & (df['num_keywords'] > 0) & (
                                    df['month'] == month) & (df['year']==year)][
                                'num_keywords'].sum()
                        x.append(p)
                        y.append(v)
                    plt.plot(x, y)
                    send_plot(category,month, year, count_type)

# Run all possible combos
# for count_type in ['num_keywords','articles_w_keyword']:
#     for year in list(range(2016,2023))+['all']:
#         for month in [1,6,'all']:
#             for category in categories+['all']:
#                 plot_count_over_partisanship(count_type, str(year), str(month), category)
#Run only comparatives
for count_type in ['num_keywords','articles_w_keyword']:
    # for year in list(range(2016,2023))+['all']:
    for year in  ['all']:
        for month in ['all']:
            # for category in categories+['all']:
            for category in ['all']:
                if category!='all' and year!='all':
                    continue
                plot_count_over_partisanship(count_type, str(year), str(month), category)