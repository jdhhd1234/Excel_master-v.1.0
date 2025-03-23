# app.py
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Excel 필터링 도구", layout="centered")

st.title("📊 엑셀 A열 필터링 도구 (웹버전)")

uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        if df.empty:
            st.error("엑셀 파일이 비어 있습니다.")
        else:
            a_col_values = df.iloc[:, 0].dropna().unique().tolist()
            selected = st.multiselect("A열 값 중 필터링할 항목을 선택하세요", sorted(a_col_values))

            if selected:
                filtered_df = df[df.iloc[:, 0].isin(selected)]

                st.success(f"✅ {len(filtered_df)}개의 행이 필터링되었습니다.")
                st.dataframe(filtered_df.head(20))

                # 다운로드 버튼
                to_excel = io.BytesIO()
                filtered_df.to_excel(to_excel, index=False)
                to_excel.seek(0)

                st.download_button(
                    label="📥 필터된 데이터 다운로드",
                    data=to_excel,
                    file_name="필터결과.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    except Exception as e:
        st.error(f"파일 처리 중 오류 발생: {e}")
