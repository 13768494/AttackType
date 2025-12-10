import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_curve, auc,
    precision_recall_curve
)
from sklearn.preprocessing import label_binarize
from sklearn.model_selection import train_test_split
import numpy as np
import os
import gc


# 路径
data_path = "你的训练集路径"
model_path = "模型保存路径/lgb_baseline.joblib"
label_encoder_path = "模型保存路径/label_encoder.joblib"
output_dir = "保存路径"

os.makedirs(output_dir, exist_ok=True)

# 1. 低内存加载数据
df = pd.read_csv(data_path, low_memory=False)
for col in df.columns:
    if col != "label":
        df[col] = pd.to_numeric(df[col], downcast="float")

X = df.drop("label", axis=1)
y = df["label"]
del df
gc.collect()

encoder = joblib.load(label_encoder_path)
y_encoded = encoder.transform(y)

# 2. 切分数据
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# 释放训练集，减少内存
del X_train, y_train
gc.collect()

# 3. 加载模型
model = joblib.load(model_path)

# 4. 分类报告
print("Running prediction on X_test...")
y_prob = model.predict(X_test)
y_pred = np.argmax(y_prob, axis=1)

report_text = classification_report(y_test, y_pred, target_names=encoder.classes_)
with open(output_dir + "classification_report.txt", "w") as f:
    f.write(report_text)

print("Saved classification_report.txt")

# 5. 混淆矩阵
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
plt.imshow(cm, cmap="Blues")
plt.colorbar()

plt.xticks(np.arange(len(encoder.classes_)), encoder.classes_, rotation=45)
plt.yticks(np.arange(len(encoder.classes_)), encoder.classes_)

for i in range(len(encoder.classes_)):
    for j in range(len(encoder.classes_)):
        plt.text(j, i, cm[i, j], ha="center", va="center", color="black")

plt.xlabel("Predicted")
plt.ylabel("True")
plt.tight_layout()
plt.savefig(output_dir + "confusion_matrix.png", dpi=300)
plt.close()

print("Saved confusion_matrix.png")

# 6. 批量 predict_proba 防止爆内存
def batch_predict_proba(model, X, batch_size=50000):
    results = []
    total = len(X)

    num_classes = len(encoder.classes_)

    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        batch = X.iloc[start:end]

        prob = model.predict(batch)

        # 防止出现一维扁平情况：如 (N*num_classes,)
        prob = prob.reshape(-1, num_classes)

        results.append(prob)

        del batch, prob
        gc.collect()

    return np.vstack(results)

print("Predicting probabilities in batches...")
y_prob = batch_predict_proba(model, X_test)

# 7. ROC + PR
y_test_bin = label_binarize(y_test, classes=range(len(encoder.classes_)))

for i, cls in enumerate(encoder.classes_):

    # ROC
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_prob[:, i])
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, label=f"AUC={roc_auc:.3f}")
    plt.plot([0,1],[0,1],"--")
    plt.title(f"ROC - {cls}")
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir + f"roc_{cls}.png", dpi=300)
    plt.close()

    # PR
    precision, recall, _ = precision_recall_curve(y_test_bin[:, i], y_prob[:, i])

    plt.figure()
    plt.plot(recall, precision)
    plt.title(f"PR Curve - {cls}")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.tight_layout()
    plt.savefig(output_dir + f"pr_{cls}.png", dpi=300)
    plt.close()

print("Saved ROC/PR curves (per class)")

# 8. 保存 metrics.csv
report_dict = classification_report(
    y_test, y_pred, target_names=encoder.classes_, output_dict=True
)
pd.DataFrame(report_dict).T.to_csv(output_dir + "metrics.csv")

print("Saved metrics.csv")
