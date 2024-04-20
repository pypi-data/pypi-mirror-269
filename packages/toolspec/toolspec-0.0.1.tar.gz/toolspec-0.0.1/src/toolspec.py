# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from tqdm import tqdm


def feature_processing(data, var_list, lbound, ubound, fill_else=np.nan, decimal=3):
    def limit(x):
        return x if x >= lbound and x <= ubound else fill_else
    for var in tqdm(var_list):
        data[var] = data[var].apply(limit).round(decimal)

def target_processing(data, target_region, fill_na=0, fill_else=np.nan):
    for target in target_region.keys():
        region = target_region[target]
        data[target].fillna(fill_na,inplace=True)
        data.loc[~data.query(region).index, target] = fill_else

def metric_ks_auc(data, var_list, target_list, weight=None, partition=None, ascending=None):
    if partition:
        if type(partition) != list:
            partition = [partition]
    index_list = []
    for target in target_list:
        data['Bad_%s' % target] = (data[target] - data[target].min()) / (data[target].max() - data[target].min())
        data['Good_%s' % target] = (data[target].max() - data[target]) / (data[target].max() - data[target].min())
        if weight:
            data['Bad_%s' % target] = data['Bad_%s' % target] * data[weight]
            data['Good_%s' % target] = data['Good_%s' % target] * data[weight]
        index_list += ['%s_%s' % (index,target) for index in ['Bad','Good']]
    perf_tbl = pd.DataFrame()
    for var in var_list:
        if partition:
            grouped = data.groupby(by=partition+[var],as_index=False)[index_list].sum()
            grouped.sort_values(by=partition+[var],ascending=False,inplace=True)
            result = data.groupby(by=partition,as_index=False)[var].count()
            for target in target_list:
                grouped[['CumBad_%s' % target,'CumGood_%s' % target]] = grouped[['Bad_%s' % target,'Good_%s' % target]].groupby(by=partition).cumsum()
                grouped['PctCumBad_%s' % target] = grouped['CumBad_%s' % target] / grouped['Bad_%s' % target].sum()
                grouped['PctCumGood_%s' % target] = grouped['CumGood_%s' % target] / grouped['Good_%s' % target].sum()
                grouped[['PctCumBadLst_%s' % target,'PctCumGoodLst_%s' % target]] = grouped[['PctCumBad_%s' % target,'PctCumGood_%s' % target]].groupby(by=partition).shift(1).fillna(0)
                grouped['+KS_%s' % target] = grouped['PctCumBad_%s' % target] - grouped['PctCumGood_%s' % target]
                grouped['-KS_%s' % target] = - grouped['+KS_%s' % target]
                grouped['+AUC_%s' % target] = (grouped['PctCumGood_%s' % target] - grouped['PctCumGoodLst_%s' % target]) * (grouped['PctCumBad_%s' % target] + grouped['PctCumBadLst_%s' % target]) / 2
                grouped['-AUC_%s' % target] = grouped['PctCumGood_%s' % target] - grouped['PctCumGoodLst_%s' % target] - grouped['+AUC_%s' % target]
                result = result.merge(grouped.groupby(by=partition,as_index=False)[['+KS_%s' % target,'-KS_%s' % target]].max(), how='left', on=partition)
                result = result.merge(grouped.groupby(by=partition,as_index=False)[['+AUC_%s' % target,'-AUC_%s' % target]].sum(), how='left', on=partition)
                if ascending == True:
                    result['KS_%s' % target] = result['+KS_%s' % target]
                    result['AUC_%s' % target] = result['+AUC_%s' % target]
                elif ascending == False:
                    result['KS_%s' % target] = result['-KS_%s' % target]
                    result['AUC_%s' % target] = result['-AUC_%s' % target]
                else:
                    result['KS_%s' % target] = result[['+KS_%s' % target,'-KS_%s' % target]].apply(max,axis=1)
                    result['AUC_%s' % target] = result[['+AUC_%s' % target,'-AUC_%s' % target]].apply(max,axis=1)
            result['var'] = var
            result = result[['var']+partition+['KS_%s' % target for target in target_list]+['AUC_%s' % target for target in target_list]]
        else:
            grouped = data.groupby(by=var,as_index=False)[index_list].sum()
            grouped.sort_values(by=var,ascending=False,inplace=True)
            result = [var]
            columns = ['var']
            for target in target_list:
                grouped[['CumBad_%s' % target,'CumGood_%s' % target]] = grouped[['Bad_%s' % target,'Good_%s' % target]].cumsum()
                grouped['PctCumBad_%s' % target] = grouped['CumBad_%s' % target] / grouped['Bad_%s' % target].sum()
                grouped['PctCumGood_%s' % target] = grouped['CumGood_%s' % target] / grouped['Good_%s' % target].sum()
                grouped[['PctCumBadLst_%s' % target,'PctCumGoodLst_%s' % target]] = grouped[['PctCumBad_%s' % target,'PctCumGood_%s' % target]].shift(1).fillna(0)
                grouped['+KS_%s' % target] = grouped['PctCumBad_%s' % target] - grouped['PctCumGood_%s' % target]
                grouped['-KS_%s' % target] = - grouped['+KS_%s' % target]
                grouped['+AUC_%s' % target] = (grouped['PctCumGood_%s' % target] - grouped['PctCumGoodLst_%s' % target]) * (grouped['PctCumBad_%s' % target] + grouped['PctCumBadLst_%s' % target]) / 2
                grouped['-AUC_%s' % target] = grouped['PctCumGood_%s' % target] - grouped['PctCumGoodLst_%s' % target] - grouped['+AUC_%s' % target]
                if ascending == True:
                    result.append(grouped['+KS_%s' % target].max())
                    result.append(grouped['+AUC_%s' % target].sum())
                elif ascending == False:
                    result.append(grouped['-KS_%s' % target].max())
                    result.append(grouped['-AUC_%s' % target].sum())
                else:
                    result.append(grouped[['+KS_%s' % target,'-KS_%s' % target]].max().max())
                    result.append(grouped[['+AUC_%s' % target,'-AUC_%s' % target]].sum().max())
                columns += ['KS_%s' % target,'AUC_%s' % target]
            result = pd.DataFrame(columns=columns, data=[result])
        perf_tbl = perf_tbl.append(result,ignore_index=True)
    return perf_tbl

def cutoff_single(data, var_list, target_list, weight=None):
    index_list = []
    for target in target_list:
        data['Cnt_%s' % target] = 1 * (data[target] >= 0)
        if weight:
            data['Total_%s' % target] = data[weight] * (data[target] >= 0)
            data['Bad_%s' % target] = data[weight] * (data[target] == 1)
        else:
            data['Total_%s' % target] = 1 * (data[target] >= 0)
            data['Bad_%s' % target] = 1 * (data[target] == 1)
        data['Good_%s' % target] = data['Total_%s' % target] - data['Bad_%s' % target]
        index_list += ['%s_%s' % (index,target) for index in ['Cnt','Total','Bad','Good']]
    for var in var_list:
        grouped = data.groupby(by=var,as_index=False)[index_list].sum()
        grouped['cutoff'] = (grouped[var] + grouped[var].shift(-1)) / 2
        grouped[['Cum%s' % index for index in index_list]] = grouped[index_list].cumsum()
        for target in target_list:
            grouped['PctCumCnt_%s' % target] = grouped['CumCnt_%s' % target] / grouped['Cnt_%s' % target].sum()
            grouped['PctCumTotal_%s' % target] = grouped['CumTotal_%s' % target] / grouped['Total_%s' % target].sum()
            grouped['PctCumBad_%s' % target] = grouped['CumBad_%s' % target] / grouped['Bad_%s' % target].sum()
            grouped['PctCumGood_%s' % target] = grouped['CumGood_%s' % target] / grouped['Good_%s' % target].sum()
            grouped['Cnt_a_%s' % target] = grouped['CumCnt_%s' % target]
            grouped['Cnt_b_%s' % target] = grouped['CumCnt_%s' % target].max() - grouped['CumCnt_%s' % target]
            grouped['PctCnt_a_%s' % target] = grouped['PctCumCnt_%s' % target]
            grouped['PctCnt_b_%s' % target] = grouped['PctCumCnt_%s' % target].max() - grouped['PctCumCnt_%s' % target]
            grouped['PctTotal_a_%s' % target] = grouped['PctCumTotal_%s' % target]
            grouped['PctTotal_b_%s' % target] = grouped['PctCumTotal_%s' % target].max() - grouped['PctCumTotal_%s' % target]
            grouped['Badrate_a_%s' % target] = grouped['CumBad_%s' % target] / grouped['CumTotal_%s' % target]
            grouped['Badrate_b_%s' % target] = (grouped['CumBad_%s' % target].max()-grouped['CumBad_%s' % target]) / (grouped['CumTotal_%s' % target].max()-grouped['CumTotal_%s' % target])
            grouped['Entropy_a_%s' % target] = - grouped['Badrate_a_%s' % target] * np.log(grouped['Badrate_a_%s' % target]) - (1-grouped['Badrate_a_%s' % target]) * np.log(1-grouped['Badrate_a_%s' % target])
            grouped['Entropy_b_%s' % target] = - grouped['Badrate_b_%s' % target] * np.log(grouped['Badrate_b_%s' % target]) - (1-grouped['Badrate_b_%s' % target]) * np.log(1-grouped['Badrate_b_%s' % target])
            grouped['EntropyNew_%s' % target] = grouped['Entropy_a_%s' % target] * grouped['PctTotal_a_%s' % target] + grouped['Entropy_b_%s' % target] * grouped['PctTotal_b_%s' % target]
            grouped['BadrateAll_%s' % target] = grouped['CumBad_%s' % target].max() / grouped['CumTotal_%s' % target].max()
            grouped['EntropyOld_%s' % target] = - grouped['BadrateAll_%s' % target] * np.log(grouped['BadrateAll_%s' % target]) - (1-grouped['BadrateAll_%s' % target]) * np.log(1-grouped['BadrateAll_%s' % target])
            grouped['Gain_%s' % target] = grouped['EntropyOld_%s' % target] - grouped['EntropyNew_%s' % target]
        grouped['Gain'] = grouped[['Gain_%s' % target for target in target_list]].apply(max,axis=1)
        grouped.sort_values(by='Gain',ascending=False,inplace=True)
        cutoff = grouped.iloc[0]
    return cutoff

def woebin(data, var_list, target, cnt_min=100, pct_min=0.05, gain_min=0.001, index='Entropy', ascending=None):
    bin_tbl = pd.DataFrame(columns=['var','bin','bucket','lbound','ubound','Total','Bad','Good','PctTotal','Badrate','WOE','IV'])
    for var in var_list:
        grouped = data.groupby(by=var,as_index=False)[target].agg({'Total':'count','Bad':'sum'})
        grouped['cutoff'] = (grouped[var] + grouped[var].shift(-1)) / 2
        grouped.eval('Good = Total - Bad',inplace=True)
        grouped[['CumTotal','CumBad','CumGood']] = grouped[['Total','Bad','Good']].cumsum()
        grouped['PctCumTotal'] = grouped['CumTotal'] / grouped['Total'].sum()
        grouped['PctCumBad'] = grouped['CumBad'] / grouped['Bad'].sum()
        grouped['PctCumGood'] = grouped['CumGood'] / grouped['Good'].sum()
        grouped[['CumTotalLst','CumBadLst','CumGoodLst']] = grouped[['CumTotal','CumBad','CumGood']].shift(1).fillna(0)
        grouped[['PctCumTotalLst','PctCumBadLst','PctCumGoodLst']] = grouped[['PctCumTotal','PctCumBad','PctCumGood']].shift(1).fillna(0)
        intervals = []
        badrates = [grouped['Bad'].sum()/grouped['Total'].sum()]
        index = 0
        while index <= len(intervals):
            lbound = -np.inf if index == 0 else intervals[index-1]
            ubound = np.inf if index == len(intervals) else intervals[index]
            tmp = grouped[(grouped[var] >= lbound) & (grouped[var] <= ubound)].copy()
            tmp['Total_a'] = tmp['CumTotal'] - tmp['CumTotalLst'].min()
            tmp['Total_b'] = tmp['CumTotal'].max() - tmp['CumTotal']
            tmp['PctTotal_a'] = tmp['PctCumTotal'] - tmp['PctCumTotalLst'].min()
            tmp['PctTotal_b'] = tmp['PctCumTotal'].max() - tmp['PctCumTotal']
            tmp['PctBad_a'] = tmp['PctCumBad'] - tmp['PctCumBadLst'].min()
            tmp['PctBad_b'] = tmp['PctCumBad'].max() - tmp['PctCumBad']
            tmp['PctGood_a'] = tmp['PctCumGood'] - tmp['PctCumGoodLst'].min()
            tmp['PctGood_b'] = tmp['PctCumGood'].max() - tmp['PctCumGood']
            tmp['Badrate_a'] = (tmp['CumBad']-tmp['CumBadLst'].min()) / (tmp['CumTotal']-tmp['CumTotalLst'].min())
            tmp['Badrate_b'] = (tmp['CumBad'].max()-tmp['CumBad']) / (tmp['CumTotal'].max()-tmp['CumTotal'])
            tmp['Entropy_a'] = - tmp['Badrate_a'] * np.log(tmp['Badrate_a']) - (1-tmp['Badrate_a']) * np.log(1-tmp['Badrate_a'])
            tmp['Entropy_b'] = - tmp['Badrate_b'] * np.log(tmp['Badrate_b']) - (1-tmp['Badrate_b']) * np.log(1-tmp['Badrate_b'])
            tmp['EntropyNew'] = tmp['Entropy_a'] * tmp['PctTotal_a'] + tmp['Entropy_b'] * tmp['PctTotal_b']
            tmp['BadrateAll'] = (tmp['CumBad'].max()-tmp['CumBadLst'].min()) / (tmp['CumTotal'].max()-tmp['CumTotalLst'].min())
            tmp['EntropyOld'] = - tmp['BadrateAll'] * np.log(tmp['BadrateAll']) - (1-tmp['BadrateAll']) * np.log(1-tmp['BadrateAll'])
            tmp['GainEnt'] = tmp['EntropyOld'] - tmp['EntropyNew']
            tmp['IV_Old'] = (tmp['PctCumBad'].max()-tmp['PctCumBadLst'].min()-tmp['PctCumGood'].max()+tmp['PctCumGoodLst'].min()) * np.log((tmp['PctCumBad'].max()-tmp['PctCumBadLst'].min())/(tmp['PctCumGood'].max()-tmp['PctCumGoodLst'].min()))
            tmp['IV_New'] = (tmp['PctBad_a']-tmp['PctGood_a']) * np.log(tmp['PctBad_a']/tmp['PctGood_a']) + (tmp['PctBad_b']-tmp['PctGood_b']) * np.log(tmp['PctBad_b']/tmp['PctGood_b'])
            tmp['GainIV'] = tmp['IV_Old'] - tmp['IV_All']
            tmp['Gain'] = tmp['GainEnt'] * (index == 'Entropy') + tmp['GainIV'] * (index == 'IV')
            tmp = tmp[(tmp['Total_a'] > cnt_min) & (tmp['Total_b'] > cnt_min)]
            tmp = tmp[(tmp['PctTotal_a'] > pct_min) & (tmp['PctTotal_b'] > pct_min)]
            tmp = tmp[(tmp['Gain'] > gain_min) & (tmp['Gain'] < np.inf)]
            if ascending == True:
                tmp = tmp[tmp['Badrate_a'] < tmp['Badrate_b']]
                if index > 0:
                    tmp = tmp[tmp['Badrate_a'] > badrates[index-1]]
                if index < len(intervals):
                    tmp = tmp[tmp['Badrate_b'] < badrates[index+1]]
            elif ascending == False:
                tmp = tmp[tmp['Badrate_a'] > tmp['Badrate_b']]
                if index > 0:
                    tmp = tmp[tmp['Badrate_a'] < badrates[index-1]]
                if index < len(intervals):
                    tmp = tmp[tmp['Badrate_b'] > badrates[index+1]]
            if not tmp.empty:
                cutoff = tmp.sort_values(by='Gain',ascending=False).iloc[0]
                intervals.insert(index,cutoff['cutoff'])
                badrates[index] = cutoff['Badrate_b']
                badrates.insert(index,cutoff['Badrate_a'])
            else:
                index += 1
        intervals.insert(0,-np.inf)
        intervals.append(np.inf)
        grouped['bucket'] = np.cut(grouped[var],intervals,include_lowest=True)
        grouped = grouped.groupby(by='bucket',as_index=False)[['Total','Bad','Good']].sum()
        grouped['PctTotal'] = grouped['Total'] / grouped['Total'].sum()
        grouped['Badrate'] = grouped['Bad'] / grouped['Total']
        grouped['WOE'] = np.log((grouped['Bad']/grouped['Bad'].sum())/(grouped['Good']/grouped['Good'].sum()))
        grouped['IV'] = (grouped['Bad']/grouped['Bad'].sum()-grouped['Good']/grouped['Good'].sum()) * grouped['WOE']
        grouped['var'] = var
        grouped['bin'] = grouped.index + 1
        grouped['bucket'] = grouped['bucket'].apply(lambda x : str(x).strip().replace('inf]','inf)'))
        grouped['lbound'] = grouped['bucket'].apply(lambda x : str(x).split(',')[0].replace('(','').replace('[',''))
        grouped['ubound'] = grouped['bucket'].apply(lambda x : str(x).split(',')[1].replace(')','').replace(']',''))
        bin_tbl = bin_tbl.append(grouped[['var','bin','bucket','lbound','ubound','Total','Bad','Good','PctTotal','Badrate','WOE','IV']])
    iv_tbl = bin_tbl.groupby(by='var',as_index=False)['IV'].agg({'bins':'count','IV':'sum'}).sort_values(by='IV',ascending=False).reset_index().rename(columns={'index':'id'})
    bin_tbl = bin_tbl.merge(iv_tbl[['var','id']], how='left', on='var').sort_values(by=['id','bin']).drop(columns='id').reset_index(drop=True)
    return iv_tbl, bin_tbl

def raw2woe(data, var_list, bin_tbl):
    woe_data = data[var_list].copy()
    for var in var_list:
        bin_tmp = bin_tbl[bin_tbl['var'] == var].copy()
        if not bin_tmp.empty:
            woe_data[var] = 0
            for i in range(bin_tmp.shape[0]):
                value = bin_tmp.iloc[i]
                woe_data[var] = woe_data[var] + value['WOE'] * (data[var] > float(value['lbound'])) * (data[var] <= float(value['ubound']))
    return woe_data

def createcard(res, bin_tbl, point0=660, odds0=1/15, pdo=15, reverse=False):
    B = pdo / np.log(2) * (-1 if reverse == True else 1)
    A = point0 + B * np.log(odds0)
    bp = A + B * res.params[0]
    scoring_table = bin_tbl.merge(pd.DataFrame(columns=['coef'],data=res.params).reset_index().rename(columns={'index':'var'}), how='inner', on='var')
    scoring_table['score_org'] = - scoring_table['WOE'] * scoring_table['coef'] * B
    grouped = scoring_table.groupby(by='var',as_index=False)['score'].min()
    bp_amort = (bp + grouped['score'].sum()) / grouped['score'].count()
    scoring_table = scoring_table.merge(grouped.rename(columns={'score':'score_min'}), how='left', on='var')
    scoring_table['score'] = (scoring_table['score_org'] - scoring_table['score_min'] + bp_amort).apply(int)
    return scoring_table




