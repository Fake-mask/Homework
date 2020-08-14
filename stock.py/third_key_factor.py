def moving_average(plot_mat):

    "plot_mat为整理后的表格。"

    mov_avg_ten = plot_mat['close'].rolling(window=10).mean()  # 计算每10天的收盘价的均值，每次向下滚动一天
    mov_avg_thirty = plot_mat['close'].rolling(window=30).mean()  # 计算每30天的收盘价的均值，每次向下滚动一天
    return mov_avg_ten, mov_avg_thirty


def plot_MA(plot_mat, mov_avg_ten, mov_avg_thirty):
    from matplotlib import pyplot as plt
    plt.plot(plot_mat.day[100:160], mov_avg_ten[100:160], label='mov_avg_ten')
    plt.plot(plot_mat.day[100:160], mov_avg_thirty[100:160], label='mov_avg_thirty')
    plt.xlabel('time')
    plt.ylabel('MA')
    plt.title('MA & time')
    plt.legend()
    plt.show()


def cal_ema(df0, period, is_dea=False): 
    '''
    df0为整理后的表格,
    is_dea用来确认是否是DEA.
    '''

    for i in range(len(df0)):
        if not is_dea:
            if i == 0:
               df0.loc[i, 'ema'+str(period)] = df0.loc[i, 'close'] #EMA初始值为当天收盘价
            else:
               df0.loc[i, 'ema'+str(period)] = (2*df0.loc[i, 'close']+(period-1)*df0.loc[i-1, 'ema'+str(period)]) / (period+1)
            ema = df0['ema'+str(period)]
        else:
            if i == 0:
               df0.loc[i, 'dea'+str(period)] = df0.loc[i, 'dif']
            else:
               df0.loc[i, 'dea'+str(period)] = ((period-1)*df0.loc[i-1, 'dea'+str(period)]+2*df0.loc[i, 'dif']) / (period+1)
            ema = df0['dea'+str(period)]
    return ema 


def cal_macd(df0, short=12, long=26, m=9):
        '''
        df0为整理后的表格,
        short,long分别指12天，26天,
        m默认为9
        '''
        short_ema = cal_ema(df0, short)  #计算12日EMA
        long_ema = cal_ema(df0, long)  #计算26日EMA
        df0['dif'] = short_ema - long_ema  #计算DIF
        dea = cal_ema(df0, m, is_dea=True)  #计算DEA  
        df0['macd'] = 2*(df0['dif'] - df0['dea'+str(m)])  #计算MACD
        return df0


def plot_macd(plot_mat):
    from matplotlib import pyplot as plt

    plt.plot(plot_mat.day[100:160], plot_mat.macd[100:160], label='macd')
    plt.xlabel('time')
    plt.ylabel('macd')
    plt.title('macd & time')
    plt.legend()
    plt.show()


def Volume(data_):

    "data_为前文深度copy所得到表格。"

    Volume = data_[['day', 'volume']].groupby(by='day').sum().reset_index()
    return Volume


def plot_Volume(plot_mat):
    from matplotlib import pyplot as plt

    plt.plot(plot_mat.day[100:160], plot_mat.volume[100:160], label='Volume')
    plt.xlabel('time')
    plt.ylabel('Volume')
    plt.title('Volume & time')
    plt.legend()
    plt.show()


def cal_rsi(df0, period=6):  # 默认周期为6日


    """
    df0为整理后的表格，
    period为周期，默认为6。
    """

    df0['diff'] = df0['close'] - df0['close'].shift(1)  # 用diff存储两天收盘价的差
    df0['diff'].fillna(0, inplace=True)  # 空值填充为0
    df0['up'] = df0['diff']  # diff赋值给up
    df0['down'] = df0['diff']  # diff赋值给down
    df0['up'][df0['up'] < 0] = 0  # 把up中小于0的置零
    df0['down'][df0['down'] > 0] = 0  #把down中大于0的置零
    df0['avg_up'] = df0['up'].rolling(period).sum() / period  #计算period天内平均上涨点数
    df0['avg_down'] = abs(df0['down'].rolling(period).sum() / period)  #计算period天内平均下降点数
    df0['avg_up'].fillna(0, inplace=True)  #空值填充为0
    df0['avg_down'].fillna(0, inplace=True)  #空值填充为0
    df0['rsi'] = 100 - 100 / (1 + (df0['avg_up'] / df0['avg_down']))  #计算RSI
    return df0  #返回原DataFrame


def plot_rsi(plot_mat):

    from matplotlib import pyplot as plt

    plt.plot(plot_mat.day[100:160], plot_mat.rsi[100:160], label='RSI')
    plt.xlabel('time')
    plt.ylabel('RSI')
    plt.title('RSI & time')
    plt.legend()
    plt.show()
#commit