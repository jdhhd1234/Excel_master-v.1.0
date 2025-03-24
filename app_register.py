import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 초기화
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.set_page_config(page_title="이메일 등록기", layout="centered")
st.title("📮 허용 이메일 등록")

email = st.text_input("📨 등록할 이메일 주소를 입력하세요")

if st.button("등록 요청"):
    if not email or "@" not in email:
        st.warning("유효한 이메일을 입력하세요.")
    else:
        try:
            doc_ref = db.collection("allowed_emails").document(email)
            doc_ref.set({"email": email})
            st.success(f"✅ 이메일이 등록되었습니다: {email}")
        except Exception as e:
            st.error(f"❌ 등록 실패: {e}")
