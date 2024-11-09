import pandas as pd
#
# 读取CSV文件
# input_filename = 'tb.csv'  # 输入文件名
# output_filename = 'taobao_data.csv'  # 输出文件名
#
# # 使用pandas读取文件
# df = pd.read_csv(input_filename)
#
# # 去掉price为0.0的行
# df = df[df['price'] != 0.0]
#
# # 去掉img为空的行
# df = df[df['img'].notna() & (df['img'] != '')]
#
# # 保存过滤后的数据到新的CSV文件
# df.to_csv(output_filename, index=False)
#
# print(f"已成功保存过滤后的数据到 {output_filename}")

# 读取第一个 CSV 文件
file1 = 'filtered_taobao_data.csv'  # 第一个 CSV 文件路径
file2 = 'taobao_data.csv'  # 第二个 CSV 文件路径
# file3 = '../data/jd3.csv'
output_file = '../data/tb.csv'  # 合并后的输出文件路径

# 加载两个文件并添加平台列
df1 = pd.read_csv(file1)
df1['platform'] = '淘宝'  # 添加 platform
df2 = pd.read_csv(file2)
df2['platform'] = '淘宝'
# df3 = pd.read_csv(file3)
# df3['platform'] = '京东'

# 保存添加新列后的数据到新的 CSV 文件
# df1.to_csv(output_file, index=False)

# 合并两个文件
merged_df = pd.concat([df1, df2], ignore_index=True)

# 指定列的顺序
merged_df = merged_df[['title', 'price', 'deal', 'shop', 'link', 'img', 'platform']]

# 将合并后的数据保存到新的 CSV 文件
merged_df.to_csv(output_file, index=False)

print(f"合并完成，结果已保存到 {output_file}")

