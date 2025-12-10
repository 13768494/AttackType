import joblib
import pandas as pd

# 加载模型
def load_model(model_path, encoder_path):
    model = joblib.load(model_path)
    encoder = joblib.load(encoder_path)
    return model, encoder

# 预测函数
def predict(df, model, encoder):
    X = df.copy()
    if "label" in X.columns:
        X = X.drop("label", axis=1)
    y_pred = model.predict(X)
    # LightGBM多分类返回预测类别索引，需要转成原始标签
    try:
        # 如果使用predict_proba，则可以选argmax
        import numpy as np
        y_pred_labels = encoder.inverse_transform(np.argmax(y_pred, axis=1))
    except:
        y_pred_labels = encoder.inverse_transform(y_pred)
    return y_pred_labels
