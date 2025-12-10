import pandas as pd

# 返回指定页码的数据
def paginate_dataframe(df, page_size=1000, page_number=1):
    total_rows = df.shape[0]
    total_pages = (total_rows // page_size) + 1
    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size
    df_page = df.iloc[start_idx:end_idx]
    return df_page, total_pages
