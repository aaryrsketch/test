import streamlit as st
import pandas as pd
from db import supabase

res=supabase.table("profiles").select("name,points").order("points",desc=True).execute()\

df=pd.DataFrame(list(res.data),columns=["name","points"])
st.title("LEADERBOARD")
st.dataframe(df)