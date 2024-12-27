import pandas as pd
import re

# 读取CSV文件
df = pd.read_csv('./data.csv')

# 处理空值
df.fillna('', inplace=True)

# 定义提取薪资范围的函数
def extract_salary_range(salary_str):
    if '薪资面议' in salary_str:
        return None, None  # 薪资面议则返回None

    # 使用正则表达式提取数字部分
    pattern = r'(\d+)-(\d+)k(·\d*薪)?'
    match = re.match(pattern, salary_str)
    if match:
        start_salary = int(match.group(1)) * 1000  # 转换为整数，单位为元
        end_salary = int(match.group(2)) * 1000  # 转换为整数，单位为元
        return start_salary, end_salary
    else:
        return None, None  # 匹配失败则返回None

# 应用提取函数到Salary列，并拆分为最低薪资和最高薪资两列
df[['Start Salary', 'End Salary']] = df['Salary'].apply(lambda x: pd.Series(extract_salary_range(x)))

# 定义提取地区的函数
def extract_district(location_str):
    # 使用字符串分割提取区域信息
    district = location_str.split('-')[-1]
    return district

# 应用提取函数到Job Location列
df['District'] = df['Job Location'].apply(extract_district)

# 将最终结果保存为CSV文件
df.to_csv('processed_data.csv', index=False)
