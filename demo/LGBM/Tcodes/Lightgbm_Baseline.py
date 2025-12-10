import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# 加载数据
df = pd.read_csv("你的训练集路径")

# 特征列 & 标签列
# 删除 label 列作为特征以外的列
drop_cols = ['label']

# 如果未来发现 'fwd_header_length.1' 重复，可手动加入 drop_cols
features = [c for c in df.columns if c not in drop_cols]

X = df[features]
y = df['label']

# 标签编码
le = LabelEncoder()
y = le.fit_transform(y)

# 切分训练集/验证集
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

train_data = lgb.Dataset(X_train, label=y_train)
val_data = lgb.Dataset(X_val, label=y_val)

# LightGBM 参数（基线）
params = {
    'objective': 'multiclass',
    'num_class': len(le.classes_),
    'learning_rate': 0.05,
    'num_leaves': 31,
    'max_depth': 8,
    'metric': 'multi_logloss',
    'verbose': -1,
    'random_state': 42
}

# 训练模型
bst = lgb.train(
    params,
    train_data,
    num_boost_round=600,
    valid_sets=[train_data, val_data],
    callbacks=[
        lgb.early_stopping(50),
        lgb.log_evaluation(50)
    ]
)

# 模型评估
y_pred = bst.predict(X_val)
y_pred = y_pred.argmax(axis=1)

print("=== Classification Report ===")
print(classification_report(y_val, y_pred, target_names=le.classes_))

print("=== Confusion Matrix ===")
print(confusion_matrix(y_val, y_pred))

# 保存模型
joblib.dump(bst, "保存路径/lgb_baseline.joblib")
joblib.dump(le, "保存路径/label_encoder.joblib")

print("The model and label encoder have been saved!!!")