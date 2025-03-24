import streamlit as st
import pandas as pd
import random
import smtplib
import io
from email.mime.text import MIMEText
from openpyxl import load_workbook

# ----------------------------
# 📌 이메일 인증 관련 설정
# ----------------------------

# Gmail 발신자 정보
SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"

# 허용된 이메일 목록
ALLOWED_EMAILS = [
    "user1@example.com",
    "client@company.com"
]

# 인증 코드 저장소
st.session_state.setdefault("verified", False)
st.session_state.setdefault("auth_code", None)
st.session_state.setdefault("auth_email", None)


# 인증 코드 생성 및 전송
def generate_code():
    return str(random.randint(100000, 999999))

def send_email(receiver, code):
    msg = MIMEText(f"🔐 인증 코드: {code}")
    msg["Subject"] = "📧 Excel Master 인증 코드"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)


# ----------------------------
# 🖥️ Streamlit App
# ----------------------------
st.set_page_config(page_title="Excel Master", layout="centered")
st.title("📊 Excel Master v1.0")

# ----------------------------
# 🔐 이메일 인증 영역
# ----------------------------

if not st.session_state.verified:
    st.subheader("🔐 인증이 필요합니다")

    email = st.text_input("이메일 입력", key="email_input")
    
    if st.button("📩 인증 코드 받기"):
        if email not in ALLOWED_EMAILS:
            st.error("❌ 등록된 이메일이 아닙니다.")
        else:
            code = generate_code()
            send_email(email, code)
            st.session_state.auth_code = code
            st.session_state.auth_email = email
            st.success("✅ 인증 코드가 전송되었습니다. 이메일을 확인하세요!")

    if st.session_state.auth_code:
        user_input_code = st.text_input("이메일로 받은 6자리 인증 코드 입력")
        if st.button("✅ 인증 완료"):
            if user_input_code == st.session_state.auth_code:
                st.session_state.verified = True
                st.success("🎉 인증 성공! 프로그램을 사용할 수 있습니다.")
            else:
                st.error("❌ 인증 코드가 일치하지 않습니다.")

# ----------------------------
# ✅ 인증 성공 시 메인 기능 제공
# ----------------------------
if st.session_state.verified:
    tab1, tab2 = st.tabs(["✅ 엑셀 필터링", "🔁 CSV → Excel 변환"])

    # ----------------------------
    # ✅ 탭 1 - 엑셀 필터링
    # ----------------------------
    with tab1:
        uploaded_excel = st.file_uploader("엑셀 파일 업로드", type=["xlsx"], key="excel")
        if uploaded_excel:
            try:
                df = pd.read_excel(uploaded_excel, engine="openpyxl")
                st.success("파일 로드 성공 ✅")
                st.write("미리보기", df.head())

                col1 = st.selectbox("첫 번째 필터 컬럼", df.columns, key="col1")
                col2 = st.selectbox("두 번째 필터 컬럼 (선택)", ["(사용 안함)"] + list(df.columns), key="col2")

                val1 = st.multiselect(f"'{col1}'에서 선택", df[col1].dropna().unique())

                val2 = None
                if col2 and col2 != "(사용 안함)":
                    val2 = st.multiselect(f"'{col2}'에서 선택", df[col2].dropna().unique())

                if st.button("🔍 필터링 실행"):
                    filtered_df = df[df[col1].isin(val1)] if val1 else df
                    if val2 and col2 != "(사용 안함)":
                        filtered_df = filtered_df[filtered_df[col2].isin(val2)]
                    st.write(f"✅ 추출된 행 수: {len(filtered_df)}")
                    st.dataframe(filtered_df)

                    buffer = io.BytesIO()
                    filtered_df.to_excel(buffer, index=False, engine="openpyxl")
                    st.download_button("📥 결과 다운로드", data=buffer.getvalue(),
                                       file_name="필터결과.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            except Exception as e:
                st.error(f"❌ 오류 발생: {e}")

    # ----------------------------
    # 🔁 탭 2 - CSV → Excel 변환
    # ----------------------------
    with tab2:
        uploaded_csv = st.file_uploader("CSV 파일 업로드", type=["csv"], key="csv")
        if uploaded_csv:
            try:
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
                # ----------------------------
# 🔁 탭 2 - CSV → Excel 변환
# ----------------------------
with tab2:
    uploaded_csv = st.file_uploader("CSV 파일 업로드", type=["csv"], key="csv")
    if uploaded_csv:
        try:
            try:
                df_csv = pd.read_csv(uploaded_csv, encoding="utf-8")
            except UnicodeDecodeError:
                df_csv = pd.read_csv(uploaded_csv, encoding="cp949")

            st.success("CSV 파일 로드 성공 ✅")
            st.write("미리보기", df_csv.head())

            buffer_csv = io.BytesIO()
            df_csv.to_excel(buffer_csv, index=False, engine="openpyxl")

            st.download_button(
                "📥 Excel로 저장",
                data=buffer_csv.getvalue(),
                file_name="변환된_엑셀.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"❌ 변환 오류: {e}")
