import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score, mean_squared_error

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score, mean_squared_error
from scipy import stats

# 1. 数据准备
data = {
    '烧结时间（小时）': [0, 2, 4, 6, 8, 20],
    '1号样块': [0.2202, 0.6291, 0.9901, 1.2610, 1.5127, 1.8693],
    '2号样块': [0.2514, 0.6915, 1.0830, 1.3555, 1.6050, 1.9243],
    '3号样块': [0.2125, 0.5959, 0.8571, 1.0599, 1.2993, 1.7185],
    '4号样块': [0.1790, 0.5541, 0.8517, 1.0439, 1.2749, 1.6729]
}

df = pd.DataFrame(data)

# 2. 绘制失水率曲线
plt.figure(figsize=(10, 6))
for column in df.columns[1:]:
    plt.plot(df['烧结时间（小时）'], df[column], marker='o', linestyle='-', label=column)
plt.title('各样块失水率随烧结时间的变化')
plt.xlabel('烧结时间（小时）')
plt.ylabel('失水率 (%)')
plt.legend()
plt.grid(True)
plt.show()


# 3. 定义逻辑斯蒂函数
def logistic(x, L, k, x0):
    return L / (1 + np.exp(-k * (x - x0)))


# 4. 拟合逻辑斯蒂模型并预测最佳烧结时间
optimal_times = {}
model_fits = {}

for column in df.columns[1:]:
    x_data = df['烧结时间（小时）'].values
    y_data = df[column].values

    # 初始参数估计
    L_init = max(y_data) * 1.1  # 预估饱和值稍大于最大观测值
    k_init = 1
    x0_init = np.median(x_data)

    try:
        popt, _ = curve_fit(logistic, x_data, y_data, p0=[L_init, k_init, x0_init], maxfev=10000)
    except RuntimeError:
        print(f"逻辑斯蒂回归拟合失败: {column}")
        continue

    L, k, x0 = popt
    y_pred = logistic(x_data, *popt)
    r2 = r2_score(y_data, y_pred)
    mse = mean_squared_error(y_data, y_pred)

    # 预测达到95%饱和值的时间
    target = L * 0.95
    # 反函数求解x
    optimal_time = x0 - (1 / k) * np.log((L / target) - 1)
    optimal_times[column] = optimal_time

    # 保存模型参数
    model_fits[column] = popt

    # 绘制拟合曲线
    x_fit = np.linspace(0, 24, 100)
    y_fit = logistic(x_fit, *popt)
    plt.figure(figsize=(10, 6))
    plt.scatter(x_data, y_data, label='实际数据')
    plt.plot(x_fit, y_fit, color='red', label='逻辑斯蒂回归拟合')
    plt.axhline(y=target, color='green', linestyle='--', label='95% 饱和值')
    plt.axvline(x=optimal_time, color='purple', linestyle='--', label=f'最佳时间 ≈ {optimal_time:.2f} 小时')
    plt.title(f'{column} 失水率 - 逻辑斯蒂回归')
    plt.xlabel('烧结时间（小时）')
    plt.ylabel('失水率 (%)')
    plt.legend()
    plt.grid(True)
    plt.show()

    print(f"{column} 最佳烧结时间预测: {optimal_time:.2f} 小时 (R²: {r2:.4f}, MSE: {mse:.4f})")

# 5. 配对t检验
print("\n配对t检验结果:")


# 函数进行配对t检验
def paired_t_test(sample1, sample2):
    t_stat, p_value = stats.ttest_rel(sample2, sample1)
    return t_stat, p_value


# 时间点列表
time_points = df['烧结时间（小时）'].tolist()

# 排除时间0，因为它是常温数据
time_pairs = list(zip(time_points[:-1], time_points[1:]))

# 计算各样块的配对t检验
t_test_results = {}
for pair in time_pairs:
    t_stat_list = []
    p_value_list = []
    for column in df.columns[1:]:
        time1, time2 = pair
        y1 = df[df['烧结时间（小时）'] == time1][column].values
        y2 = df[df['烧结时间（小时）'] == time2][column].values
        t_stat, p_value = stats.ttest_rel(y2, y1)
        t_stat_list.append(t_stat)
        p_value_list.append(p_value)
    # 计算平均p值
    avg_p_value = np.mean(p_value_list)
    t_test_results[pair] = avg_p_value
    print(f"比较时间点 {pair[0]} 小时 和 {pair[1]} 小时:")
    print(f"平均 p值 = {avg_p_value:.6f}")
    if avg_p_value < 0.05:
        print("结果：差异显著，继续烧结。\n")
    else:
        print("结果：差异不显著，可以考虑终止烧结。\n")

# 6. 综合逻辑斯蒂回归与t检验的结果
# 找出t检验中首次p值不显著的时间点
non_significant_time = None
for pair, p_value in t_test_results.items():
    if p_value >= 0.05:
        non_significant_time = pair[1]
        break

# 打印逻辑斯蒂回归预测的平均最佳时间
average_optimal_time = np.mean(list(optimal_times.values()))
print(f"综合各样块的最佳烧结时间预测（逻辑斯蒂回归平均值）: {average_optimal_time:.2f} 小时")

# 比较t检验与逻辑斯蒂回归的最佳时间
if non_significant_time:
    print(f"t检验显示首次变化不显著的时间点为: {non_significant_time} 小时")
    print(f"逻辑斯蒂回归预测的最佳时间为: {average_optimal_time:.2f} 小时")
    # 判断逻辑斯蒂预测时间是否接近t检验的时间点
    time_difference = abs(average_optimal_time - non_significant_time)
    print(f"逻辑斯蒂预测时间与t检验时间点的差异: {time_difference:.2f} 小时")
    # 根据差异决定是否采用t检验时间点或逻辑斯蒂预测时间
    if time_difference <= 1.0:
        print("逻辑斯蒂回归预测的最佳时间与t检验结果一致，建议采用此时间点。")
        optimal_time_final = non_significant_time
    else:
        print("逻辑斯蒂回归预测的最佳时间与t检验结果存在差异，建议进一步分析。")
        optimal_time_final = average_optimal_time
else:
    print("所有配对时间点的变化均显著，建议继续烧结至逻辑斯蒂回归预测的最佳时间。")
    optimal_time_final = average_optimal_time

print(f"最终推荐的最佳烧结时间: {optimal_time_final:.2f} 小时")
