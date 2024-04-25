
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu,chi2_contingency
from statsmodels.stats.multitest import multipletests

def sigTest(data: pd.DataFrame, label: str, confoundVars: list[str], varType: list[str]):
    result_list = []  # 存储要添加到DataFrame的数据
    for var,type in zip(confoundVars,varType):
        # print(var,type)
        if type == 'scale': # 连续型，使用 Mann-Whitney U检验
            groupPos = data[data[label] == 1][var]
            groupNeg = data[data[label] == 0][var]
            # Mann-Whitney U检验, 比较两组独立样本数据之间的差异
            stat, p_val = mannwhitneyu(groupPos, groupNeg)
            result_list.append({'var': var, 'stat': stat, 'p_val': p_val})

        else: # 分组型，使用卡方检验
            # 创建一个列联表
            table = pd.crosstab(data[label], data[var])
            # 执行卡方检验
            chi2, p_val, _, _ = chi2_contingency(table)
            # 将数据添加到列表中
            result_list.append({'var': var, 'stat': chi2, 'p_val': p_val})

    # 转化成DataFrame
    resultTest = pd.DataFrame(result_list)
    # 计算 BH Q值
    # 从resultTest_var['p_val']获取p值
    p_vals = resultTest['p_val'].values

    # 找到'scale'位置的索引
    scale_index = [i for i, v in enumerate(varType) if v == 'scale']
    # 提取'scale'位置的值和其他位置的值
    pA = p_vals[scale_index]
    non_scale_index = [i for i in range(len(varType)) if i not in scale_index]
    pB = p_vals[non_scale_index]

    # 使用BH方法进行多重比较校正,按检验方法不同分别处理
    _, qA, _, _ = multipletests(pA, method='fdr_bh')
    _, qB, _, _ = multipletests(pB, method='fdr_bh')

    # 合并 qA 和 qB
    q_vals = np.empty(len(varType))
    q_vals[scale_index] = qA
    q_vals[non_scale_index] = qB

    return q_vals


# label = 'label'
def weightCalculate(data: pd.DataFrame, label: str, confoundVars: list[str], varType: list[str]):

    q_vals = sigTest(data, label, confoundVars, varType)

    # 计算缩放调整因子
    nroot = len(confoundVars) + 2
    correction = (-np.log(q_vals)) ** (1 / nroot) / np.log(20)
    weight = correction.tolist()

    return weight,q_vals


