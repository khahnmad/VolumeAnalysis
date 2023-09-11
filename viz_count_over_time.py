import universal_functions as uf
import matplotlib.pyplot as plt
import pandas as pd

# data = uf.import_json('initial_subsample/output/subsample_keyword_count.json')

data = uf.import_json('sample/output/sample_keyword_count.json')
for k in data.keys():
    data[k] = uf.remove_duplicates(data[k])
partisanships = ['FarLeft', 'Left', 'CenterLeft', 'Center', 'CenterRight', 'Right', 'FarRight']
categories =['Immigration', 'Islamophobia', 'Transphobia', 'Anti-semitism']

def combine_data_dictionaries(data, columns):
    df = pd.DataFrame(data=data['Immigration'][1:], columns=columns)
    df['category'] = "Immigration"
    for k in list(data.keys())[1:]:
        next_df = pd.DataFrame(data=data[k][1:], columns=columns)
        next_df['category'] = k
        df = pd.concat([df, next_df])
    return df

def fetch_num_keywords_per_partisanship(df, partisanship, time_frame:str='month', cat_type:str='specified'):
    x, y = [], []
    for yr in range(2016, 2023):
        if time_frame=='year':
            if cat_type=='specified':
                v = df.loc[(df['year'] == str(yr)) & (df['partisanship'] == partisanship)][
                    'num_keywords'].sum()
            else:
                v = \
                df.loc[(df['year'] == str(yr)) & (df['partisanship'] == partisanship) & (df['category'] == cat_type)][
                    'num_keywords'].sum()
            y.append(v)
            x.append(f"{yr}")
        if time_frame == 'month':
            for m in range(1, 13):
                if cat_type=='specified':
                    # if time_frame=='month':
                    v = df.loc[(df['month'] == str(m)) & (df['year'] == str(yr)) & (df['partisanship'] == partisanship)]['num_keywords'].sum()
                    # elif time_frame=='year':
                    #     v = df.loc[(df['year'] == str(yr)) & (df['partisanship'] == partisanship)][
                    #         'num_keywords'].sum()
                else:
                    # if time_frame=='month':
                    v = df.loc[(df['month'] == str(m)) & (df['year'] == str(yr)) & (df['partisanship'] == partisanship) & (df['category']==cat_type)]['num_keywords'].sum()
                    # elif time_frame=='year':
                    #     v = df.loc[(df['year'] == str(yr)) & (df['partisanship'] == partisanship) & (df['category']==cat_type)][
                    #         'num_keywords'].sum()
                y.append(v)
                x.append(f"{m}/{yr}")
    return x, y

def fetch_num_articles_per_partisanship(df, partisanship, time_frame:str='month',cat_type:str='specified'):
    x, y = [], []
    for yr in range(2016, 2023):
        if time_frame=='year':
            if  cat_type=='specified':
                v = len(
                    df.loc[(df['year'] == str(yr)) & (df['partisanship'] == partisanship) & (
                            df['num_keywords'] > 0)])
            else:
                v = len(
                    df.loc[(df['year'] == str(yr)) & (df['partisanship'] == partisanship) & (
                            df['num_keywords'] > 0) & (df['category'] == cat_type)])

            y.append(v)
            x.append(yr)
        if time_frame == 'month':
            for m in range(1, 13):
                if cat_type=='specified':

                        v = len(df.loc[(df['month'] == str(m)) & (df['year'] == str(yr)) & (df['partisanship'] == partisanship) & (
                                    df['num_keywords'] > 0)])
                    # elif time_frame=='year':
                        # v = len(
                        #     df.loc[ (df['year'] == str(yr)) & (df['partisanship'] == partisanship) & (
                        #             df['num_keywords'] > 0)])
                else:
                    if time_frame=='month':
                        v = len(df.loc[(df['month'] == str(m)) & (df['year'] == str(yr)) & (df['partisanship'] == partisanship) & (
                                    df['num_keywords'] > 0) & (df['category']==cat_type)])
                    # elif time_frame=='year':

                y.append(v)
                x.append(f"{m}/{yr}")
    return x,y

def fetch_dataframe(category_type, data):
    columns = ['article_id', 'num_unique_kw_per_art', 'num_keywords', 'month', 'year', 'partisanship']

    if category_type == 'all':
        df = combine_data_dictionaries(data, columns)
    else:
        df = pd.DataFrame(data=data[category_type][1:], columns=columns)
    return df

def send_plot(cat, part, count,w_legend:bool=False):
    if w_legend==True:
        plt.legend()
    plt.xticks(rotation=90)
    plt.xlabel('Time')
    if count=='num_keywords':
        plt.ylabel('Number of Keywords')
    # plt.title(f'{cat}: {part} {count} over time')
        plt.title(f'Category: {cat}, Partisanship: {part} Number of Keywords Over Time By Topic')
    else:
        plt.ylabel('Number of Articles with Keywords')
        # plt.title(f'{cat}: {part} {count} over time')
        plt.title(f'Category: {cat}, Partisanship: {part} Number of Articles with Keywords Over Time By Topic')
    plt.show()


def plot_count_over_time(count_type:str,partisanship:str,time_bin:str,category:str):
    df = fetch_dataframe(category, data)

    if count_type == 'articles_w_keyword':
        if partisanship =='all':
            if category=='all':
                for c in categories:
                    y =[0,0,0,0,0,0,0]
                    for p in partisanships:
                        x, p_y = fetch_num_articles_per_partisanship(df, p, time_frame=time_bin,cat_type=c)
                        y = [sum(i) for i in zip(p_y, y)]
                    plt.plot(x, y, label=c)
                send_plot(category,partisanship, count_type, w_legend=True)
            else:
                for p in partisanships:
                    x,y = fetch_num_articles_per_partisanship(df, p,time_frame=time_bin)
                    plt.plot(x,y,label=p)
                send_plot(w_legend=True,cat=category, part=partisanship, count=count_type)
        else:
            if category =='all':
                for c in categories:
                    x,y = fetch_num_articles_per_partisanship(df, partisanship, time_frame=time_bin, cat_type=c)
                    plt.plot(x, y,label=c)
                send_plot(category, partisanship, count_type, w_legend=True)
            else:
                x,y = fetch_num_articles_per_partisanship(df, partisanship,time_frame=time_bin)
                plt.plot(x, y)
                send_plot(category, partisanship, count_type)

    if count_type=='num_keywords':
        if partisanship != 'all':
            if category =='all':
                for c in categories:
                    x,y = fetch_num_keywords_per_partisanship(df, partisanship, time_frame=time_bin, cat_type=c)
                    plt.plot(x, y,label=c)
                send_plot(category, partisanship, count_type, w_legend=True)
            else:
                x,y = fetch_num_keywords_per_partisanship(df, partisanship, time_frame=time_bin)
                plt.plot(x, y)
                send_plot(category, partisanship, count_type)
        else:
            if category=='all':
                for c in categories:
                    y =[0,0,0,0,0,0,0]
                    for p in partisanships:
                        x, p_y = fetch_num_keywords_per_partisanship(df, p, time_frame=time_bin,cat_type=c)
                        y = [sum(i) for i in zip(p_y, y)]
                    plt.plot(x, y, label=c)

                send_plot(cat=category,part=partisanship, count=count_type, w_legend=True)
            else:
                for p in partisanships:
                    x, y = fetch_num_keywords_per_partisanship(df, p, time_frame=time_bin)
                    plt.plot(x, y, label=p)
                send_plot(w_legend=True, cat=category, part=partisanship, count=count_type)


# Run all possible combos
# for ct in ['articles_w_keyword','num_keywords']:
#     for tf in ['month','year']:
#         for pt in partisanships + ['all']:
#             for ca in categories + ['all']:
#                 plot_count_over_time(ct,pt,tf,ca)

# Run only comparative graphs
# for ct in ['articles_w_keyword','num_keywords']:
#     for tf in [ 'month','year']:
#         # for pt in partisanships + ['all']:
#         for pt in  ['all']:
#             for ca in  ['all']:
#             # for ca in categories + ['all']:
#                 if pt!='all' and ca!='all':
#                     continue
#                 plot_count_over_time(ct, pt, tf, ca)
#
for ct in ['articles_w_keyword','num_keywords']:
    plot_count_over_time(ct, 'all','year','all')

# plot_count_over_time('articles_w_keyword','all','month',"Immigration")
# plot_count_over_time('articles_w_keyword','all','year',"Immigration")
# plot_count_over_time('articles_w_keyword','FarLeft','month',"Immigration")
#
# plot_count_over_time('num_keywords','FarLeft','month',"Immigration")

for p in partisanships:
    plot_count_over_time('num_keywords',p,'month','all')