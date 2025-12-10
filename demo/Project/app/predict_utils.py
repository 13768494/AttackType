from model_utils import predict

# 对整个 DataFrame 做预测并添加 predicted_label 列
def predict_full(df, model, encoder):
    y_pred = predict(df.copy(), model, encoder)
    df["predicted_label"] = y_pred
    return df
