from supabase import create_client
import streamlit as st
import os
from db import init_supabase

supabase = init_supabase()
def register(email,password,name,community):
    res=supabase.auth.sign_up({
        "email": email,
        "password":password
    })
    if res.user:
        supabase.table("profiles").insert({
            "id":res.user.id,
            "name": name,
            "communityname":community,
        }).execute()
        return True,"Account created successfully"
    return False,"registration failed"

def login(email,password):
    res=supabase.auth.sign_in_with_password({
        "email":email,
        "password":password
    })
    if res.user:
        st.session_state.user=res.user
        st.session_state.session=res.session
        return True,"logged in successfully"
    return False,"invalid email or password"

def is_logged_in():
    return "user" in st.session_state and st.session_state.user is not None

#streamlit part
def loginpage():
        st.title("Login/Signup")
        tab1,tab2=st.tabs(["login","register"])

        with tab1:
            email=st.text_input("email",key="login_email")
            password=st.text_input("password",type="password",key="login_password")
            if st.button("Login"):
                success, message = login(email, password)
                st.write(message)
        with tab2:
            name = st.text_input("Name", key="reg_name")
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_password")
            community = st.selectbox("Community name",["Indiranagar", "Koramangala", "Jayanagar", "Whitefield", "Electronic City", "HSR Layout", "BTM Layout", "Rajajinagar", "Basaveshwaranagar", "Yelahanka"])
            if st.button("Register"):
                success, message = register(email, password, name, community)
                st.write(message)
if not is_logged_in():
    loginpage()
else:
    st.switch_page("pages/scan.py")