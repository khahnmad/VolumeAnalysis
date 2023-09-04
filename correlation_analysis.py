# Are the other partisanships correltaed with the far right?
import numpy as np
import universal_functions as uf
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

data = uf.import_json('initial_subsample/output/subsample_keyword_count.json')
# data = uf.import_json('sample/output/sample_keyword_count.json')
partisanships = ['FarLeft', 'Left', 'CenterLeft', 'Center', 'CenterRight', 'Right', 'FarRight']
categories =['Immigration', 'Islamophobia', 'Transphobia', 'Anti-semitism']

# # Far Right, 2016 1st half, immigration, num articles with keyword
# df = pd.DataFrame(data['Immigration'][1:], columns=data['Immigration'][0])
# df['month'] = df['month'].astype(int)
# x_source = df.loc[(df['partisanship']=='FarRight') &( df['month'] <=6 ) & (df['year']=='2016')]
# y_source = df.loc[(df['partisanship']=='Center') &( df['month'] >6 ) & ( df['month'] <=12 ) & (df['year']=='2016')]
#
# x, y = [],[]
# for i in range(1,7):
#     x.append(len(x_source.loc[(x_source['num_keywords']>0) & (x_source['month']==i)]))
# for j in range(7,13):
#     y.append(len(y_source.loc[(y_source['num_keywords']>0) & (y_source['month']==j)]))
#
# plt.scatter(x,y)
# r = np.corrcoef(x, y)
# print(r)
# plt.show()

def prep_dataframe(data, category):
    df = pd.DataFrame(data[category][1:],
                      columns=['article_id', 'num_unique_kw_per_art', 'num_keywords', 'month', 'year', 'partisanship'])
    df['month'] = df['month'].astype(int)
    df['year'] = df['year'].astype(int)
    df['time_index'] = None

    count = 0
    for yr in range(2016, 2023):
        for m in range(1, 13):
            count += 1
            df.loc[(df['month'] == m) & (df['year'] == yr),'time_index']= count
            # print('')
    return df

def compare_years(category, displacement, partisanship, fr_year):
    month_range = [1, 6]
    df = pd.DataFrame(data[category][1:], columns=data[category][0])
    df['month'] = df['month'].astype(int)
    x_source = df.loc[(df['partisanship'] == 'FarRight') &
                       (df['year'] == str(fr_year))]
    y_source = df.loc[
        (df['partisanship'] == partisanship) & (df['month'] > month_range[0] + displacement) & (
                    df['month'] <= month_range[1] + displacement) & (df['year'] == '2016')]

    x, y = [list(range(1, 7)), []], [list(range(1, 7)), []]
    for i in range(1, 7):
        x[1].append(len(x_source.loc[(x_source['num_keywords'] > 0) & (x_source['month'] == i)]))
    for j in range(7, 13):
        y[1].append(len(y_source.loc[(y_source['num_keywords'] > 0) & (y_source['month'] == j)]))


    r = pearsonr(x[1], y[1])
    print(r.correlation)
    # print(r)
    if r.correlation > 0.7:
        plt.plot(x[0], x[1])
        plt.plot(y[0], y[1])
        plt.xlabel('Far Right Articles')
        plt.ylabel(f"{partisanship} Articles")
        plt.title(f"Category: {category}, Far Right + {partisanship}, diplacement={displacement} months")
        plt.show()


def compare_within_same_year(category, displacement, partisanship):
    month_range = [1,6]
    df = pd.DataFrame(data[category][1:], columns=data[category][0])
    df['month'] = df['month'].astype(int)
    x_source = df.loc[(df['partisanship'] == 'FarRight') & (df['month'] >= month_range[0])&
                      (df['month'] <= month_range[1]) & (df['year'] == '2016')]
    y_source = df.loc[
        (df['partisanship'] == partisanship) & (df['month'] > month_range[0]+displacement) & (df['month'] <= month_range[1]+displacement) & (df['year'] == '2016')]

    x, y = [list(range(1,7)),[]], [list(range(1,7)),[]]
    for i in range(1, 7):
        x[1].append(len(x_source.loc[(x_source['num_keywords'] > 0) & (x_source['month'] == i)]))
    for j in range(7, 13):
        y[1].append(len(y_source.loc[(y_source['num_keywords'] > 0) & (y_source['month'] == j)]))


    # r = np.corrcoef(x, y)
    r = pearsonr(x[1],y[1])
    print(r.correlation)
    # print(r)
    if r.correlation > 0.7:
        plt.plot(x[0], x[1])
        plt.plot(y[0],y[1])
        plt.xlabel('Far Right Articles')
        plt.ylabel(f"{partisanship} Articles")
        plt.title(f"Category: {category}, Far Right + {partisanship}, diplacement={displacement} months")
        plt.show()

def convert_to_month_yr(num):
    if num <=12:
        return num, 2016
    else:
        if num <= 24:
            return num - 12, 2017
        else:
            if num <= 36:
                return num - 24, 2018
            else:
                if num <= 48:
                    return num-36, 2019
                else:
                    if num <=60:
                        return num-48, 2020
                    else:
                        if num <=72:
                            return num-60, 2021
                        else:
                            if num <= 84:
                                return num-72, 2022


def compare_full_time_range(category, partisanship, displacement):

    df = prep_dataframe(data, category)
    x_initial_years = df.loc[(df['partisanship'] == 'FarRight') & (df['year']!=df['year'].max())]
    x_final_year = df.loc[(df['partisanship'] == 'FarRight') & (df['year']==df['year'].max()) & (df['month']<=12-displacement)]
    x_source = pd.concat([x_final_year, x_initial_years])

    y_initial_year = df.loc[(df['partisanship'] == partisanship) & (df['year'] == df['year'].min()) & (df['month']>=displacement+1)]
    y_final_years = df.loc[(df['partisanship'] == partisanship) & (df['year'] !=  df['year'].min())]
    y_source = pd.concat([y_initial_year, y_final_years])

    num_dates = (2*12)+10-displacement # while 10-2018 is the last date, complete would be (12*7)-displacement
    x, y = [list(range(num_dates)), []], [list(range(num_dates)), []]
    for i in range(1, num_dates+1):
        m, yr = convert_to_month_yr(i)
        x[1].append(len(x_source.loc[(x_source['num_keywords'] > 0) & (x_source['month'] == m) & (x_source['year']==yr)]))
    for j in range(displacement+1, num_dates+displacement+1):
        m, yr = convert_to_month_yr(j)
        y[1].append(len(y_source.loc[(y_source['num_keywords'] > 0) & (y_source['month'] == m) & (y_source['year']==yr)]))


    r = pearsonr(x[1], y[1])


    if r.correlation > 0.7:
        print(f"Category: {category}, Far Right + {partisanship}, diplacement={displacement} months")
        print(r.correlation)
        plt.plot(x[0], x[1],label='FarRight')
        plt.plot(y[0], y[1],label=p)
        plt.xlabel('Time in months')
        plt.ylabel(f"Number of Articles with Keywords")
        plt.legend()
        plt.title(f"Category: {category}, Far Right + {partisanship}, diplacement={displacement} months")
        plt.show()

def compare_partial_timeframe(timeframe:int, category, start_time,displacement, part):

    df = prep_dataframe(data, category)
    x_source = df.loc[(df['partisanship'] == 'FarRight') & (df['time_index'] >= start_time) & (df['time_index'] <= timeframe+start_time)]

    y_source =df.loc[(df['partisanship'] == part) & (df['time_index'] >= start_time+displacement) & (df['time_index'] <= timeframe+start_time+displacement)]

    num_dates = (2 * 12) + 10 - displacement  # while 10-2018 is the last date, complete would be (12*7)-displacement
    x, y = [list(range(1,timeframe+1)), []], [list(range(1,timeframe+1)), []]
    for i in range(start_time, timeframe+start_time):

        x[1].append(
            len(x_source.loc[(x_source['num_keywords'] > 0) & (x_source['time_index'] == i) ]))
    for j in range(start_time+displacement,timeframe+start_time+displacement):
        y[1].append(
            len(y_source.loc[(y_source['num_keywords'] > 0) & (y_source['time_index'] == j)]))

    r = pearsonr(x[1], y[1])

    if r.correlation > 0.7:
        # print(f"Category: {category}, Far Right + {part}, diplacement={displacement} months, timeframe={timeframe} months, starting={start_time}")
        # print(r.correlation)
        # plt.plot(x[0], x[1], label='FarRight')
        # plt.plot(y[0], y[1], label=part)
        # plt.xlabel('Time in months')
        # plt.ylabel(f"Number of Articles with Keywords")
        # plt.legend()
        # plt.title(f"Category: {category}, Far Right + {part}, diplacement={displacement} months, timeframe={timeframe} months, starting={start_time}")
        # plt.show()
        return [displacement,category,part, timeframe, start_time,r.correlation,r.pvalue]
    return None

# Full time frame
# for cat in categories:
#     for p in partisanships:
#         for d in range(1,13):
#             compare_full_time_range(cat,p,d)
#
# import pandas as pd
from collections import Counter
df = pd.read_csv('subsample_partial_correlation_analysis.csv')
corre_analysis = uf.import_csv('subsample_partial_correlation_analysis.csv')

def find_frequent_partisanship_diplacement_pairs(data):
    dp_pairs = [f"{x[0]} {x[2]}" for x in data]
    counter = Counter(dp_pairs)
    mc = counter.most_common(10)
    outcome = []
    for elt in mc:
        split_ = elt[0].split(' ')
        outcome.append(split_)
    return outcome

def find_freq_part_displacement_cate_pairs(data):
    dp_pairs = [f"{x[0]} {x[1]} {x[2]}" for x in data]
    counter = Counter(dp_pairs)
    mc = counter.most_common(10)
    outcome = []
    for elt in mc:
        split_ = elt[0].split(' ')
        outcome.append(split_)
    return outcome

def find_freq_part_displacement_cate_tf_pairs(data):
    dp_pairs = [f"{x[0]} {x[1]} {x[2]} {x[3]}" for x in data]
    counter = Counter(dp_pairs)
    mc = counter.most_common(10)
    outcome = []
    for elt in mc:
        split_ = elt[0].split(' ')
        outcome.append(split_)
    return outcome

pd_pairs = find_frequent_partisanship_diplacement_pairs(corre_analysis)
pdct_pairs = find_freq_part_displacement_cate_tf_pairs(corre_analysis)
results = []
for pair in pdct_pairs:
    for st in range(1, 79):
        outcome = compare_partial_timeframe(timeframe=int(pair[3]), category=pair[1], start_time=st,displacement=int(pair[0]),part=pair[2])
        if outcome:
            results.append(outcome)
uf.export_nested_list(f"PDCT_pairs.csv",results)
y = find_freq_part_displacement_cate_pairs(corre_analysis)
print('')

# Conduct follow up analysis
for tf in [3,6,9,12]:
    for st in range(1,48):
        for cat in categories:
            for p in partisanships:
                for d in range(1,6):
                    outcome = compare_partial_timeframe(timeframe=tf, category=cat, start_time=st,displacement=d,part=p)
                    if outcome:
                        results.append(outcome)

# # Partial tiem frames
# results = [['displacement','category','partisanship','timeframe','starttime','correlation','pvalue']]
# for tf in [3,6,9,12]:
#     for st in range(1,48):
#         for cat in categories:
#             for p in partisanships:
#                 for d in range(1,6):
#                     outcome = compare_partial_timeframe(timeframe=tf, category=cat, start_time=st,displacement=d,part=p)
#                     if outcome:
#                         results.append(outcome)
# uf.export_nested_list('subsample_partial_correlation_analysis.csv',results)

# > year time_frame
# , for cat in categories:
#     for p in partisanships:
#         print(p)
#         for i in range(1,7):
#             print(i)
#             compare_within_same_year(cat,i, p)
