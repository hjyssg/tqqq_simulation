# 写一个python随机模拟程序。每个step从-3~3范围，随机抽一个数字float。对初始值进行百分比拜变化。注意的是随机数需要符合正态分布。

import numpy as np
import matplotlib.pyplot as plt

# 设置初始值和模拟步骤数
initial_value = 1000  # 例如1000元
num_steps = 3000  # 模拟1000步

# 生成符合正态分布的随机数
mean = 0.03   
# mean = 0.06
# mean = 0
std_dev = 1  # 标准差为1
random_changes = np.random.normal(mean, std_dev, num_steps)

# 限制随机数在-3到3范围内
random_changes = np.clip(random_changes, -3, 3)

# 计算每一步的百分比变化并应用于初始值
values = [initial_value]
for change in random_changes:
    new_value = values[-1] * (1 + change / 100)
    values.append(new_value)

# 绘制结果
plt.plot(values)
plt.xlabel('Step')
plt.ylabel('Value')
plt.title('Random Walk Simulation')
plt.show()


# 只要mean大于0一点点，长期就会巨大的复利