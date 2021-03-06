# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from functools import reduce

import numpy as np
import pandas as pd

from QUANTAXIS.QAIndicator.QAIndicator_Series import *


"""
DataFrame 类

以下的函数都可以被直接add_func



1.	趋向指标 
又叫趋势跟踪类指标,主要用于跟踪并预测股价的发展趋势

包含的主要指标
移动平均线 MA
指数平滑移动平均线 MACD
趋向指标 DMI
瀑布线 PBX
平均线差 DMA
动力指标(动量线)  MTM
指数平均线 EXPMA
宝塔线 TWR

2.	反趋向指标
主要捕捉趋势的转折点

随机指标KDJ
乖离率 BIAS
变动速率 ROC
顺势指标 CCI
威廉指标 W&R
震荡量(变动速率) OSC
相对强弱指标 RSI
动态买卖指标 ADTM

3.	量能指标
通过成交量的大小和变化研判趋势变化
容量指标 VR
量相对强弱 VRSI
能量指标 CR
量变动速率 VROC
人气意愿指标 ARBR
成交量标准差 VSTD


4.	量价指标
通过成交量和股价变动关系分析未来趋势
震荡升降指标ASI
价量趋势PVT
能量潮OBV
量价趋势VPT
主力进出指标ABV
威廉变异离散量WVAD


5.	压力支撑指标
主要用于分析股价目前收到的压力和支撑

布林带 BOLL
麦克指标 MIKE
抛物转向 SAR
薛斯通道 XS
6.	大盘指标
通过涨跌家数研究大盘指数的走势

涨跌比率 ADR
绝对幅度指标 ABI
新三价率 TBR
腾落指数 ADL
广量冲力指标
指数平滑广量 STIX

"""


def QA_indicator_OSC(DataFrame, N=20, M=6):
    """变动速率线

    震荡量指标OSC，也叫变动速率线。属于超买超卖类指标,是从移动平均线原理派生出来的一种分析指标。

    它反应当日收盘价与一段时间内平均收盘价的差离值,从而测出股价的震荡幅度。

    按照移动平均线原理，根据OSC的值可推断价格的趋势，如果远离平均线，就很可能向平均线回归。
    """
    C = DataFrame['close']
    OS = (C - MA(C, N)) * 100
    MAOSC = EMA(OS, M)
    DICT = {'OSC': OS, 'MAOSC': MAOSC}

    return pd.DataFrame(DICT)


def QA_indicator_BBI(DataFrame, N1=3, N2=6, N3=12, N4=24):
    '多空指标'
    C = DataFrame['close']
    bbi = (MA(C, N1) + MA(C, N2) + MA(C, N3) + MA(C, N4)) / 4
    DICT = {'BBI': bbi}

    return pd.DataFrame(DICT)


def QA_indicator_PBX(DataFrame, N1=3, N2=5, N3=8, N4=13, N5=18, N6=24):
    '瀑布线'
    C = DataFrame['close']
    PBX1 = (EMA(C, N1) + EMA(C, 2 * N1) + EMA(C, 4 * N1)) / 3
    PBX2 = (EMA(C, N2) + EMA(C, 2 * N2) + EMA(C, 4 * N2)) / 3
    PBX3 = (EMA(C, N3) + EMA(C, 2 * N3) + EMA(C, 4 * N3)) / 3
    PBX4 = (EMA(C, N4) + EMA(C, 2 * N4) + EMA(C, 4 * N4)) / 3
    PBX5 = (EMA(C, N5) + EMA(C, 2 * N5) + EMA(C, 4 * N5)) / 3
    PBX6 = (EMA(C, N6) + EMA(C, 2 * N6) + EMA(C, 4 * N6)) / 3
    DICT = {'PBX1': PBX1, 'PBX2': PBX2, 'PBX3': PBX3,
            'PBX4': PBX4, 'PBX5': PBX5, 'PBX6': PBX6}

    return pd.DataFrame(DICT)


def QA_indicator_BOLL(DataFrame, N=20, P=2):
    '布林线'
    C = DataFrame['close']
    boll = MA(C, N)
    UB = boll + P * STD(C, N)
    LB = boll - P * STD(C, N)
    DICT = {'BOLL': boll, 'UB': UB, 'LB': LB}

    return pd.DataFrame(DICT)


def QA_indicator_ROC(DataFrame, N=12, M=6):
    '变动率指标'
    C = DataFrame['close']
    roc = 100 * (C - REF(C, N)) / REF(C, N)
    ROCMA = MA(roc, M)
    DICT = {'ROC': roc, 'ROCMA': ROCMA}

    return pd.DataFrame(DICT)


def QA_indicator_MTM(DataFrame, N=12, M=6):
    '动量线'
    C = DataFrame['close']
    mtm = C - REF(C, N)
    MTMMA = MA(mtm, M)
    DICT = {'MTM': mtm, 'MTMMA': MTMMA}

    return pd.DataFrame(DICT)


def QA_indicator_KDJ(DataFrame, N=9, M1=3, M2=3):
    C = DataFrame['close']
    H = DataFrame['high']
    L = DataFrame['low']

    RSV = (C - LLV(L, N)) / (HHV(H, N) - LLV(L, N)) * 100
    K = SMA(RSV, M1)
    D = SMA(K, M2)
    J = 3 * K - 2 * D
    DICT = {'KDJ_K': K, 'KDJ_D': D, 'KDJ_J': J}
    return pd.DataFrame(DICT)


def QA_indicator_MFI(DataFrame, N=14):
    """
    资金指标
    TYP := (HIGH + LOW + CLOSE)/3;
    V1:=SUM(IF(TYP>REF(TYP,1),TYP*VOL,0),N)/SUM(IF(TYP<REF(TYP,1),TYP*VOL,0),N);
    MFI:100-(100/(1+V1));
    赋值: (最高价 + 最低价 + 收盘价)/3
    V1赋值:如果TYP>1日前的TYP,返回TYP*成交量(手),否则返回0的N日累和/如果TYP<1日前的TYP,返回TYP*成交量(手),否则返回0的N日累和
    输出资金流量指标:100-(100/(1+V1))
    """
    C = DataFrame['close']
    H = DataFrame['high']
    L = DataFrame['low']
    VOL = DataFrame['volume']
    TYP = (C + H + L) / 3
    V1 = SUM(IF(TYP > REF(TYP, 1), TYP * VOL, 0), N) / \
        SUM(IF(TYP < REF(TYP, 1), TYP * VOL, 0), N)
    mfi = 100 - (100 / (1 + V1))
    DICT = {'MFI': mfi}

    return pd.DataFrame(DICT)


def QA_indicator_ATR(DataFrame, N):
    C = DataFrame['close']
    H = DataFrame['high']
    L = DataFrame['low']
    TR1 = MAX(MAX((H - L), ABS(REF(C, 1) - H)), ABS(REF(C, 1) - L))
    atr = MA(TR1, N)
    return atr


def QA_indicator_SKDJ(DataFrame, N, M):
    CLOSE = DataFrame['close']
    LOWV = LLV(DataFrame['low'], N)
    HIGHV = HHV(DataFrame['high'], N)
    RSV = EMA((CLOSE - LOWV) / (HIGHV - LOWV) * 100, M)
    K = EMA(RSV, M)
    D = MA(K, M)
    DICT = {'SKDJ_K': K, 'SKDJ_D': D}

    return pd.DataFrame(DICT)


def QA_indicator_WR(DataFrame, N, N1):
    '威廉指标'
    HIGH = DataFrame['high']
    LOW = DataFrame['low']
    CLOSE = DataFrame['close']
    WR1 = 100 * (HHV(HIGH, N) - CLOSE) / (HHV(HIGH, N) - LLV(LOW, N))
    WR2 = 100 * (HHV(HIGH, N1) - CLOSE) / (HHV(HIGH, N1) - LLV(LOW, N1))
    DICT = {'WR1': WR1, 'WR2': WR2}

    return pd.DataFrame(DICT)


def QA_indicator_BIAS(DataFrame, N1, N2, N3):
    '乖离率'
    CLOSE = DataFrame['close']
    BIAS1 = (CLOSE - MA(CLOSE, N1)) / MA(CLOSE, N1) * 100
    BIAS2 = (CLOSE - MA(CLOSE, N2)) / MA(CLOSE, N2) * 100
    BIAS3 = (CLOSE - MA(CLOSE, N3)) / MA(CLOSE, N3) * 100
    DICT = {'BIAS1': BIAS1, 'BIAS2': BIAS2, 'BIAS3': BIAS3}

    return pd.DataFrame(DICT)


def QA_indicator_RSI(DataFrame, N1=12, N2=26, N3=9):
    '相对强弱指标RSI1:SMA(MAX(CLOSE-LC,0),N1,1)/SMA(ABS(CLOSE-LC),N1,1)*100;'
    CLOSE = DataFrame['close']
    LC = REF(CLOSE, 1)
    RSI1 = SMA(MAX(CLOSE - LC, 0), N1) / SMA(ABS(CLOSE - LC), N1) * 100
    RSI2 = SMA(MAX(CLOSE - LC, 0), N2) / SMA(ABS(CLOSE - LC), N2) * 100
    RSI3 = SMA(MAX(CLOSE - LC, 0), N3) / SMA(ABS(CLOSE - LC), N3) * 100
    DICT = {'RSI1': RSI1, 'RSI2': RSI2, 'RSI3': RSI3}

    return pd.DataFrame(DICT)


def QA_indicator_ADTM(DataFrame, N, M):
    '动态买卖气指标'
    HIGH = DataFrame['high']
    LOW = DataFrame['low']
    OPEN = DataFrame['open']
    DTM = IF(OPEN <= REF(OPEN, 1), 0, MAX(
        (HIGH - OPEN), (OPEN - REF(OPEN, 1))))
    DBM = IF(OPEN >= REF(OPEN, 1), 0, MAX((OPEN - LOW), (OPEN - REF(OPEN, 1))))
    STM = SUM(DTM, N)
    SBM = SUM(DBM, N)
    ADTM1 = IF(STM > SBM, (STM - SBM) / STM,
               IF(STM == SBM, 0, (STM - SBM) / SBM))
    MAADTM = MA(ADTM1, M)
    DICT = {'ADTM': ADTM1, 'MAADTM': MAADTM}

    return pd.DataFrame(DICT)


def QA_indicator_DDI(DataFrame, N, N1, M, M1):
    '方向标准离差指数'
    H = DataFrame['high']
    L = DataFrame['low']
    DMZ = IF((H + L) <= (REF(H, 1) + REF(L, 1)), 0,
             MAX(ABS(H - REF(H, 1)), ABS(L - REF(L, 1))))
    DMF = IF((H + L) >= (REF(H, 1) + REF(L, 1)), 0,
             MAX(ABS(H - REF(H, 1)), ABS(L - REF(L, 1))))
    DIZ = SUM(DMZ, N) / (SUM(DMZ, N) + SUM(DMF, N))
    DIF = SUM(DMF, N) / (SUM(DMF, N) + SUM(DMZ, N))
    ddi = DIZ - DIF
    ADDI = SMA(ddi, N1, M)
    AD = MA(ADDI, M1)
    DICT = {'DDI': ddi, 'ADDI': ADDI, 'AD': AD}

    return pd.DataFrame(DICT)


def QA_indicator_CCI(DataFrame, N=14):
    """
    TYP:=(HIGH+LOW+CLOSE)/3;
    CCI:(TYP-MA(TYP,N))/(0.015*AVEDEV(TYP,N));
    返回一个值
    """
    typ = (DataFrame['high'] + DataFrame['low'] + DataFrame['close']) / 3
    return ((typ - MA(typ, N)) / (0.015 * AVEDEV(typ, N))).tail(1)


def QA_indicator_ASI(DataFrame, M1, M2):
    """
    LC=REF(CLOSE,1);
    AA=ABS(HIGH-LC);
    BB=ABS(LOW-LC);
    CC=ABS(HIGH-REF(LOW,1));
    DD=ABS(LC-REF(OPEN,1));
    R=IF(AA>BB AND AA>CC,AA+BB/2+DD/4,IF(BB>CC AND BB>AA,BB+AA/2+DD/4,CC+DD/4));
    X=(CLOSE-LC+(CLOSE-OPEN)/2+LC-REF(OPEN,1));
    SI=16*X/R*MAX(AA,BB);
    ASI:SUM(SI,M1);
    ASIT:MA(ASI,M2);
    """
    CLOSE = DataFrame['close']
    HIGH = DataFrame['high']
    LOW = DataFrame['low']
    OPEN = DataFrame['open']
    LC = REF(CLOSE, 1)
    AA = ABS(HIGH - LC)
    CC = ABS(HIGH - REF(LOW, 1))
    DD = ABS(LC - REF(OPEN, 1))

    # R=IF(AA>BB AND AA>CC,AA+BB/2+DD/4,IF(BB>CC AND BB>AA,BB+AA/2+DD/4,CC+DD/4))
    X = (CLOSE - LC + (CLOSE - OPEN) / 2 + LC - REF(OPEN, 1))


def QA_indicator_MA(DataFrame, N):
    CLOSE = DataFrame['close']
    return MA(CLOSE, N)


def QA_indicator_MACD(DataFrame, short=12, long=26, mid=9):
    """
    MACD CALC
    """
    CLOSE = DataFrame['close']

    DIF = EMA(CLOSE, short)-EMA(CLOSE, long)
    DEA = EMA(DIF, mid)
    MACD = (DIF-DEA)*2

    return {'DIF': DIF, 'DEA': DEA, 'MACD': MACD}


def QA_indicator_EMA(DataFrame, N):
    CLOSE = DataFrame['close']
    return EMA(CLOSE, N)


def QA_indicator_SMA(DataFrame, N):
    CLOSE = DataFrame['close']
    return SMA(CLOSE, N)


def lower_shadow(DataFrame):  # 下影线
    return abs(DataFrame.low - MIN(DataFrame.open, DataFrame.close))


def upper_shadow(DataFrame):  # 上影线
    return abs(DataFrame.high - MAX(DataFrame.open, DataFrame.close))


def body_abs(DataFrame):
    return abs(DataFrame.open - DataFrame.close)


def body(DataFrame):
    return DataFrame.close - DataFrame.open


def price_pcg(DataFrame):
    return body(DataFrame) / DataFrame.open


def amplitude(DataFrame):
    return (DataFrame.high - DataFrame.low) / DataFrame.low


# def QA_indicator_LAST(dataframe, text, N=0, M=0):
#     return len(dataframe.iloc[-N:-M, :].query(text))


# def QA_indicator_COUNT(dataframe, text, N=10):
#     """[summary]
#     函数：COUNT(X,N) 参数： X为数组，N为计算周期
#     说明：统计N周期中满足X条件的周期数,若N=0则从第一个有效值开始。
#     示例：COUNT(CLOSE>OPEN,20);表示统计20周期内收阳的周期数。
#     Arguments:
#         dataframe {[type]} -- [description]
#         text {[type]} -- [description]

#     Keyword Arguments:
#         N {[type]} -- [description] (default: {10})
#     """

#     return len(dataframe.tail(N).query(text))
