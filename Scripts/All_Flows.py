import pandas as pd
import glob
# 获取目录下所有 CSV 文件
csv_files = glob.glob("未处理的CSV所在文件夹/*.csv")

# 用列表推导式读取 CSV
dfs = [pd.read_csv(f) for f in csv_files]

# 合并所有 DataFrame
merged_df = pd.concat(dfs, ignore_index=True)

# 保存为一个 CSV
merged_df.to_csv("处理完成后的CSV.csv", index=False)
print("success!")