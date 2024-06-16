import pandas as pd
import os
import sys
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler

# 将util.py所在的目录添加到系统路径中，以便导入_util模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _util

# 加载数据
data = _util.load_csv_as_dataframe("^NDX.csv")  # data is dataframe

# 将Date列转换为datetime格式，并设置为索引
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# 使用resample函数将数据按月重采样，并聚合成月线级别数据
monthly_data = data.resample('M').agg({
    'Open': 'first',       # 每个月的开盘价
    'High': 'max',         # 每个月的最高价
    'Low': 'min',          # 每个月的最低价
    'Close': 'last',       # 每个月的收盘价
    'Adj Close': 'last',   # 每个月的调整收盘价
    'Volume': 'sum'        # 每个月的成交量总和
}).dropna()

# 选择需要的特征，这里只使用收盘价
dataset = monthly_data[['Close']].values

# 使用MinMaxScaler将数据归一化到[0, 1]区间
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

# 创建数据集
def create_dataset(data, time_step=1):
    X, Y = [], []
    for i in range(len(data) - time_step):
        X.append(data[i:(i + time_step), 0])
        Y.append(data[i + time_step, 0])
    return np.array(X), np.array(Y)

time_step = 90  # 使用过去90天的数据来预测
X, y = create_dataset(scaled_data, time_step)

# 重塑输入数据为 LSTM 所需的格式 [samples, time steps, features]
X = X.reshape(X.shape[0], X.shape[1], 1)

# 创建 LSTM 模型
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))  # 第一层LSTM，返回序列
model.add(LSTM(50, return_sequences=False))  # 第二层LSTM，不返回序列
model.add(Dense(25))  # 全连接层，包含25个神经元
model.add(Dense(1))  # 输出层，预测一个值

# 编译模型，使用adam优化器和均方误差损失函数
model.compile(optimizer='adam', loss='mean_squared_error')

# 训练模型，使用全部数据，批大小为1，训练20个周期
model.fit(X, y, batch_size=1, epochs=20)

# 使用模型预测接下来的三个月
last_data = scaled_data[-time_step:]  # 取最后time_step个数据
next_predictions = []

for _ in range(3):
    last_data_reshaped = last_data.reshape((1, time_step, 1))
    next_pred = model.predict(last_data_reshaped)
    next_predictions.append(next_pred[0, 0])
    last_data = np.append(last_data, next_pred)[-time_step:]

# 反归一化预测值，将它们转换回原始范围
next_predictions = scaler.inverse_transform(np.array(next_predictions).reshape(-1, 1))

# 打印预测结果
print("Next 3 months predictions (Close prices):")
print(next_predictions)

# 绘图
plt.figure(figsize=(14, 8))
plt.plot(scaler.inverse_transform(scaled_data), label='Original Data')  # 原始数据
plt.plot(np.arange(len(scaled_data), len(scaled_data) + 3), next_predictions, label='Next 3 Months Predictions', color='red')  # 预测数据
plt.legend()
plt.show()
