import pandas as pd
import os
import matplotlib.pyplot as plt
import sys
from datetime import datetime, timedelta

# 确保路径正确，导入 _util
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将util.py所在的目录添加到系统路径中
import _util

# 加载数据
data = _util.load_csv_as_dataframe("^SPX.csv")  # data is dataframe



# 确定阿波罗登月日期
apollo_landing_date = datetime(1969, 7, 20)

# 确定登月前后6个月的时间范围
start_date = apollo_landing_date - timedelta(days=12*30)
end_date = apollo_landing_date + timedelta(days=12*30)

# 转换数据中的日期格式
data['Date'] = pd.to_datetime(data['Date'])

# 筛选时间范围内的数据
filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

# 绘制图表
plt.figure(figsize=(14, 7))
plt.plot(filtered_data['Date'], filtered_data['Close'], label='收盘价')
plt.axvline(x=apollo_landing_date, color='r', linestyle='--', label='阿波罗登月日期')

# 避免乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

plt.xlabel('日期')
plt.ylabel('收盘价')
plt.title('阿波罗登月前后6个月的股票变化')
plt.legend()
plt.grid(True)
plt.show()


"""""
虽然在2024年我们认为人工智能是一个巨大的历史事件，它正在改变各行各业的运作方式，并且影响着全球经济和社会结构，但回顾历史，我们会发现，这并不是人类第一次面对如此重大的技术革新。事实上，许多发明在它们各自的时代也同样是伟大的创举，带来了前所未有的变革和进步。
这些发明不仅改变了人们的日常生活，还推动了社会和经济的发展，奠定了现代文明的基础。以下是一些在历史长河中极具重要意义的发明及其发明年份：

白炽灯（1879年）：爱迪生的白炽灯发明，使得人类摆脱了对自然光的依赖，延长了工作和生活的时间，极大地改变了社会的运作方式。
发电系统（1882年）：爱迪生建立的发电系统，不仅解决了电力分配的问题，还为现代工业社会奠定了基础。
电话（1876年）：贝尔发明的电话改变了人类沟通的方式，使得长距离实时交流成为可能。
飞机（1903年）：莱特兄弟的飞行器发明，开启了人类飞行的梦想，不仅缩短了地理距离，也促进了全球化的进程。
汽车（1886年）：卡尔·本茨发明的汽车，彻底改变了交通运输方式，使得人们的生活半径大大扩展。
电视（1927年）：费洛·法恩斯沃斯发明的电视，改变了人们获取信息和娱乐的方式，极大地影响了文化传播。
火箭（1957年）：苏联发射的第一颗人造卫星斯普特尼克1号，标志着火箭技术的发展，使得人类迈出了探索太空的第一步，开启了太空时代。
半导体（1947年）：贝尔实验室发明的晶体管，是现代电子技术的基石，为计算机和互联网的发展提供了核心支撑。
计算机（1946年）：ENIAC计算机的诞生，使得信息处理和存储能力大幅提升，改变了几乎所有行业的运作方式。
互联网（1969年）：ARPANET的建立，标志着互联网的诞生，连接了全球的信息网络，改变了人类获取信息和交流的方式，推动了全球信息化进程。
智能手机（2007年）：苹果公司推出的iPhone，将计算机、电话和互联网功能整合在一个便携设备中，彻底改变了人们的生活方式和工作方式。
每一个时代的伟大发明，都是历史的里程碑，推动了人类文明的进步和社会的巨大变革。AI的崛起，也将成为这样一个重要的历史节点，持续影响未来的发展。


尽管AI的崛起无疑是一个重要的历史节点，它将持续影响未来的发展，但我们也要保持理性和谨慎。在追逐科技创新和投资机会时，务必要深入了解相关技术的实际应用和市场前景。历史告诉我们，每一项伟大发明的背后，都有其自身的发展周期和潜在的风险。
盲目跟风投资AI，可能会带来不可预见的财务风险。投资者应基于深入的研究和充分的准备，理性判断技术的实际价值和市场潜力，避免陷入短期炒作的陷阱。
科技的发展和创新固然令人兴奋，但只有在理性的指导下，才能真正实现技术进步与投资收益的双赢。因此，保持冷静、理智和谨慎，是我们面对AI时代最好的策略。


本文完全是AI写的，所以，如果你觉得哪里不对，就怪GPT吧。
"""