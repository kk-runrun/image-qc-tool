import streamlit as st
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog

# 1. 定义标准后缀列表
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

def scan_local_folder(root_path):
    """直接扫描本地物理路径"""
    results = []
    
    # 获取根目录下所有的子文件夹
    try:
        packages = [f for f in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, f))]
        if not packages:
            # 如果根目录下全是文件，则把根目录本身当做一个图包处理
            packages = ["."]
    except Exception as e:
        st.error(f"无法读取路径: {e}")
        return None

    for pkg in packages:
        pkg_full_path = os.path.join(root_path, pkg)
        found_suffixes = set()
        naming_errors = []
        
        # 遍历图包内的所有文件（包括子文件夹）
        for root, dirs, files in os.walk(pkg_full_path):
            for file in files:
                if file.startswith('.'): continue # 跳过隐藏文件
                
                name_without_ext = os.path.splitext(file)[0]
                
                matched = False
                for suffix in REQUIRED_SUFFIXES:
                    if name_without_ext.endswith(suffix):
                        found_suffixes.add(suffix)
                        matched = True
                        break
                
                if not matched:
                    naming_errors.append(file)

        missing_suffixes = [s for s in REQUIRED_SUFFIXES if s not in found_suffixes]
        
        status = "正确" if not missing_suffixes and not naming_errors else "图片命名有误，请人工核查"
        
        results.append({
            "第一层图报名": pkg if pkg != "." else os.path.basename(root_path),
            "校验结果": status,
            "缺失图片后缀": " | ".join(missing_suffixes) if missing_suffixes else "无",
            "命名错误图片": " | ".join(naming_errors) if naming_errors else "无"
        })
        
    return pd.DataFrame(results)

# --- UI 界面 ---
st.set_page_config(page_title="本地图包质检工具", layout="wide")
st.title("🏠 本地图包命名一键质检")

# 文件夹选择逻辑
st.markdown("### 第一步：指定本地图包目录")
st.info("说明：请在下方输入文件夹的完整路径，或者点击按钮选择。如果是多包质检，请输入包含多个图包文件夹的那个父目录。")

# 原生文件夹选择框
if 'folder_path' not in st.session_state:
    st.session_state.folder_path = ""

col1, col2 = st.columns([4, 1])
with col1:
    target_path = st.text_input("本地路径 (例如 D:/Work/Images)", value=st.session_state.folder_path)
with col2:
    if st.button("📁 选择文件夹"):
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True) # 确保弹出框在最前面
        selected_path = filedialog.askdirectory(master=root)
        root.destroy()
        if selected_path:
            st.session_state.folder_path = selected_path
            st.rerun()

# 校验按钮
if target_path:
    if st.button("🔍 开始质检", type="primary"):
        if os.path.exists(target_path):
            with st.spinner('正在扫描本地文件...'):
                df_result = scan_local_folder(target_path)
                if df_result is not None:
                    st.subheader("📋 质检报告")
                    st.dataframe(df_result, use_container_width=True)
                    
                    # 导出报告
                    csv = df_result.to_csv(index=False).encode('utf-8-sig')
                    st.download_button("导出报告 (CSV)", data=csv, file_name='local_qc_report.csv')
        else:
            st.error("路径不存在，请检查输入的路径是否正确。")