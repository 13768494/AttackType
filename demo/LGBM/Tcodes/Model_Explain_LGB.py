import joblib
import pandas as pd
import lightgbm as lgb
import shap
import matplotlib.pyplot as plt

# 文件路径
data_path = "你的训练集路径"
model_path = "模型保存路径/lgb_baseline.joblib"
label_encoder_path = "模型保存路径/label_encoder.joblib"
output_dir = "保存路径"

# 1. 加载数据 & 模型
df = pd.read_csv(data_path)
X = df.drop("label", axis=1)
model = joblib.load(model_path)
encoder = joblib.load(label_encoder_path)

# 2. LightGBM Feature Importance (Gain)
importance = model.feature_importance(importance_type='gain')
feature_names = model.feature_name()

imp_df = pd.DataFrame({
    "feature": feature_names,
    "importance_gain": importance
}).sort_values(by="importance_gain", ascending=False)

imp_df.to_csv(output_dir + "feature_importance_gain.csv", index=False)
print("Feature importance has been saved:feature_importance_gain.csv")

plt.figure(figsize=(10, 10))
lgb.plot_importance(model, max_num_features=25, importance_type='gain')
plt.tight_layout()
plt.savefig(output_dir + "feature_importance_top25.png", dpi=300)
plt.close()
print("Top 25 feature importance plots have been saved")

# 3. SHAP 模型解释（抽样以防 OOM）===
X_sample = X.sample(2000, random_state=42)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_sample)

# 保存 SHAP values
joblib.dump(shap_values, output_dir + "shap_values.joblib")
print("Saved SHAP values")

# 4. SHAP Summary Plot
shap.summary_plot(shap_values, X_sample, show=False)
plt.savefig(output_dir + "shap_summary.png", dpi=300, bbox_inches='tight')
plt.close()
print("Saved SHAP summary")

# 5. SHAP Bar Plot
shap.summary_plot(shap_values, X_sample, plot_type="bar", show=False)
plt.savefig(output_dir + "shap_bar.png", dpi=300, bbox_inches='tight')
plt.close()
print("Saved SHAP bar plot")