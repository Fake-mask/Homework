# 移动平均线MA
def moving_average(str):
    mov_avg_ten = plot_mat[str].rolling(windows=10).mean()  # 十天的均值
    mov_avg_thirty = plot_mat[str].rolling(windows=30).mean()  # 三十天的均值


def cal_rsi(df0, period=6):  # 默认周期为6日
    df0['diff'] = df0['close']-df0['close'].shift(1)  # 用diff存储两天收盘价的差
    df0['diff'].fillna(0.inplace=True)  # 空值填充为0
    df0['up'] = df0['diff']  # diff赋值给up
    df0['down'] = df0['diff']  # diff赋值给down
    df0['up'][df0['up']<0] = 0  # 把up中小于0的置零
    df0['down'][df0['down']>0] = 0  #把down中大于0的置零
    df0['avg_up'] = df0['up'].rolling(period).sum()/period  #计算period天内平均上涨点数
    df0['avg_down'] = abs(df0['down'].rolling(period).sum()/period)  #计算period天内平均下降点数
    df0['avg_up'].fillna(0,inplace=True)  #空值填充为0
    df0['avg_down'].fillna(0,inplace=True)  #空值填充为0
    df0['rsi'] = 100-100/(1+(df0['avg_up']/df0['avg_down']))  #计算RSI
    return df0  #返回原DataFrame


def cal_ema(df0, period, is_dea=False): 
    for i in rang(len(df0)):
        if not is_dea:
            if i == 0:
               df0.loc[i, 'ema'+str(period)] = df0.loc[i, 'close'] #EMA初始值为当天收盘价
            else:
               df0.loc[i, 'ema'+str(period)] = (2*df0.loc[i, 'close']+(period-1)*df0.loc[i-1, 'ema'+str(period)])/(period+1)
        else:
           if i == 0:
               df0.loc[i, 'dea'+str(period)] = df0.loc[i, 'dif']
           else:
               df0.loc[i, 'dea'+str(period)] = ((period-1)*df0.loc[i-1, 'dea'+str(period)]+2*df0.loc[i, 'dif'])/(period+1)
           ema = df0['dea'+str(period)]
   return ema 


def cal_macd(df0, short=12, long=26, m=9):
    short_ema = cal_ema(df0, short)  #计算12日EMA
    long_ema = cal_ema(df0, long)  #计算26日EMA
    df0['dif'] = short_ema-long_ema  #计算DIF
    dea = cal_ema(df0, m, is_dea=True)  #计算DEA  
    df0['macd'] = 2*(df0['dif']-df0['dea'+str(m)])  #计算MACD
    return df0


    


