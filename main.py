import streamlit as st

st.set_page_config(page_title="BCC ArtGuard", layout="centered")


if "status" not in st.session_state:
    st.session_state.status = "safe"

st.markdown("<h1 style='text-align: center; color: #C9A227;'>BCC ArtGuard</h1>", unsafe_allow_html=True)


col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.session_state.status == "safe":
        st.image("safe.png", width='stretch')
        st.markdown("<h3 style='text-align: center; color: #00AB75;'>СТАТУС: БЕЗОПАСНО</h3>", unsafe_allow_html=True)
    else:
        st.image("danger.png", width='stretch')
        st.markdown("<h3 style='text-align: center; color: #DC2626;'>⚠ ПОДОЗРИТЕЛЬНАЯ АКТИВНОСТЬ</h3>", unsafe_allow_html=True)


    if st.button("Сменить статус", use_container_width=True):
        st.session_state.status = "danger" if st.session_state.status == "safe" else "safe"
        st.rerun()
