import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

def plot_attack_distribution(df):
    attack_count = df["predicted_label"].value_counts()
    attack_count = attack_count[attack_count > 0]

    # 定义高饱和度颜色，可以根据攻击类型数量扩展
    color_seq = [
        '#0bd415',
        '#377eb8',
        '#4daf4a',
        '#ff4000',
        '#ffae00',
        '#ffff33',
    ][:len(attack_count)]  # 根据实际类型数量切片

    fig = px.pie(
        names=attack_count.index,
        values=attack_count.values,
        title="攻击类型比例",
        labels={'values':'总数', 'names':'攻击类型'},
        color_discrete_sequence=color_seq  # 高饱和度颜色序列
    )

    fig.update_traces(
        textposition='outside',
        textinfo='percent+label',
        insidetextorientation='radial',
        pull=[0]*len(attack_count),
        showlegend=True
    )

    fig.update_layout(
        uniformtext_minsize=10,
        uniformtext_mode='hide',
        margin=dict(t=50, b=50, l=50, r=50),
        legend_title_text='攻击类型'
    )

    return fig

def plot_risk_bar(df):
    # 固定顺序和颜色
    levels = ['低危', '中危', '高危', '严重']
    colors = ['#0bd415', 'yellow', 'orange', 'red']

    # 统计数量并按顺序排列，缺失等级填0
    level_count = df["risk_level"].value_counts()
    counts = [level_count.get(level, 0) for level in levels]

    # 构造 DataFrame
    df_plot = pd.DataFrame({
        "Risk Level": levels,
        "Count": counts,
        "Color": colors
    })

    # 绘制柱状图
    fig = px.bar(
        df_plot,
        x="Risk Level",
        y="Count",
        text="Count",
        color="Risk Level",
        color_discrete_map=dict(zip(levels, colors)),
    )

    # 更新布局
    fig.update_traces(
        textposition='outside'  # 在柱顶显示数值
    )
    fig.update_layout(
        title="风险等级数量",
        xaxis_title="风险等级",
        yaxis_title="数量",
        uniformtext_minsize=10,
        uniformtext_mode='hide',
        showlegend=False,  # 如果不需要单独图例，可以关闭
        margin=dict(t=50, b=50, l=50, r=50)
    )

    return fig