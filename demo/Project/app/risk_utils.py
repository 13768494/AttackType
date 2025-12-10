import pandas as pd

# 风险等级映射
RISK_SCORE_MAP = {
    "BENIGN": 5,
    "DoS": 60,
    "PortScan": 55,
    "DDoS": 80,
    "Bot": 75,
    "BruteForce": 65,
    "WebAttack": 70,
    "Infiltration": 85,
    "Heartbleed": 90,
}

# 根据预测类型生成风险分数和风险等级
def compute_risk_score(df: pd.DataFrame):
    # 生成风险分
    df["risk_score"] = df["predicted_label"].map(RISK_SCORE_MAP).fillna(40)

    # 风险等级
    def score_to_level(score):
        if score < 20:
            return "低危"
        elif score < 50:
            return "中危"
        elif score < 80:
            return "高危"
        else:
            return "严重"

    df["risk_level"] = df["risk_score"].apply(score_to_level)
    return df
