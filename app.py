import streamlit as st
import pandas as pd
import os

# 1. 定义标准后缀列表 (完整版)
REQUIRED_SUFFIXES = [
    "a100-1", "a100-1.10", "a100-1.10w", "a100-1.11", "a100-1.11-m", "a100-1.11-pt", "a100-1.11-ptw", "a100-1.11w", 
    "a100-1.12", "a100-1.12-m", "a100-1.12w", "a100-1.13", "a100-1.13-m", "a100-1.13w", "a100-1.14", "a100-1.14-m", 
    "a100-1.14w", "a100-1.15", "a100-1.15-m", "a100-1.15w", "a100-1.16", "a100-1.16-m", "a100-1.16w", "a100-1.17", 
    "a100-1.17-m", "a100-1.17w", "a100-1.18", "a100-1.18-m", "a100-1.18w", "a100-1.19", "a100-1.19-m", "a100-1.19w", 
    "a100-1.2", "a100-1.20", "a100-1.20-m", "a100-1.20w", "a100-1.21", "a100-1.21-m", "a100-1.21w", "a100-1.22", 
    "a100-1.22-m", "a100-1.22w", "a100-1.23", "a100-1.23-m", "a100-1.23w", "a100-1.24", "a100-1.24-m", "a100-1.25-m", 
    "a100-1.26-m", "a100-1.27-m", "a100-1.28-m", "a100-1.29-m", "a100-1.3", "a100-1.4", "a100-1.4-m", "a100-1.4-pt", 
    "a100-1.4-ptw", "a100-1.4w", "a100-1.5", "a100-1.6", "a100-1.7", "a100-1.8", "a100-1.9", "a100-1.92", "a100-1.93", 
    "a100-1w", "a100-2", "a100-2.2", "a100-2.2-m", "a100-2.2-pt", "a100-2.2-ptw", "a100-2.2w", "a100-2.3", "a100-2.3-m", 
    "a100-2.3-pt", "a100-2.3-ptw", "a100-2.3w", "a100-2.4", "a100-2.4-m", "a100-2.4-pt", "a100-2.4-ptw", "a100-2.4w", 
    "a100-2.5", "a100-2.5-m", "a100-2.5-pt", "a100-2.5-ptw", "a100-2.5w", "a100-2w", "a100-3", "a100-3w", "a100-4", 
    "a100-4-pt", "a100-4w", "a100-dlz1", "f1", "f1-f", "f1w", "f2", "f2-f", "f2w", "f3", "f3-f", "f3w", "f4", "f4-f", 
    "f4w", "f5", "f5-f", "f5w", "f6", "f6-f", "f6w", "f7", "f7-f", "f7w", "f8", "f8-f", "f8w", "fb1", "m100-1.1", 
    "m100-1.12", "m100-1.2", "m100-1.21", "m100-1.2ae", "m100-1.2w", "m100-1.3", "m100-1.30", "m100-10", "m100-10w", 
    "m100-11", "m100-11w", "m100-12", "m100-12w", "m100-13", "m100-13w", "m100-14", "m100-15", "m100-2", "m100-2w", 
    "m100-3", "m100-3w", "m100-4", "m100-4w", "m100-5", "m100-5w", "m100-6", "m100-6w", "m100-7", "m100-7w", "m100-8", 
    "m100-8w", "m100-9", "m100-9w", "x1", "x1w", "vevor-350-176", "vevor-600-180", "pvp1", "pvp2", "pvp3", "pvp4", 
    "v100-1.1", "v100-1.2", "v100-1.3", "m100-1.1w", "m100-1.12w", "a100-1.11-mw", "a100-1.12-mw", "a100-1.13-mw", 
    "a100-1.14-mw", "a100-1.15-mw", "a100-1.16-mw", "a100-1.17-mw", "a100-1.18-mw", "a100-1.19-mw", "a100-1.20-mw", 
    "a100-1.21-mw", "a100-1.22-mw", "a100-1.23-mw", "a100-1.4-mw", "a100-2.2-mw", "a100-2.3-mw", "a100-2.4-mw", 
    "a100-2.5-mw", "m100-1.2-fw", "f1-fw", "f2-fw", "f3-fw", "f4-fw", "f5-fw", "f6-fw", "f7-fw", "f8-fw", "f9-fw"
]

def check_naming(uploaded_files):
    results = []
    package_groups = {}
    
    # 模拟文件夹分组
    for file in uploaded_files:
        # Streamlit 上传多文件时 file.name 包含相对路径
        parts = file.name.split('/')
        pkg_name = parts[0] if len(parts) > 1 else "根目录"
        if pkg_name not in package_groups:
            package_groups[pkg_name] = []
        package_groups[pkg_name].append(file.name)

    for pkg_name, file_paths in package_groups.items():
        found_suffixes = set()
        naming_errors = []
        
        for path in file_paths:
            full_filename = os.path.basename(path)
            if full_filename.startswith('.'): continue # 跳过隐藏文件
            
            name_without_ext = os.path.splitext(full_filename)[0]
            matched = False
            for suffix in REQUIRED_SUFFIXES:
                if name_without_ext.endswith(suffix):
                    found_suffixes.add(suffix)
                    matched = True
                    break
            
            if not matched:
                naming_errors.append(full_filename)

        missing_suffixes = [s for s in REQUIRED_SUFFIXES if s not in found_suffixes]
        status = "正确" if not missing_suffixes and not naming_errors else "图片命名有误，请人工核查"
            
        results.append({
            "第一层图报名": pkg_name,
            "校验结果": status,
            "缺失图片后缀": " | ".join(missing_suffixes) if missing_suffixes else "无",
            "命名错误图片": " | ".join(naming_errors) if naming_errors else "无"
        })
        
    return pd.DataFrame(results)

# --- 界面展示 ---
st.set_page_config(page_title="图包命名在线质检", layout="wide")
st.title("📸 图包命名在线质检")
st.markdown("⚠️ **注意：** 在线版请直接拖入文件夹或选中所有图片。")

# 使用 Streamlit 原生上传组件
uploaded_files = st.file_uploader("请在此处拖入图包文件夹", accept_multiple_files=True)

if uploaded_files:
    st.info(f"已识别到 {len(uploaded_files)} 个文件。")
    if st.button("🚀 开始校验"):
        with st.spinner('分析中...'):
            df_result = check_naming(uploaded_files)
            st.subheader("📊 校验报告")
            st.dataframe(df_result, use_container_width=True)
            
            csv = df_result.to_csv(index=False).encode('utf-8-sig')
            st.download_button("下载结果表 (CSV)", data=csv, file_name='qc_report.csv')
