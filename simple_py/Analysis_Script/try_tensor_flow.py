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

# 将数据分为训练集和测试集，训练集占80%
train_size = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_size]
test_data = scaled_data[train_size:]

# 定义一个函数来创建数据集
# time_step是LSTM网络的时间步长，即每次用多少天的数据来预测下一天的数据
def create_dataset(data, time_step=1):
    X, Y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step), 0])
        Y.append(data[i + time_step, 0])
    return np.array(X), np.array(Y)

time_step = 90  # 时间步长，可以调整
X_train, y_train = create_dataset(train_data, time_step)
X_test, y_test = create_dataset(test_data, time_step)

# 重塑输入数据为 LSTM 所需的格式 [samples, time steps, features]
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# 创建 LSTM 模型
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))  # 第一层LSTM，返回序列
model.add(LSTM(50, return_sequences=False))  # 第二层LSTM，不返回序列
model.add(Dense(25))  # 全连接层，包含25个神经元
model.add(Dense(1))  # 输出层，预测一个值

# 编译模型，使用adam优化器和均方误差损失函数
model.compile(optimizer='adam', loss='mean_squared_error')

# 训练模型，使用训练集，批大小为1，训练20个周期
model.fit(X_train, y_train, batch_size=1, epochs=20)

# 进行预测
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

# 反归一化预测值，将它们转换回原始范围
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)
y_train = scaler.inverse_transform(y_train.reshape(-1, 1))
y_test = scaler.inverse_transform(y_test.reshape(-1, 1))

# 计算RMSE（均方根误差），衡量预测值与实际值之间的差距
train_rmse = np.sqrt(np.mean(((train_predict - y_train) ** 2)))
test_rmse = np.sqrt(np.mean(((test_predict - y_test) ** 2)))
print(f'Train RMSE: {train_rmse}')
print(f'Test RMSE: {test_rmse}')

# 创建一个数组，用于绘制训练集预测结果
train_plot = np.empty_like(dataset)
train_plot[:, :] = np.nan
train_plot[time_step:len(train_predict) + time_step, :] = train_predict

# 创建一个数组，用于绘制测试集预测结果
test_plot = np.empty_like(dataset)
test_plot[:, :] = np.nan
test_plot[len(train_predict) + (time_step * 2) + 1:len(dataset) - 1, :] = test_predict

# 绘制原始数据与预测数据的对比图
plt.figure(figsize=(14, 8))
plt.plot(scaler.inverse_transform(scaled_data), label='Original Data')  # 原始数据
plt.plot(train_plot, label='Train Prediction')  # 训练集预测数据
plt.plot(test_plot, label='Test Prediction')  # 测试集预测数据
plt.legend()
plt.show()
