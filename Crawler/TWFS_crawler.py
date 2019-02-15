import requests
import pandas as pd
import numpy as np

def financial_statement(year, season, type='綜合損益彙總表'):

    if year >= 1000:
        year -= 1911

    if type == '綜合損益彙總表':
        url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb04'
    elif type == '資產負債彙總表':
        url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb05'
    elif type == '營益分析彙總表':
        url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb06'
    else:
        print('type does not match')

    r = requests.post(url, {
        'encodeURIComponent':1,
        'step':1,
        'firstin':1,
        'off':1,
        'TYPEK':'sii',
        'year':str(year),
        'season':str(season),
    })

    r.encoding = 'utf8'
    dfs = pd.read_html(r.text)


    for i, df in enumerate(dfs):
        df.columns = df.columns

        df.columns = df.iloc[0]
        dfs[i] = df.iloc[1:]

    df = pd.concat(dfs)
    #df = df.dropna(axis='columns')
    df = df[df['公司代號'] != '公司代號']
    df = df[~df['公司代號'].isnull()]
    return df

# financial types: '綜合損益彙總表', '資產負債彙總表', '營益分析彙總表'
for y in range(2013, 2019):
    for q in range(1, 5):
        tmp = financial_statement(y, q, '營益分析彙總表')
        tmp.to_csv('TWFS_' + str(y) + '_Q' + str(q) + '.csv', index=False)
