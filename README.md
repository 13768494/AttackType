# 攻击流量检测系统使用手册

## 一、项目目录结构

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

## 二、环境部署

> 操作系统：Ubuntu 24.10 TLS
> Python：Python 3.12.7
> Java：openjdk version "1.8.0_452"

```shell
# 配置必要开发环境
sudo apt update && sudo apt install -y openjdk-8-jdk python3 python3-venv python3-pip
```

requirements

```shell
# 安装开发环境Python必要库
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

## 三、服务启动

进入安装了开发必要的Python库的虚拟环境。

![image-20260131151316054](https://github.com/13768494/AttackType/blob/main/assets/image-20260131151316054.png)

使用`streamlit`命令启动站点主入口`streamlit_app.py`（最好进入app路径再执行，否则会出现用户上传的文件没有读取权限的问题）。

![image-20260131151557390](https://github.com/13768494/AttackType/blob/main/assets/image-20260131151557390.png)

浏览器就会自动打开系统页面。

![image-20260131151624255](https://github.com/13768494/AttackType/blob/main/assets/image-20260131151624255.png)

用户点击`Browse files`选择本地需要检测的CSV流量文件即可进行流量风险的预测。

![image-20260131152110339](https://github.com/13768494/AttackType/blob/main/assets/image-20260131152110339.png)

<center>风险预测数据可视化结果</center>

![image-20260131152229551](https://github.com/13768494/AttackType/blob/main/assets/image-20260131152229551.png)

<center>用户上传CSV预览以及风险预测结果</center>

点击`下载预测结果 CSV`就可以把页面展示的列表保存到本地进行预览，如果用户只有原始的.pcap流量数据可以点击下方的数据处理工具转换为.csv文件。

![image-20260131152433684](https://github.com/13768494/AttackType/blob/main/assets/image-20260131152433684.png)

## *模型训练

使用`Lightgbm_Baseline.py`即可根据需求训练模型，将自己整合好的CSV文件所在目录填入`pd.read_csv`即可指定训练集。

![image-20260131152811749](https://github.com/13768494/AttackType/blob/main/assets/image-20260131152811749.png)

在训练过程会输出训练的日志，训练结束之后会保存在用户指定的目录下，并生成两个文件`lgb_baseline.joblib（基线模型）`以及`label_encoder.joblib(编码器)`。

![image-20260131152930100](https://github.com/13768494/AttackType/blob/main/assets/image-20260131152930100.png)

后续只需要将自己训练好的模型替换掉`AttackType\demo\Project\models`目录中的旧模型即可使用新训练的模型进行风险预测。
