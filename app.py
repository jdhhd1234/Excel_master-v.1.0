import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Excel Master", layout="centered")
st.title("📊 Excel Master v1.0")

tab1, tab2 = st.tabs(["✅ 엑셀 필터링", "🔁 CSV → Excel 변환"])

# -------------------
# ✅ 엑셀 필터링 탭
# -------------------
with tab1:
    uploaded_excel = st.file_uploader("엑셀 파일 업로드", type=["xlsx"])
    if uploaded_excel:
        try:
            df = pd.read_excel(uploaded_excel, engine="openpyxl")
            st.success("파일 로드 성공 ✅")
            st.write("미리보기", df.head())

            col1 = st.selectbox("첫 번째 필터 컬럼", df.columns, key="col1")
            col2 = st.selectbox("두 번째 필터 컬럼 (선택)", ["(사용 안함)"] + list(df.columns), key="col2")

            if col1:
                val1 = st.multiselect(f"'{col1}'에서 선택", df[col1].dropna().unique())

            if col2 and col2 != "(사용 안함)":
                val2 = st.multiselect(f"'{col2}'에서 선택", df[col2].dropna().unique())
            else:
                val2 = None

            if st.button("필터링 실행"):
                filtered_df = df[df[col1].isin(val1)] if val1 else df
                if val2 and col2 != "(사용 안함)":
                    filtered_df = filtered_df[filtered_df[col2].isin(val2)]
                st.write(f"🔍 추출된 행 수: {len(filtered_df)}")
                st.dataframe(filtered_df)

                buffer = io.BytesIO()
                filtered_df.to_excel(buffer, index=False, engine="openpyxl")
                st.download_button("📥 결과 다운로드", data=buffer.getvalue(),
                                   file_name="필터결과.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        except Exception as e:
            st.error(f"❌ 오류 발생: {e}")

# -------------------
# 🔁 CSV → Excel 변환 탭
# -------------------
with tab2:
    uploaded_csv = st.file_uploader("CSV 파일 업로드", type=["csv"], key="csv")
    if uploaded_csv:
        try:
            # 자동 인코딩 감지
            try:
                df_csv = pd.read_csv(uploaded_csv, encoding="utf-8")
            except UnicodeDecodeError:
                df_csv = pd.read_csv(uploaded_csv, encoding="cp949")

            st.success("CSV 파일 로드 성공 ✅")
            st.write("미리보기", df_csv.head())

            buffer_csv = io.BytesIO()
            df_csv.to_excel(buffer_csv, index=False, engine="openpyxl")
            st.download_button("📥 Excel로 저장", data=buffer_csv.getvalue(),
                               file_name="변환된_엑셀.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        except Exception as e:
            st.error(f"❌ 변환 오류: {e}")
