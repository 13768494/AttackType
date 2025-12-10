import os
import pandas as pd

# 输入输出路径
input_file = "/home/zgy/Works/MachineLearning/AttackType/Data/tmp/sourcedata/GeneratedLabelledFlows/Friday-WorkingHours-Morning.pcap_ISCX.csv"
output_file = "/home/zgy/Works/MachineLearning/AttackType/Data/PCSV/P3.csv"

# 统一目标字段（训练时使用的78字段）
selected_columns = [
    'destination_port', 'flow_duration', 'total_fwd_packets', 
    'total_backward_packets', 'total_length_of_fwd_packets',
    'total_length_of_bwd_packets', 'fwd_packet_length_max',
    'fwd_packet_length_min', 'fwd_packet_length_mean', 'fwd_packet_length_std',
    'bwd_packet_length_max', 'bwd_packet_length_min', 'bwd_packet_length_mean',
    'bwd_packet_length_std', 'flow_bytes_s', 'flow_packets_s', 'flow_iat_mean',
    'flow_iat_std', 'flow_iat_max', 'flow_iat_min', 'fwd_iat_total', 
    'fwd_iat_mean', 'fwd_iat_std', 'fwd_iat_max', 'fwd_iat_min',
    'bwd_iat_total', 'bwd_iat_mean', 'bwd_iat_std', 'bwd_iat_max',
    'bwd_iat_min', 'fwd_psh_flags', 'bwd_psh_flags', 'fwd_urg_flags',
    'bwd_urg_flags', 'fwd_header_length', 'bwd_header_length', 'fwd_packets_s',
    'bwd_packets_s', 'min_packet_length', 'max_packet_length', 
    'packet_length_mean', 'packet_length_std', 'packet_length_variance',
    'fin_flag_count', 'syn_flag_count', 'rst_flag_count', 'psh_flag_count',
    'ack_flag_count', 'urg_flag_count', 'cwe_flag_count', 'ece_flag_count',
    'down_up_ratio', 'average_packet_size', 'avg_fwd_segment_size',
    'avg_bwd_segment_size', 'fwd_header_length_dup', 'fwd_avg_bytes_bulk',
    'fwd_avg_packets_bulk', 'fwd_avg_bulk_rate', 'bwd_avg_bytes_bulk',
    'bwd_avg_packets_bulk', 'bwd_avg_bulk_rate', 'subflow_fwd_packets',
    'subflow_fwd_bytes', 'subflow_bwd_packets', 'subflow_bwd_bytes',
    'init_win_bytes_forward', 'init_win_bytes_backward', 'act_data_pkt_fwd',
    'min_seg_size_forward', 'active_mean', 'active_std', 'active_max',
    'active_min', 'idle_mean', 'idle_std', 'idle_max', 'idle_min', 'label'
]

# 字段映射表（原字段 → 目标字段）
column_map = {
    "dst port": "destination_port",
    "dst_port": "destination_port",
    "flow duration": "flow_duration",
    "flow_duration": "flow_duration",
    "tot fwd pkts": "total_fwd_packets",
    "tot bwd pkts": "total_backward_packets",
    "totlen fwd pkts": "total_length_of_fwd_packets",
    "totlen bwd pkts": "total_length_of_bwd_packets",
    "fwd pkt len max": "fwd_packet_length_max",
    "fwd pkt len min": "fwd_packet_length_min",
    "fwd pkt len mean": "fwd_packet_length_mean",
    "fwd pkt len std": "fwd_packet_length_std",
    "bwd pkt len max": "bwd_packet_length_max",
    "bwd pkt len min": "bwd_packet_length_min",
    "bwd pkt len mean": "bwd_packet_length_mean",
    "bwd pkt len std": "bwd_packet_length_std",
    "flow byts/s": "flow_bytes_s",
    "flow pkts/s": "flow_packets_s",
    "flow iat mean": "flow_iat_mean",
    "flow iat std": "flow_iat_std",
    "flow iat max": "flow_iat_max",
    "flow iat min": "flow_iat_min",
    "fwd iat tot": "fwd_iat_total",
    "fwd iat mean": "fwd_iat_mean",
    "fwd iat std": "fwd_iat_std",
    "fwd iat max": "fwd_iat_max",
    "fwd iat min": "fwd_iat_min",
    "bwd iat tot": "bwd_iat_total",
    "bwd iat mean": "bwd_iat_mean",
    "bwd iat std": "bwd_iat_std",
    "bwd iat max": "bwd_iat_max",
    "bwd iat min": "bwd_iat_min",
    "fwd psh flags": "fwd_psh_flags",
    "bwd psh flags": "bwd_psh_flags",
    "fwd urg flags": "fwd_urg_flags",
    "bwd urg flags": "bwd_urg_flags",
    "fwd header len": "fwd_header_length",
    "bwd header len": "bwd_header_length",
    "fwd pkts/s": "fwd_packets_s",
    "bwd pkts/s": "bwd_packets_s",
    "pkt len min": "min_packet_length",
    "pkt len max": "max_packet_length",
    "pkt len mean": "packet_length_mean",
    "pkt len std": "packet_length_std",
    "pkt len var": "packet_length_variance",
    "fin flag cnt": "fin_flag_count",
    "syn flag cnt": "syn_flag_count",
    "rst flag cnt": "rst_flag_count",
    "psh flag cnt": "psh_flag_count",
    "ack flag cnt": "ack_flag_count",
    "urg flag cnt": "urg_flag_count",
    "cwe flag count": "cwe_flag_count",
    "ece flag cnt": "ece_flag_count",
    "down/up ratio": "down_up_ratio",
    "pkt size avg": "average_packet_size",
    "fwd seg size avg": "avg_fwd_segment_size",
    "bwd seg size avg": "avg_bwd_segment_size",
    "fwd byts/b avg": "fwd_avg_bytes_bulk",
    "fwd pkts/b avg": "fwd_avg_packets_bulk",
    "fwd blk rate avg": "fwd_avg_bulk_rate",
    "bwd byts/b avg": "bwd_avg_bytes_bulk",
    "bwd pkts/b avg": "bwd_avg_packets_bulk",
    "bwd blk rate avg": "bwd_avg_bulk_rate",
    "subflow fwd pkts": "subflow_fwd_packets",
    "subflow fwd byts": "subflow_fwd_bytes",
    "subflow bwd pkts": "subflow_bwd_packets",
    "subflow bwd byts": "subflow_bwd_bytes",
    "init fwd win byts": "init_win_bytes_forward",
    "init bwd win byts": "init_win_bytes_backward",
    "fwd act data pkts": "act_data_pkt_fwd",
    "fwd seg size min": "min_seg_size_forward",
    "active mean": "active_mean",
    "active std": "active_std",
    "active max": "active_max",
    "active min": "active_min",
    "idle mean": "idle_mean",
    "idle std": "idle_std",
    "idle max": "idle_max",
    "idle min": "idle_min",
    "label": "label"
}


# 标签值映射
label_map = {
    "BENIGN": "BENIGN",
    "DDoS": "DoS", "DoS Hulk": "DoS", "DoS GoldenEye": "DoS",
    "DoS slowloris": "DoS", "DoS Slowhttptest": "DoS",
    "PortScan": "PortScan",
    "Infiltration": "Other",
    "FTP-Patator": "BruteForce", "SSH-Patator": "BruteForce",
    "Web Attack-Brute Force": "WebAttack",
    "Web Attack-XSS": "WebAttack",
    "Web Attack-Sql Injection": "WebAttack",
    "Bot": "Botnet", "Botnet": "Botnet",
    "Heartbleed": "Other"
}

# 列名规范化函数
def normalize_columns(cols):
    return [c.strip().replace(" ", "_").replace("/", "_").lower() for c in cols]

# 主处理逻辑
def main():
    df = pd.read_csv(input_file)
    print(f"[INFO] Loaded CSV: {df.shape}")

    # 统一列名
    df.columns = normalize_columns(df.columns)

    # 映射字段名
    renamed = {}
    for col in df.columns:
        if col in column_map:
            renamed[col] = column_map[col]
        else:
            renamed[col] = col
    df.rename(columns=renamed, inplace=True)

    # 标签映射
    if "label" in df.columns:
        df["label"] = df["label"].astype(str).str.strip().replace(label_map)
    else:
        df["label"] = "BENIGN"

    # 补齐缺失字段
    for col in selected_columns:
        if col not in df.columns:
            df[col] = 0

    # 保留 selected_columns 顺序输出
    df = df[selected_columns]
    assert len(df.columns) >= 78, f"ERROR: final columns = {len(df.columns)}, expected 78"
    df.to_csv(output_file, index=False)
    print(f"[INFO] SUCCESS! Output → {output_file}")
    print(f"[INFO] Final columns count: {len(df.columns)}")

if __name__ == "__main__":
    main()
