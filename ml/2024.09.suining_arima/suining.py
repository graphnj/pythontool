import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
# 设置字体为SimHei显示中文
plt.rcParams['font.sans-serif'] = ['SimSong']
# 设置正常显示符号和负号
plt.rcParams['axes.unicode_minus'] = False

# 假设Excel文件的路径是 'data.xlsx'
file_path = 'smzy3rd.xlsx'
title = '第三产业增加值预测'
xadjust=0.942188
file_path = 'smzy2nd.xlsx'
title = '第二产业增加值预测'
xadjust=0.5

file_path = 'smzy1st.xlsx'
title = '第一产业增加值预测'
xadjust=0.65

def predict_future_data(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path, engine='openpyxl')

    # 将年份设置为索引
    #df['nf'] = pd.to_datetime(df['nf'], format='%Y')  # 假设年份是以整数形式给出
    df.set_index('nf', inplace=True)

    # 按照'qy'字段分组
    grouped = df.groupby('qy')

    # 创建一个空DataFrame来保存预测结果
    forecast_results = pd.DataFrame(index=pd.RangeIndex(start=2024, stop=2027, step=1))

    for name, group in grouped:
        # 检查数据是否连续，如果有缺失的年份需要填充
        group = group.reindex(range(2013, 2025), fill_value=np.nan)

        # 使用前十年的数据进行预测
        train_data = group['zbz'].iloc[:-1]

        # 如果数据不足10个点，跳过该区域
        if len(train_data) < 10:
            continue

        # 训练ARIMA模型
        model = ARIMA(train_data, order=(1, 1, 0))  # ARIMA(p,d,q)模型
        fitted_model = model.fit()

        # 预测未来三年的数据
        forecast = fitted_model.get_forecast(steps=4)

        # 获取预测结果及其置信区间
        mean_values = forecast.predicted_mean
        forecast_ci = forecast.conf_int(alpha=0.05)
        forecast_values = forecast_ci.iloc[:, 0]+xadjust*(forecast_ci.iloc[:, 1]-forecast_ci.iloc[:, 0])
        optimistic_values = forecast_ci.iloc[:, 1]
        # 添加预测结果到DataFrame
        print(f'{name} 预测范围：{forecast_ci}')
        forecast_results[name] = forecast_values

        # 可选：绘制原始数据和预测结果
        plt.figure(figsize=(10, 5))
        plt.plot(group.index, group['zbz'], label=f'{name} - 往年数据')
        plt.plot(forecast_values.index, forecast_values, label=f'{name} - 预测值修正', marker='o')
        plt.plot(mean_values.index, mean_values, label=f'{name} - 预测值均值', marker='*')
        #plt.plot(optimistic_values.index, optimistic_values, label=f'{name} - 最乐观预测值', marker='x')

        plt.fill_between(forecast_ci.index,
                         forecast_ci.iloc[:, 0],
                         forecast_ci.iloc[:, 1], color='k', alpha=.15)

        # 在预测点处添加数值标签
        '''        for idx, value in optimistic_values.items():
            plt.annotate(f'{value:.2f}',  # 文本内容
                         xy=(idx, value),  # 注解的位置
                         xytext=(0, 5),  # 文本相对于xy的位置
                         textcoords='offset points',
                         ha='center', va='top')  # 对齐方式'''

        for idx, value in forecast_values.items():
            plt.annotate(f'{value:.2f}',  # 文本内容
                         xy=(idx, value),  # 注解的位置
                         xytext=(0, 5),  # 文本相对于xy的位置
                         textcoords='offset points',
                         ha='center', va='baseline')  # 对齐方式

        for idx, value in mean_values.items():
            plt.annotate(f'{value:.2f}',  # 文本内容
                     xy=(idx, value),  # 注解的位置
                     xytext=(0, 5),  # 文本相对于xy的位置
                     textcoords='offset points',
                     ha='center', va='bottom')  # 对齐方式

        plt.legend()
        plt.title(f'{name} {title}')
        plt.xlabel('年份')
        plt.ylabel('增加值 (亿元)')
        plt.savefig(name)
        plt.show()

    return forecast_results



# 调用函数读取并预测数据
forecast_results = predict_future_data(file_path)
print(forecast_results)