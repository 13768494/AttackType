import pandas as pd
import glob
# 获取目录下所有 CSV 文件
csv_files = glob.glob("/home/zgy/Works/MachineLearning/AttackType/Data/tmp/sourcedata/MachineLearningCVE/*.csv")

# 用列表推导式读取 CSV
dfs = [pd.read_csv(f) for f in csv_files]

# 合并所有 DataFrame
merged_df = pd.concat(dfs, ignore_index=True)

# 保存为一个 CSV
merged_df.to_csv("/home/zgy/Works/MachineLearning/AttackType/Data/TCSV/All_Flows_P2.csv", index=False)
print("success!")