# README

## 介绍

​	站点提供用户上传流量CSV文件自动检测流量类型的功能。

![image-20251209211641906](D:\狗屎\毕设\AttackType\assets\showindex.png)

## 使用

**服务启动**

```less
streamlit run streamlit_app.py 
```

​	选择一个流量包的CSV上传即可使用。如果只用原始的.pcap包，可以使用站点提供的[CICFlowMeter-4.0](https://www.researchgate.net/profile/Arash-Habibi-Lashkari/publication/326991554_CICFlowmeter-V40_formerly_known_as_ISCXFlowMeter_is_a_network_traffic_Bi-flow_generator_and_analyser_for_anomaly_detection_httpsgithubcomISCXCICFlowMeter/data/5b717144a6fdcc87df742e3e/cicflowmeter-4.zip?origin=publication_detail&_tp=eyJjb250ZXh0Ijp7ImZpcnN0UGFnZSI6InB1YmxpY2F0aW9uIiwicGFnZSI6InB1YmxpY2F0aW9uRG93bmxvYWQiLCJwcmV2aW91c1BhZ2UiOiJwdWJsaWNhdGlvbiJ9fQ)工具制作。

## 一、部署环境

> 操作系统：Ubuntu 24.10
> Java：openjdk version "1.8.0_452"
> Python：Python 3.12.7

```less
sudo apt update && sudo apt install -y openjdk-8-jdk python3 python3-venv python3-pip
```

**requirements.txt**

```less
streamlit==1.51.0
pandas==2.3.3
chardet==5.2.0
joblib==1.5.2
matplotlib==3.10.7
plotly==6.5.0
lightgbm==4.6.0
scikit-learn==1.7.2
numpy==2.3.5
shap==0.50.0
```

## 二、项目结构

​	项目包括机器学习阶段以及站点开发阶段的所有源码，用户可以使用提供的机器学习源码来跑对应的模型。生成出自己的模型可以替换掉站点中`models`文件夹的内容，就可以使用自己的模型来进行流量攻击类型的预测。

```less
AttackType
 ┣ assets
 ┣ Scripts	// 模型训练前的数据处理
 ┃ ┣ .vscode
 ┃ ┃ ┗ settings.json
 ┃ ┣ All_Flows.py	// 合并CSV
 ┃ ┣ Data_Drop.py	// 删除指定标签
 ┃ ┗ Process_csv.py	// 数据清洗、格式化
 ┗ demo
 ┃ ┣ LGBM	// 模型训练等一系列工作
 ┃ ┃ ┣ Explain	// 模型特征重要性图
 ┃ ┃ ┣ JobLibs	// 训练好的模型
 ┃ ┃ ┣ Result	// 模型评价报告
 ┃ ┃ ┗ Tcodes
 ┃ ┃ ┃ ┣ Lightgbm_Baseline.py	// 模型训练脚本
 ┃ ┃ ┃ ┣ Model_Evaluate_Export.py	// 生成模型评价报告
 ┃ ┃ ┃ ┗ Model_Explain_LGB.py	// 生成 LightGBM 模型特征重要性图——Gain 排序
 ┃ ┗ Project	// 站点程序
 ┃ ┃ ┣ app
 ┃ ┃ ┃ ┣ .streamlit	// Web站点配置
 ┃ ┃ ┃ ┣ __pycache__
 ┃ ┃ ┃ ┣ csv_preview.py	// CSV预览
 ┃ ┃ ┃ ┣ csv_processor.py	// 对用户上传的CSV数据处理
 ┃ ┃ ┃ ┣ model_utils.py	// 模型调用
 ┃ ┃ ┃ ┣ plot_risk.py	// 饼图与柱状图
 ┃ ┃ ┃ ┣ predict_utils.py	// 预测
 ┃ ┃ ┃ ┣ risk_utils.py	// 风险等级
 ┃ ┃ ┃ ┗ streamlit_app.py	// 主入口
 ┃ ┃ ┣ data	// 用户上传文件存储
 ┃ ┃ ┣ models	// 训练的模型
 ┣ requirements.txt
 ┣ README.md
```

