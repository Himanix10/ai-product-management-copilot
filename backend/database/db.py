import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@st.cache_resource
def get_db_engine():
    # Points directly to your SQLite database
    return create_engine("sqlite:///backend/database/app.db", connect_args={"check_same_thread": False})

def get_db_session():
    engine = get_db_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
