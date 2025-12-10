import pandas as pd

input_path = "/home/zgy/Works/MachineLearning/AttackType/Data/AllLabelFlows_Summed.csv"
output_path = "/home/zgy/Works/MachineLearning/AttackType/Data/AllLabelFlows_Summed_NoOther.csv"

df = pd.read_csv(input_path)
print("Original data volume:", len(df))
print(df['label'].value_counts())

# 删除 Other 类
df = df[df['label'] != "Other"]

print("Delete data volume after Other:", len(df))
print(df['label'].value_counts())

# 保存文件
df.to_csv(output_path, index=False)
print(f"Success !!!")
