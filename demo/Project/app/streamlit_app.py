import streamlit as st
import io
from csv_processor import process_csv
from csv_preview import paginate_dataframe
from predict_utils import predict_full
from model_utils import load_model
from risk_utils import compute_risk_score
from plot_risk import plot_attack_distribution, plot_risk_bar
import pandas as pd

# 页面配置
st.set_page_config(page_title="攻击流量检测系统原型", layout="wide")
st.title("攻击流量检测系统原型")
st.write("上传 CSV 文件，自动处理并预测攻击类型与风险等级")

# 上传 CSV
uploaded_file = st.file_uploader("上传 CSV 文件", type=["csv"])

@st.cache_data(show_spinner=False)
def load_and_process_csv(file_bytes: bytes, output_path: str):
    # 缓存 CSV 处理 + 保存，保证返回 DataFrame
    file_io = io.BytesIO(file_bytes)
    df = process_csv(file_io, output_path)
    return df

@st.cache_resource(show_spinner=False)
def load_model_cached(model_path, encoder_path):
    # 缓存模型加载
    return load_model(model_path, encoder_path)

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    output_file = "../data/processed_uploaded.csv"

    try:
        # CSV 处理
        df_full = load_and_process_csv(file_bytes, output_file)
        st.success(f"CSV 处理完成！")

        # 加载模型
        model, encoder = load_model_cached("../models/lgb_baseline.joblib","../models/label_encoder.joblib")

        # 整体预测
        df_full = predict_full(df_full, model, encoder)

        # 风险评分计算
        df_full = compute_risk_score(df_full)

        # 风险等级可视化
        st.subheader("风险等级统计")
        col1, col2 = st.columns(2)

        with col1:
            fig1 = plot_attack_distribution(df_full)
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = plot_risk_bar(df_full)
            st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        # 分页显示
        page_size = st.number_input("每页显示多少行？", min_value=50, max_value=20000, value=1000, step=100)
        # 先计算总页数（不缓存）
        total_rows = len(df_full)
        total_pages = (total_rows + page_size - 1) // page_size

        # 页码输入控件：动态限制范围
        page = st.number_input(
            "选择页码",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1
        )

        # 使用缓存分页
        @st.cache_data(show_spinner=False)
        def get_page(df, page_size, page_num):
            df_page, total_pages = paginate_dataframe(df, page_size, page_num)
            return df_page, total_pages

        df_page, _ = get_page(df_full, page_size, page)

        st.subheader(f"当前显示第 {page} 页（共 {total_pages} 页）")
        st.dataframe(df_page, width="stretch")

        # 下载完整预测结果
        csv = df_full.to_csv(index=False, encoding="utf-8-sig")
        csv_bytes = csv.encode("utf-8-sig")

        st.download_button(
            label="下载预测结果 CSV",
            data=csv_bytes,
            file_name="prediction_result_full.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"CSV 处理失败: {e}")

# 提供工具下载链接
st.subheader("只有 .pcap 文件?")
url = "https://www.researchgate.net/profile/Arash-Habibi-Lashkari/publication/326991554_CICFlowmeter-V40_formerly_known_as_ISCXFlowMeter_is_a_network_traffic_Bi-flow_generator_and_analyser_for_anomaly_detection_httpsgithubcomISCXCICFlowMeter/data/5b717144a6fdcc87df742e3e/cicflowmeter-4.zip?origin=publication_detail&_tp=eyJjb250ZXh0Ijp7ImZpcnN0UGFnZSI6InB1YmxpY2F0aW9uIiwicGFnZSI6InB1YmxpY2F0aW9uRG93bmxvYWQiLCJwcmV2aW91c1BhZ2UiOiJwdWJsaWNhdGlvbiJ9fQ"
st.markdown(f"[点击这里下载 CICFlowMeter-4.0]({url})")
