# TQQQ 仿真项目 Prompt 库（优化版）

本库是为 **金融数据分析脚本生成** 准备的 Prompt 索引。整体结构分三层：
1) **通用约束**（所有脚本必须遵守）
2) **通用任务类型**（按“分析目的”组织）
3) **脚本索引**（按 `scripts/` 目录组织，便于快速定位现有实现）

---

## 0. 通用约束（System Prompt）
> 你是一个金融数据分析专家。编写 Python 脚本时：
> 1. 导入 `scripts/_util.py` 并使用 `load_csv_as_dataframe` 加载 `data/` 下的文件。
> 2. 绘图前调用 `_util.init_plotting()`，显示前调用 `_util.show_plot()`。
> 3. 代码力求简洁，关键逻辑使用向量化操作。

---

## 1. 通用任务类型（按分析目的）
> 适用场景：当你不知道现有脚本是否覆盖需求，或需要生成新脚本时先从这里选类型。

### 1.1 基础统计与排名
**适用场景**：寻找“极端日/极端区间”、涨跌幅排名、年份分布。
- 例：读取 `^SPX.csv`，计算日涨跌幅，输出涨幅/跌幅最大的前 N 天并统计年份分布。

### 1.2 季节性与周期分布
**适用场景**：月度/季度/年度规律、分布形态。
- 例：将指数按月重采样，绘制 1-12 月平均收益柱状图。

### 1.3 技术指标验证
**适用场景**：验证 Boll/均线突破后的收益分布与频率。
- 例：统计 Bollinger Bands 上轨/下轨突破频率（按日/周/月）。

### 1.4 对比与相关性
**适用场景**：两个标的或真实 vs 模拟杠杆的对比。
- 例：对齐两标的月度收益，绘制累计收益曲线并输出最终收益。

### 1.5 事件研究（事件前后窗口）
**适用场景**：重大事件前后市场表现（战争、危机、科技事件）。
- 例：标注古巴导弹危机日期并绘制 `^SPX` 事件窗口走势。

### 1.6 回撤、波动与风险
**适用场景**：波动率、回撤、极端风险可视化。
- 例：统计年化波动率并标记波动最大的年份。

### 1.7 模拟与策略评估
**适用场景**：杠杆模拟、FIRE 资产消耗、随机风险评估。
- 例：用 `_util.calculate_n_derivatives` 生成 n 倍杠杆模拟曲线并对比真实 ETF。

### 1.8 数据获取与维护
**适用场景**：下载/更新标的历史数据。
- 例：使用 yfinance 下载指定标的并保存到 `data/`。

---

## 2. 脚本索引（按目录）
> 适用场景：你想基于已有脚本做改造或直接复用。

### 2.1 `scripts/Analysis_Script/`
- **find_most_dramatic_day.py**：极端涨跌日统计 + 年份分布
- **find_quiet_days.py**：低波动日筛选与标记
- **statisitc_CAGR.py**：多标的 CAGR 对比 + 横向条形图
- **statistic_by_month.py**：月度平均收益（季节性）
- **statistic_specific_month.py**：指定月份分布统计
- **when_japan_crash_how_spx_do.py**：日本暴跌时美日市场对比

### 2.2 `scripts/Comparison_Script/`
- **compare_qqq_with_bitcoin_return.py**：NDX vs BTC 月度资金曲线
- **compare_two_stock_line_chart.py**：双标的月度收益曲线对比

### 2.3 `scripts/FIRE/`
- **fire_spending_prediction.py**：确定性 FIRE 资产消耗预测
- **Fire_risk.py**：随机模拟 FIRE 破产风险

### 2.4 `scripts/LETF/`
- **compare_n_time_derivatives.py**：n 倍杠杆模拟 vs 真实 ETF
- **compare_real_vs_derivatives.py**：真实与模拟杠杆收益率回归对比
- **visualize_halfing.py**：腰斩（回撤>50%）可视化

### 2.5 `scripts/Option/`
- **Visualize_option_decay.py**：期权时间价值衰减曲线
- **visualize_spy_call.py**：Call 价格随时间变化
- **option_prompt.txt**：期权计算题 Prompt 模板

### 2.6 `scripts/Technical_Indicators/`
- **how_common_to_break_down.py**：Boll 下轨突破频率
- **how_common_to_break_up.py**：Boll 上轨突破频率
- **top10_drop.py**：单日最大跌幅前十
- **verify_boll_day_level_up.py**：日线连续突破后的收益分布
- **verify_boll_week_level.py**：周线突破后的下一周表现
- **verify_boll_week_level_low.py**：周线跌破后的下一周表现

### 2.7 `scripts/Visualization_Script/`
- **cuban_missile_crisis_sp500_analysis.py.py**：古巴导弹危机事件窗口
- **plot_ww2_market.py**：二战期间走势可视化
- **visualize_1929.py**：1929 崩盘后的走势
- **visualize_1987.py**：历史大波动期走势
- **visualize_ATH.py**：ATH 刷新间隔与走势
- **visualize_ATH_with_dash.py**：交互式 ATH 可视化
- **visualize_average_daily_change.py**：平均年内走势
- **visualize_big_correction_during_bull_market.py**：牛市中大回调标记
- **visualize_middle_east_war.py**：中东战争事件研究（Dash）
- **visualize_moon_landing.py**：登月事件窗口
- **visualize_n_days_after_ATH.py**：ATH 后 N 天表现
- **visualize_narrow_escape_week.py**：周内大跌但周末收涨的分布
- **visualize_percent_distribution.py**：日/周/月/年分布可视化
- **visualize_std_volatility.py**：年化波动率对比
- **visualize_year_change.py**：年度涨幅分布
- **visualize_year_change_without_sep.py**：避开 9 月策略年度分布

### 2.8 `scripts/` 根目录
- **_util.py**：公共工具函数（读取、杠杆模拟、分位数、绘图等）
- **yfinance_download.py**：数据下载与更新
