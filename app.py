from pathlib import Path

# 인증 + 기존 엑셀 필터링 + CSV 변환 통합된 Streamlit 앱 코드
app_with_email_auth = """\
import streamlit as st
import pandas as pd
import random
import smtplib
from email.message import EmailMessage
import io

# ---------- 이메일 인증 관련 ----------
def send_auth_email(to_email, code):
    msg = EmailMessage()
    msg["Subject"] = "Excel Master 인증 코드"
    msg["From"] = "excelmaster228@gmail.com"
    msg["To"] = to_email
    msg.set_content(f"📌 인증 코드: {code}\\n\\n이 코드는 1회용이며, 5분간 유효합니다.")

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "excelmaster228@gmail.com"
    sender_password = "qxvazbiysowtvluo"  # 앱 비밀번호

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"이메일 전송 실패: {e}")
        return False

# ---------- 앱 시작 ----------
st.set_page_config(page_title="Excel Master", layout="centered")
st.title("📧 Excel Master 인증 시스템")

# 인증 세션 변수
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "auth_sent" not in st.session_state:
    st.session_state.auth_sent = False
if "auth_code" not in st.session_state:
    st.session_state.auth_code = ""

if not st.session_state.authenticated:
    email = st.text_input("이메일 주소를 입력하세요")

    if st.button("📨 인증 코드 받기"):
        if email:
            code = str(random.randint(100000, 999999))
            if send_auth_email(email, code):
                st.session_state.auth_code = code
                st.session_state.auth_sent = True
                st.success("인증 코드가 이메일로 전송되었습니다.")

    if st.session_state.auth_sent:
        input_code = st.text_input("인증 코드 입력", max_chars=6)
        if st.button("✅ 인증 확인"):
            if input_code == st.session_state.auth_code:
                st.session_state.authenticated = True
                st.success("인증 성공! 프로그램을 사용할 수 있습니다.")
            else:
                st.error("인증 코드가 일치하지 않습니다.")

# 인증 완료 후 기능 사용
if st.session_state.authenticated:
    st.markdown("---")
    st.title("📊 Excel Master 기능")

    tab1, tab2 = st.tabs(["✅ 엑셀 필터링", "🔁 CSV → Excel 변환"])

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
"""

# 저장
app_path = Path("/mnt/data/app.py")
with open(app_path, "w", encoding="utf-8") as f:
    f.write(app_with_email_auth)

app_path = Path("/mnt/data/app.py")  # 👉 저장 경로 설정
with open(app_path, "w", encoding="utf-8") as f:
    f.write(app_with_email_auth)     # 👉 해당 경로에 코드 내용 저장

print("✅ app.py 저장 완료:", app_path)
