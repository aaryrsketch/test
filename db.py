from datetime import date
from supabase import create_client
import streamlit as st

@st.cache_resource
def init_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

supabase = init_supabase()

def already_scanned_today(user_id):
    today = date.today().isoformat()
    res = supabase.table("scans")\
        .select("id")\
        .eq("user_id", user_id)\
        .gte("scanned_at", f"{today}T00:00:00")\
        .lte("scanned_at", f"{today}T23:59:59")\
        .execute()
    return len(res.data) > 0

def save_scan(user_id, categories, points):
    supabase.table("scans").insert({
        "user_id": user_id,
        "wastecategory": categories,
        "points_awarded": points,
    }).execute()

    current = supabase.table("profiles")\
        .select("points")\
        .eq("id", user_id)\
        .execute()
    
    current_points = current.data[0]["points"]
    
    supabase.table("profiles")\
        .update({"points": current_points + points})\
        .eq("id", user_id)\
        .execute()