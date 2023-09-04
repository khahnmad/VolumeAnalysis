import universal_functions as uf
import pandas as pd
import matplotlib.pyplot as plt


ANTI_DF = pd.read_csv('output/Anti-semitism_Keyword_Count.csv')
IMMI_DF = pd.read_csv('output/Immigration_Keyword_Count.csv')
ISLAM_DF = pd.read_csv('output/Islamophobia_Keyword_Count.csv')
TRANS_DF = pd.read_csv('output/Transphobia_Keyword_Count.csv')
COMBO_DF = [IMMI_DF,ISLAM_DF,TRANS_DF,ANTI_DF]
CATEGORIES = ['Immigration','Islamophobia','Transphobia','Anti-semitism']
# print('')

def plot_num_article_w_keywords_by_time_partisanship(category):
    dates = ['6/2016', '12/2016', '6/2017', '12/2017', '6/2018', '12/2018', '6/2019', '12/2019', '6/2020',
             '12/2020', '6/2021', '12/2021', '6/2022', '12/2022']
    partisanships = ['FarLeft', 'Left', 'CenterLeft', 'Center', 'CenterRight', 'Right', 'FarRight']

    for p in partisanships:
        y = []
        for d in dates:
            m = int(d.split('/')[0])
            yr = int(d.split('/')[1])
            y.append(len(DF[DF['month'] <= m][DF['year'] == yr][DF['partisanship']==p]))
        plt.plot(dates, y,label=p)
    plt.xlabel('Time')
    plt.xticks(rotation=90)
    plt.ylabel('Number of Articles with a Keyword')
    plt.title(f'Number of Articles with an {category} Keyword over time')
    plt.legend()
    plt.show()


def plot_num_keywords_by_time_partisanship(category):
    dates = ['6/2016', '12/2016', '6/2017', '12/2017', '6/2018', '12/2018', '6/2019', '12/2019', '6/2020',
             '12/2020', '6/2021', '12/2021', '6/2022', '12/2022']
    partisanships = ['FarLeft', 'Left', 'CenterLeft', 'Center', 'CenterRight', 'Right', 'FarRight']

    for p in partisanships:
        y = []
        for d in dates:
            m = int(d.split('/')[0])
            yr = int(d.split('/')[1])
            y.append(sum(list(DF[DF['month'] <= m][DF['year'] == yr][DF['partisanship'] == p]['num_keywords'].values)))
        plt.plot(dates, y, label=p)
    plt.xlabel('Time')
    plt.xticks(rotation=90)
    plt.ylabel('Number of Keywords')
    plt.title(f'{category}: Number of Keywords over time ')
    plt.legend()
    plt.show()

def plot_num_articles_w_keyword_over_time():
    dates = ['1/2016', '2/2016', '3/2016', '4/2016', '5/2016', '6/2016', '7/2016', '8/2016', '9/2016', '10/2016', '11/2016', '12/2016', '1/2017', '2/2017', '3/2017', '4/2017', '5/2017', '6/2017', '7/2017', '8/2017', '9/2017', '10/2017', '11/2017', '12/2017', '1/2018', '2/2018', '3/2018', '4/2018', '5/2018', '6/2018', '7/2018', '8/2018', '9/2018', '10/2018', '11/2018', '12/2018', '1/2019', '2/2019', '3/2019', '4/2019', '5/2019', '6/2019', '7/2019', '8/2019', '9/2019', '10/2019', '11/2019', '12/2019', '1/2020', '2/2020', '3/2020', '4/2020', '5/2020', '6/2020', '7/2020', '8/2020', '9/2020', '10/2020', '11/2020', '12/2020', '1/2021', '2/2021', '3/2021', '4/2021', '5/2021', '6/2021', '7/2021', '8/2021', '9/2021', '10/2021', '11/2021', '12/2021', '1/2022', '2/2022', '3/2022', '4/2022', '5/2022', '6/2022', '7/2022', '8/2022', '9/2022', '10/2022', '11/2022', '12/2022']
    y = []
    for d in dates:
        m = int(d.split('/')[0])
        yr = int(d.split('/')[1])
        y.append(len(DF[DF['month']==m][DF['year']==yr]))
    plt.plot(dates,y)
    plt.xlabel('Time')
    plt.xticks(rotation=90)
    plt.ylabel('Number of Articles with a Keyword')
    plt.title('Number of Articles with an Immigration Keyword over time')
    plt.show()

def plot_num_keywords_over_time(category):
    dates = ['1/2016', '2/2016', '3/2016', '4/2016', '5/2016', '6/2016', '7/2016', '8/2016', '9/2016', '10/2016',
             '11/2016', '12/2016', '1/2017', '2/2017', '3/2017', '4/2017', '5/2017', '6/2017', '7/2017', '8/2017',
             '9/2017', '10/2017', '11/2017', '12/2017', '1/2018', '2/2018', '3/2018', '4/2018', '5/2018', '6/2018',
             '7/2018', '8/2018', '9/2018', '10/2018', '11/2018', '12/2018', '1/2019', '2/2019', '3/2019', '4/2019',
             '5/2019', '6/2019', '7/2019', '8/2019', '9/2019', '10/2019', '11/2019', '12/2019', '1/2020', '2/2020',
             '3/2020', '4/2020', '5/2020', '6/2020', '7/2020', '8/2020', '9/2020', '10/2020', '11/2020', '12/2020',
             '1/2021', '2/2021', '3/2021', '4/2021', '5/2021', '6/2021', '7/2021', '8/2021', '9/2021', '10/2021',
             '11/2021', '12/2021', '1/2022', '2/2022', '3/2022', '4/2022', '5/2022', '6/2022', '7/2022', '8/2022',
             '9/2022', '10/2022', '11/2022', '12/2022']
    if category=='All':
        for i in range(len(CATEGORIES)):
            DF = COMBO_DF[i]
            y = []
            for d in dates:
                m = int(d.split('/')[0])
                yr = int(d.split('/')[1])
                value = sum(list(DF[DF['month'] == m][DF['year'] == yr]['num_keywords'].values))
                y.append(value)
            plt.plot(dates, y ,label=CATEGORIES[i])
        plt.xlabel('Time')
        plt.xticks(rotation=90)
        plt.ylabel('Number of Keywords')
        plt.title(f'Number of {category} Keywords over time')
        plt.legend()
        plt.show()


    else:

        y = []
        for d in dates:
            m = int(d.split('/')[0])
            yr = int(d.split('/')[1])
            value = sum(list(DF[DF['month'] == m][DF['year'] == yr]['num_keywords'].values))
            y.append(value)
        plt.plot(dates, y)
        plt.xlabel('Time')
        plt.xticks(rotation=90)
        plt.ylabel('Number of Keywords')
        plt.title(f'Number of {category} Keywords over time')
        plt.show()


def plot_num_articles_w_keyword_over_partisanship(cat):
    partisanships = ['FarLeft', 'Left', 'CenterLeft', 'Center', 'CenterRight', 'Right', 'FarRight']
    y = []
    for p in partisanships:
        y.append(len(DF[DF['partisanship']==p]))
    plt.plot(partisanships, y)
    plt.xlabel('Partisanship')
    plt.ylabel('Number of Articles with a Keyword')
    plt.title(f'Number of Articles with an {cat} Keyword over time')
    plt.show()

def plot_num_keywords_over_partisanship():
    partisanships = ['FarLeft', 'Left', 'CenterLeft', 'Center', 'CenterRight', 'Right', 'FarRight']
    y = []
    for p in partisanships:
        y.append(sum(list(DF[DF['partisanship']==p]['num_keywords'].values)))
    plt.plot(partisanships, y)
    plt.xlabel('Partisanship')

    plt.ylabel('Number of Keywords')
    plt.title('Number of Immigration Keywords over time')
    plt.show()


plot_num_keywords_over_time('All')


plot_num_articles_w_keyword_over_partisanship('Transphobia')
plot_num_keywords_over_partisanship()
#
plot_num_articles_w_keyword_over_time()


plot_num_keywords_by_time_partisanship('Transphobia')
# plot_num_article_w_keywords_by_time_partisanship("Immigration")

