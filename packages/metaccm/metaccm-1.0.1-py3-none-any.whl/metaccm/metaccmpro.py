#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

# 自定义计算样本间距离的函数
def dist2sample(Spos, Sneg, weight):
    # 在这里实现你自定义的样本间距离计算方法
    # 找到Spos中数值型元素的位置
    numeric_positions = np.where(np.array([isinstance(val, (int, float)) for val in Spos]))[0]
    # 提取出对应位置的Spos,Sneg值
    Spos_numVar = Spos[numeric_positions]
    Sneg_numVar = Sneg[numeric_positions]

    # 找到Spos中字符型元素的位置
    str_positions = np.where(np.array([isinstance(val, str) for val in Spos]))[0]
    Spos_strVar = Spos[str_positions]
    Sneg_strVar = Sneg[str_positions]

    # 计算数值型列的差值的平方
    diff_squared = (Spos_numVar - Sneg_numVar) ** 2

    # 计算字符型列的相等情况, 相同为0，不同为1
    char_equal = (Spos_strVar != Sneg_strVar).astype(int)

    # 合并 diff_squared 和 char_equal
    combined_array = np.empty(len(Spos))
    combined_array[numeric_positions] = diff_squared
    combined_array[str_positions] = char_equal

    weight = np.array(weight)

    dist = np.dot(combined_array, weight)

    # 返回样本间距离的值
    return dist


# data=data
# sampleID='sampleID'
# label='label'
# matchVars=confoundVars
# weight=weightVars
# RequireDiffVar=RequireDiffVar
# sample='sampleID'

# help(matchingVars)
# 增加全局匹配的策略，基于距离矩阵，更能优先使距离最近的 Case-Ctrl 匹配。
def metaccmPro(data: pd.DataFrame, sample: str, label: str, matchVars: list[str], weight: list[float]):

    pos_df = data[data[label] == 1]
    neg_df = data[data[label] == 0]

    pos_df.set_index(sample, inplace=True)
    neg_df.set_index(sample, inplace=True)

    pos_df = pos_df[matchVars]
    neg_df = neg_df[matchVars]

    # 创建一个空的数据框D
    # D = pd.DataFrame(index=range(len(pos_df)), columns=range(len(neg_df)))
    # 创建空的DataFrame D，并指定行列名
    D = pd.DataFrame(index=pos_df.index, columns=neg_df.index)

    # 循环计算距离并存储
    for i in range(len(pos_df)):
        for j in range(len(neg_df)):
            # print(i, j)
            Spos = pos_df.iloc[i].values
            Sneg = neg_df.iloc[j].values

            # 计算距离
            dist = dist2sample(Spos, Sneg, weight)

            # 将距离值存储在数据框D的(i, j)位置
            D.iloc[i, j] = dist

    # 初始化保存匹配样本对的数据框
    matched_pos = pd.DataFrame()  # 阳性样本池
    matched_neg = pd.DataFrame()  # 阴性样本池

    pairs = 0  # 初始化
    matchType = 'metaccmPro'

    while not D.empty:  # 持续直到数据框 D 为空
        pairs += 1

        min_idx = np.unravel_index(np.argmin(D.values), D.shape)  # 找出最小值的索引

        # 找到对应的样本索引
        pos_sample = D.index[min_idx[0]]
        neg_sample = D.columns[min_idx[1]]

        # 将对应的样本添加到匹配的阳性和阴性样本池中
        item_pos = pd.DataFrame(pos_df.loc[pos_sample]).T  # 转换为单行 DataFrame
        item_neg = pd.DataFrame(neg_df.loc[neg_sample]).T  # 转换为单行 DataFrame

        # 添加标识列 pairs 的值
        item_pos['pairs'] = pairs
        item_neg['pairs'] = pairs

        # 将对应的样本添加到匹配的阳性和阴性样本池中
        matched_pos = pd.concat([matched_pos, item_pos])
        matched_neg = pd.concat([matched_neg, item_neg])

        # 从数据框 D 中删除已匹配的行和列
        D = D.drop(index=pos_sample, columns=neg_sample)

    # 合并正负样本对数据框并保存结果
    matched_pairs_df = pd.concat([matched_pos, matched_neg], axis=0)
    # 将索引恢复为列
    matched_pairs_df.reset_index(inplace=True)
    matched_pairs_df = matched_pairs_df.rename(columns={'index': sample})

    matched_pairs_df['matchType'] = matchType

    # 按照 pairs 顺序排列行
    balanced_data = matched_pairs_df.sort_values('pairs').reset_index(drop=True)

    return balanced_data


