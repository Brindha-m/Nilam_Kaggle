import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import numpy as np
import re
import html
import time
import markdown2

# Page configuration - commented out for main.py integration
# st.set_page_config(
#     page_title="Nilam - Agricultural Assistant",
#     page_icon="🌱",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# Enhanced CSS with improved selectbox styling
st.markdown("""
<style>
    :root {
        --cream-light: #fefcf8;
        --cream-medium: #f5f1e8;
        --cream-dark: #ede4d3;
        --earth-green: #7a8471;
        --earth-brown: #8b7355;
        --text-primary: #2d3436;
        --text-secondary: #636e72;
        --graph-text: #2d3436;
        --graph-text-secondary: #636e72;
        --sidebar-text: #ffffff;
        --selection-text: #ffffff;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--cream-light) 0%, var(--cream-medium) 100%);
    }
    
    /* Sidebar styles */
    .css-1d391kg, .css-1lcbmhc, .css-1v0mbdj,
    [data-testid="stSidebar"] {
        background-color: #2d3436 !important;
        color: white !important;
    }
    
    /* Global selectbox styles - make all selectbox text white */
    .stSelectbox,
    .stSelectbox *,
    .stSelectbox label,
    .stSelectbox > div,
    .stSelectbox > div > div,
    .stSelectbox > div > div > div,
    .stSelectbox span,
    div[data-baseweb="select"],
    div[data-baseweb="select"] *,
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] span,
    .stSelectbox option,
    .stSelectbox select,
    .stSelectbox select option,
    [data-testid="stSelectbox"] *,
    [data-testid="stSelectbox"] span,
    [data-testid="stSelectbox"] div,
    [data-testid="stSelectbox"] label,
    /* Additional comprehensive selectors for all selectbox elements */
    .stSelectbox div[data-baseweb="select"] span,
    .stSelectbox div[data-baseweb="select"] div,
    .stSelectbox div[data-baseweb="select"] div span,
    .stSelectbox div[data-baseweb="select"] div div,
    .stSelectbox div[data-baseweb="select"] div div span,
    .stSelectbox div[data-baseweb="select"] div div div,
    .stSelectbox div[data-baseweb="select"] div div div span,
    /* Streamlit specific selectbox classes */
    .stSelectbox .css-1d391kg,
    .stSelectbox .css-1lcbmhc,
    .stSelectbox .css-1v0mbdj,
    .stSelectbox [data-testid="stSelectbox"],
    .stSelectbox [data-testid="stSelectbox"] *,
    .stSelectbox [data-testid="stSelectbox"] span,
    .stSelectbox [data-testid="stSelectbox"] div,
    .stSelectbox [data-testid="stSelectbox"] label,
    /* Baseweb select components */
    .stSelectbox [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"] *,
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] div,
    .stSelectbox [data-baseweb="select"] div span,
    .stSelectbox [data-baseweb="select"] div div,
    .stSelectbox [data-baseweb="select"] div div span,
    /* All possible selectbox text elements */
    .stSelectbox *,
    .stSelectbox span,
    .stSelectbox div,
    .stSelectbox label,
    .stSelectbox p,
    .stSelectbox strong,
    .stSelectbox em,
    .stSelectbox b,
    .stSelectbox i {
        color: white !important;
    }
    
    /* Ultra comprehensive selectbox styling - catch all possible cases */
    div[data-baseweb="select"] *,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] label,
    div[data-baseweb="select"] p,
    div[data-baseweb="select"] strong,
    div[data-baseweb="select"] em,
    div[data-baseweb="select"] b,
    div[data-baseweb="select"] i,
    [data-testid="stSelectbox"] *,
    [data-testid="stSelectbox"] span,
    [data-testid="stSelectbox"] div,
    [data-testid="stSelectbox"] label,
    [data-testid="stSelectbox"] p,
    [data-testid="stSelectbox"] strong,
    [data-testid="stSelectbox"] em,
    [data-testid="stSelectbox"] b,
    [data-testid="stSelectbox"] i {
        color: white !important;
    }
    
    /* Force white color on all selectbox related elements */
    .stSelectbox, .stSelectbox *, div[data-baseweb="select"], div[data-baseweb="select"] *, [data-testid="stSelectbox"], [data-testid="stSelectbox"] * {
        color: white !important;
    }
    
    /* Enhanced selectbox selected option styling */
    .stSelectbox option:checked, 
    .stSelectbox option:selected {
        color: white !important;
        background-color: #2d3436 !important;
    }
    
    /* Force white text for all dropdown popup content */
    div[data-baseweb="select"] div[data-baseweb="popover"] *,
    [data-testid="stSelectbox"] div[data-baseweb="popover"] * {
        color: white !important;
        background-color: #2d3436 !important;
    }
    
    /* Ensure dropdown list items are white */
    div[data-baseweb="select"] [role="option"],
    div[data-baseweb="select"] [role="option"] *,
    [data-testid="stSelectbox"] [role="option"],
    [data-testid="stSelectbox"] [role="option"] * {
        color: white !important;
        background-color: #2d3436 !important;
    }
    
    /* Selected/active state for dropdown options */
    div[data-baseweb="select"] [role="option"][aria-selected="true"],
    div[data-baseweb="select"] [role="option"][aria-selected="true"] *,
    [data-testid="stSelectbox"] [role="option"][aria-selected="true"],
    [data-testid="stSelectbox"] [role="option"][aria-selected="true"] * {
        color: white !important;
        background-color: #636e72 !important;
    }
    
    /* Specific styling for dropdown options and popup elements */
    .stSelectbox div[data-baseweb="select"] div[data-baseweb="popover"] *,
    .stSelectbox div[data-baseweb="select"] div[data-baseweb="popover"] span,
    .stSelectbox div[data-baseweb="select"] div[data-baseweb="popover"] div,
    .stSelectbox div[data-baseweb="select"] div[data-baseweb="popover"] li,
    .stSelectbox div[data-baseweb="select"] div[data-baseweb="popover"] ul,
    .stSelectbox div[data-baseweb="select"] div[data-baseweb="popover"] ol,
    .stSelectbox div[data-baseweb="select"] div[data-baseweb="popover"] p,
    .stSelectbox div[data-baseweb="select"] div[data-baseweb="popover"] strong,
    .stSelectbox div[data-baseweb="select"] div[data-baseweb="popover"] em,
    .stSelectbox div[data-baseweb="select"] div[data-baseweb="popover"] b,
    .stSelectbox div[data-baseweb="select"] div[data-baseweb="popover"] i,
    /* Baseweb specific dropdown styling */
    div[data-baseweb="select"] div[data-baseweb="popover"] *,
    div[data-baseweb="select"] div[data-baseweb="popover"] span,
    div[data-baseweb="select"] div[data-baseweb="popover"] div,
    div[data-baseweb="select"] div[data-baseweb="popover"] li,
    div[data-baseweb="select"] div[data-baseweb="popover"] ul,
    div[data-baseweb="select"] div[data-baseweb="popover"] ol,
    div[data-baseweb="select"] div[data-baseweb="popover"] p,
    div[data-baseweb="select"] div[data-baseweb="popover"] strong,
    div[data-baseweb="select"] div[data-baseweb="popover"] em,
    div[data-baseweb="select"] div[data-baseweb="popover"] b,
    div[data-baseweb="select"] div[data-baseweb="popover"] i,
    /* Streamlit test ID specific dropdown styling */
    [data-testid="stSelectbox"] div[data-baseweb="popover"] *,
    [data-testid="stSelectbox"] div[data-baseweb="popover"] span,
    [data-testid="stSelectbox"] div[data-baseweb="popover"] div,
    [data-testid="stSelectbox"] div[data-baseweb="popover"] li,
    [data-testid="stSelectbox"] div[data-baseweb="popover"] ul,
    [data-testid="stSelectbox"] div[data-baseweb="popover"] ol,
    [data-testid="stSelectbox"] div[data-baseweb="popover"] p,
    [data-testid="stSelectbox"] div[data-baseweb="popover"] strong,
    [data-testid="stSelectbox"] div[data-baseweb="popover"] em,
    [data-testid="stSelectbox"] div[data-baseweb="popover"] b,
    [data-testid="stSelectbox"] div[data-baseweb="popover"] i {
        color: white !important;
        background-color: #2d3436 !important;
    }
    
    /* Additional styling for dropdown list items */
    .stSelectbox ul li,
    .stSelectbox ol li,
    div[data-baseweb="select"] ul li,
    div[data-baseweb="select"] ol li,
    [data-testid="stSelectbox"] ul li,
    [data-testid="stSelectbox"] ol li {
        color: white !important;
        background-color: #2d3436 !important;
    }
    
    /* Hover effects for dropdown options */
    .stSelectbox ul li:hover,
    .stSelectbox ol li:hover,
    div[data-baseweb="select"] ul li:hover,
    div[data-baseweb="select"] ol li:hover,
    [data-testid="stSelectbox"] ul li:hover,
    [data-testid="stSelectbox"] ol li:hover {
        color: white !important;
        background-color: #636e72 !important;
    }
    
    /* Specific sidebar selectbox styles */
    .css-1d391kg *, .css-1lcbmhc *, .css-1v0mbdj *,
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stSelectbox *,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSelectbox > div,
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stSelectbox > div > div > div,
    [data-testid="stSidebar"] .stSelectbox span,
    [data-testid="stSidebar"] div[data-baseweb="select"],
    [data-testid="stSidebar"] div[data-baseweb="select"] *,
    [data-testid="stSidebar"] div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: white !important;
        background-color: #2d3436 !important;
    }
    
    /* Ultra-specific sidebar dropdown styling */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-baseweb="popover"] *,
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-baseweb="popover"] span,
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-baseweb="popover"] div,
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-baseweb="popover"] li,
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-baseweb="popover"] ul,
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-baseweb="popover"] ol,
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-baseweb="popover"] p,
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-baseweb="popover"] strong,
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-baseweb="popover"] em,
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-baseweb="popover"] b,
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-baseweb="popover"] i,
    /* Sidebar specific dropdown list items */
    [data-testid="stSidebar"] .stSelectbox ul li,
    [data-testid="stSidebar"] .stSelectbox ol li,
    [data-testid="stSidebar"] div[data-baseweb="select"] ul li,
    [data-testid="stSidebar"] div[data-baseweb="select"] ol li,
    /* Sidebar hover effects */
    [data-testid="stSidebar"] .stSelectbox ul li:hover,
    [data-testid="stSidebar"] .stSelectbox ol li:hover,
    [data-testid="stSidebar"] div[data-baseweb="select"] ul li:hover,
    [data-testid="stSidebar"] div[data-baseweb="select"] ol li:hover {
        color: white !important;
        background-color: #636e72 !important;
    }
    
    /* Force white text on all sidebar elements */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Additional sidebar selectbox targeting */
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stSelectbox *,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSelectbox span,
    [data-testid="stSidebar"] .stSelectbox div,
    [data-testid="stSidebar"] .stSelectbox p,
    [data-testid="stSidebar"] .stSelectbox strong,
    [data-testid="stSidebar"] .stSelectbox em,
    [data-testid="stSidebar"] .stSelectbox b,
    [data-testid="stSidebar"] .stSelectbox i {
        color: white !important;
    }
    
    /* ==== FORCE All sidebar selectbox text to be white ==== */
    [data-testid="stSidebar"] .stSelectbox *,
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] select,
    [data-testid="stSidebar"] option,
    [data-testid="stSidebar"] div[data-baseweb="select"] *,
    [data-testid="stSidebar"] div[data-baseweb="select"] {
        color: white !important;
    }
   
            
    .main-header {
        background: linear-gradient(135deg, var(--earth-brown) 0%, var(--cream-dark) 50%, var(--earth-green) 100%);
        padding: 2.5rem;
        border-radius: 20px; 
        color: var(--text-primary);
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        font-weight: 700;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .expert-response-container {
        background: linear-gradient(135deg, var(--cream-light) 0%, var(--cream-medium) 100%);
        border: 3px solid var(--earth-green);
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(122, 132, 113, 0.2);
        overflow: hidden;
    }
    
    .response-header {
        background: linear-gradient(135deg, var(--earth-green) 0%, var(--earth-brown) 100%);
        color: white;
        padding: 1.5rem 2rem;
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        border-bottom: 3px solid var(--earth-brown);
    }
    
    .response-content {
        padding: 2.5rem;
        color: var(--text-primary);
        line-height: 1.8;
        font-size: 16px;
        text-align: justify;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .response-content .section-header {
        background: linear-gradient(135deg, var(--earth-brown) 0%, var(--earth-green) 100%);
        color: white !important;
        padding: 1.2rem 2rem;
        margin: 2.5rem -2.5rem 2rem -2.5rem;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        text-align: center;
        border-radius: 0;
        box-shadow: 0 4px 15px rgba(139, 115, 85, 0.3);
    }
    
    .bullet-point {
        background: linear-gradient(135deg, var(--cream-medium) 0%, var(--cream-dark) 100%);
        margin: 0.8rem 0;
        padding: 1rem 1.5rem;
        border-left: 5px solid var(--earth-green);
        border-radius: 0 10px 10px 0;
        box-shadow: 0 3px 10px rgba(122, 132, 113, 0.15);
        font-weight: 500;
        transition: all 0.3s ease;
        text-align: left;
        line-height: 1.6;
    }
    
    .bullet-point:hover {
        transform: translateX(10px);
        box-shadow: 0 5px 15px rgba(122, 132, 113, 0.25);
    }
    
    .important-note {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 2px solid #f39c12;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 2rem 0;
        box-shadow: 0 6px 20px rgba(243, 156, 18, 0.2);
        font-weight: 600;
        color: #856404;
        text-align: left;
        line-height: 1.6;
    }
    
    .response-table {
        margin: 2rem 0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        background: white;
    }
    
    .response-table table {
        width: 100% !important;
        border-collapse: collapse !important;
        margin: 0 !important;
    }
    
    .response-table th {
        background: linear-gradient(135deg, #2d3436 0%, #636e72 100%) !important;
        color: white !important;
        font-weight: bold !important;
        padding: 1.2rem !important;
        text-align: center !important;
        font-size: 1rem !important;
        border-bottom: 3px solid var(--earth-green) !important;
    }
    
    .response-table td {
        padding: 1rem !important;
        border: 1px solid #e0e0e0 !important;
        color: #2d3436 !important;
        font-size: 0.95rem !important;
        vertical-align: middle !important;
        text-align: center !important;
    }
    
    .response-table tr:nth-child(even) {
        background: linear-gradient(135deg, #f9f9f9 0%, #f5f5f5 100%) !important;
    }
    
    .response-table tr:hover {
        background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%) !important;
        transform: scale(1.01);
        transition: all 0.3s ease !important;
    }
    
    .response-section-card {
        background: linear-gradient(135deg, var(--cream-light) 0%, var(--cream-medium) 100%);
        border: 2px solid var(--earth-green);
        border-radius: 15px;
        margin: 2rem 0;
        padding: 0;
        box-shadow: 0 8px 25px rgba(122, 132, 113, 0.2);
        overflow: hidden;
    }
    
    .card-header {
        background: linear-gradient(135deg, var(--earth-green) 0%, var(--earth-brown) 100%);
        color: white;
        padding: 1.2rem 2rem;
        font-size: 1.3rem;
        font-weight: bold;
        text-align: center;
        border-bottom: 3px solid var(--earth-brown);
    }
    
    .card-content {
        padding: 2rem;
        color: var(--text-primary);
        line-height: 1.7;
        text-align: justify;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .metric-card {
        background: linear-gradient(135deg, var(--cream-medium) 0%, var(--cream-dark) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--earth-brown);
        text-align: center;
        color: var(--text-primary);
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(139, 115, 85, 0.15);
        transition: transform 0.3s ease;
    }
    
    .recommendation-box {
        background: linear-gradient(135deg, var(--cream-light) 0%, var(--cream-medium) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid var(--earth-green);
        margin: 1rem 0;
        color: var(--text-primary);
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(122, 132, 113, 0.15);
        text-align: left;
        line-height: 1.6;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--earth-green) 0%, var(--earth-brown) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        font-size: 16px;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(122, 132, 113, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(122, 132, 113, 0.4);
    }
    
    .stButton > button[data-testid*="enhanced_quick_"] {
        background: linear-gradient(135deg, #2d3436 0%, #636e72 100%) !important;
        color: white !important;
        border: 2px solid #7a8471 !important;
        font-size: 13px !important;
        padding: 0.8rem 1rem !important;
        margin: 0.4rem 0 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[data-testid*="enhanced_quick_"]:hover {
        background: linear-gradient(135deg, #7a8471 0%, #8b7355 100%) !important;
        transform: translateX(5px) !important;
        box-shadow: 0 4px 12px rgba(122, 132, 113, 0.3) !important;
    }
    
    h1, h2, h3, h4 { 
        color: var(--text-primary) !important; 
        font-weight: 700;
    }
    
    p, li, span, div { 
        color: var(--text-primary) !important; 
        font-size: 16px;
    }
    
    /* Code block styling - white text for code snippets - COMPREHENSIVE */
    /* All code blocks and inline code */
    pre,
    code,
    pre code,
    code pre,
    .response-content pre,
    .response-content pre code,
    .response-content code,
    /* Streamlit markdown code blocks */
    div[data-testid="stMarkdownContainer"] pre,
    div[data-testid="stMarkdownContainer"] pre code,
    div[data-testid="stMarkdownContainer"] code,
    /* Chat message code blocks */
    .stChatMessage pre,
    .stChatMessage pre code,
    .stChatMessage code,
    /* All possible code block selectors */
    div pre,
    div pre code,
    div code,
    p code,
    li code,
    span code,
    /* Streamlit code component */
    .stCodeBlock pre,
    .stCodeBlock code,
    /* Generic code elements */
    * pre,
    * pre code,
    * code {
        color: white !important;
        background-color: #2d3436 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    
    /* Code block containers */
    pre,
    .response-content pre,
    div[data-testid="stMarkdownContainer"] pre,
    .stChatMessage pre,
    div pre {
        padding: 1rem !important;
        border-radius: 8px !important;
        overflow-x: auto !important;
        border: 1px solid #636e72 !important;
        margin: 1rem 0 !important;
        background-color: #2d3436 !important;
    }
    
    /* Code inside pre blocks */
    pre code,
    .response-content pre code,
    div[data-testid="stMarkdownContainer"] pre code,
    .stChatMessage pre code,
    div pre code {
        padding: 0 !important;
        background-color: transparent !important;
        color: white !important;
    }
    
    /* Inline code (not in pre blocks) */
    code:not(pre code),
    .response-content code:not(pre code),
    div[data-testid="stMarkdownContainer"] code:not(pre code),
    p code,
    li code,
    span code {
        padding: 0.2rem 0.4rem !important;
        border-radius: 4px !important;
        color: white !important;
        background-color: #2d3436 !important;
        font-size: 0.9em !important;
    }
     
</style>
""", unsafe_allow_html=True)

# Agricultural data constants - REALISTIC VALUES
BASE_COSTS = {
    "Rice": 60000, "Wheat": 50000, "Cotton": 70000, "Sugarcane": 80000, 
    "Maize": 55000, "Groundnut": 65000, "Soybean": 58000, "Turmeric": 120000,
    "Onion": 85000, "Tomato": 95000, "Mango": 250000, "Grapes": 300000,
    "Tea": 400000, "Coffee": 350000, "Cardamom": 500000, "Black Pepper": 300000
}

YIELD_DATA = {
    "Rice": {"yield_kg": 2800, "price_kg": 20}, "Wheat": {"yield_kg": 3200, "price_kg": 22},
    "Cotton": {"yield_kg": 2200, "price_kg": 65}, "Sugarcane": {"yield_kg": 65000, "price_kg": 3.5},
    "Maize": {"yield_kg": 4500, "price_kg": 18}, "Groundnut": {"yield_kg": 2000, "price_kg": 45},
    "Soybean": {"yield_kg": 2500, "price_kg": 35}, "Turmeric": {"yield_kg": 8000, "price_kg": 150},
    "Onion": {"yield_kg": 25000, "price_kg": 12}, "Tomato": {"yield_kg": 30000, "price_kg": 15},
    "Mango": {"yield_kg": 0, "price_kg": 45}, "Grapes": {"yield_kg": 12000, "price_kg": 150}  # Mango takes 4-5 years
}

GOVERNMENT_SCHEMES = {
    "PM-KISAN": {"benefit": 6000, "eligibility": "Small & Marginal Farmers", "application": "pm-kisan.gov.in", "contact": "1800-115-526"},
    "PMFBY": {"benefit": "Crop Insurance", "eligibility": "All Farmers", "application": "pmfby.gov.in", "contact": "1800-200-7710"},
    "KCC": {"benefit": "Credit up to ₹3 Lakh", "eligibility": "Landowner Farmers", "application": "Banks/CSCs", "contact": "1800-270-3333"},
    "NMSA": {"benefit": "₹50,000 Subsidy", "eligibility": "Sustainable Agriculture", "application": "Agriculture Dept", "contact": "1800-180-1551"},
    "PKVY": {"benefit": "₹31,000/ha", "eligibility": "Organic Farmers", "application": "State Agriculture Dept", "contact": "1800-180-1551"}
}

CONTACT_DIRECTORY = {
    "🌾 Agriculture Helpline": {"number": "1800-180-1551", "purpose": "General farming queries & crop advisory"},
    "💰 Kisan Credit Card": {"number": "1800-270-3333", "purpose": "Credit, loans & financial assistance"},
    "🚜 Equipment Subsidy": {"number": "1800-115-526", "purpose": "Farm machinery & equipment subsidies"},
    "🌡️ Weather Advisory": {"number": "1800-180-1551", "purpose": "Weather alerts & climate advice"},
    "📈 Market Intelligence": {"website": "enam.gov.in", "purpose": "Live market prices & trading"},
    "🏥 Crop Insurance": {"number": "1800-200-7710", "purpose": "Insurance claims & support"}
}

# Language translations
TRANSLATIONS = {
    "English": {
        "greeting": "Welcome!",
        "expert_response": "Agricultural Expert Response"
    },
    "हिंदी (Hindi)": {
        "greeting": "स्वागत है!",
        "expert_response": "कृषि विशेषज्ञ प्रतिक्रिया"
    },
    "தமிழ் (Tamil)": {
        "greeting": "வணக்கம்!",
        "expert_response": "விவசாய நிபுணர் பதில்"
    },
    "తెలుగు (Telugu)": {
        "greeting": "స్వాగతం!",
        "expert_response": "వ్యవసాయ నిపుణుడి సమాధానం"
    },
    "ಕನ್ನಡ (Kannada)": {
        "greeting": "ಸ್ವಾಗತ!",
        "expert_response": "ಕೃಷಿ ತಜ್ಞರ ಪ್ರತಿಕ್ರಿಯೆ"
    },
    "বাংলা (Bengali)": {
        "greeting": "স্বাগতম!",
        "expert_response": "কৃষি বিশেষজ্ঞের উত্তর"
    }
}

def initialize_gemini():
    """Initialize Gemini API - Secure server-side implementation"""
    from secure_config import get_gemini_api_key, validate_api_key
    
    # Get API key securely from server-side sources only (never from user input)
    api_key = get_gemini_api_key()
    
    if not validate_api_key(api_key):
        st.error("""
        ⚠️ **API Key Not Configured**
        
        Please configure your Gemini API key using one of these methods:
        
        **For Streamlit Cloud:**
        1. Go to your app settings
        2. Navigate to "Secrets" section
        3. Add: `GEMINI_API_KEY = "your-api-key-here"`
        
        **For Local Development:**
        1. Create `.streamlit/secrets.toml` file
        2. Add: `GEMINI_API_KEY = "your-api-key-here"`
        
        **For Docker:**
        Set environment variable: `GEMINI_API_KEY=your-api-key-here`
        """)
        return None
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        return model
    except Exception as e:
        st.error(f"❌ Error initializing Gemini: {str(e)}")
        return None

def extract_and_format_tables(text):
    """Extract and convert markdown tables to styled HTML tables"""
    table_pattern = r'\|(.+?)\|\s*\n\|[ \-|:\s]+\|\s*\n((?:\|.*?\|(?:\s*\n|$))+)'
    
    def replace_table(match):
        header_row = match.group(1).strip()
        data_rows = match.group(2).strip().split('\n')
        
        headers = [cell.strip() for cell in header_row.split('|') if cell.strip()]
        
        rows = []
        for row in data_rows:
            if row.strip().startswith('|'):
                cells = [cell.strip() for cell in row.split('|') if cell.strip()]
                if cells and len(cells) == len(headers):
                    rows.append(cells)
        
        html_table = '<div class="response-table"><table>'
        html_table += '<tr>'
        for header in headers:
            html_table += f'<th>{html.escape(header)}</th>'
        html_table += '</tr>'
        
        for row in rows:
            html_table += '<tr>'
            for cell in row:
                html_table += f'<td>{html.escape(cell)}</td>'
            html_table += '</tr>'
        
        html_table += '</table></div>'
        return html_table
    
    formatted_text = re.sub(table_pattern, replace_table, text, flags=re.MULTILINE | re.DOTALL)
    return formatted_text

def create_section_cards(text):
    """Convert sections into styled cards"""
    sections = re.split(r'##\s*([^\n]+)\n', text)[1:]
    formatted_sections = []
    
    for i in range(0, len(sections), 2):
        header = sections[i].strip()
        content = sections[i + 1].strip() if i + 1 < len(sections) else ""
        
        icon_map = {
            'direct answer': ('🎯', 'Direct Answer'),
            'cost breakdown': ('💰', 'Cost Breakdown'),
            'government schemes': ('🏛️', 'Government Schemes'),
            'best practices': ('⭐', 'Best Practices'),
            'risk mitigation': ('🛡️', 'Risk Mitigation'),
            'roi analysis': ('📈', 'ROI Analysis'),
            'market trends': ('📊', 'Market Trends')
        }
        
        header_lower = header.lower()
        icon, title = next(
            (icon, title) for key, (icon, title) in icon_map.items()
            if key in header_lower
        ) if any(key in header_lower for key in icon_map) else ('📋', header)
        
        if content:
            content_html = markdown2.markdown(content, extras=['fenced-code-blocks', 'tables'])
            content_html = re.sub(
                r'<li>(.*?)</li>',
                r'<div class="bullet-point">• \1</div>',
                content_html,
                flags=re.DOTALL
            )
            
            section_card = f"""
            <div class="response-section-card">
                <div class="card-header">{icon} {html.escape(title)}</div>
                <div class="card-content">{content_html}</div>
            </div>
            """
            formatted_sections.append(section_card)
    
    return formatted_sections

def clean_and_format_response(text):
    """Clean and format response text with markdown-to-HTML conversion"""
    text = html.unescape(text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ ]{2,}', ' ', text)
    text = markdown2.markdown(text, extras=['fenced-code-blocks', 'tables'])
    text = re.sub(
        r'<li>(.*?)</li>',
        r'<div class="bullet-point">• \1</div>',
        text,
        flags=re.DOTALL
    )
    text = re.sub(
        r'<strong>Important:</strong>\s*(.+?)(?=<(?:h[1-6]|p|div))',
        r'<div class="important-note">⚠️ <strong>Important:</strong> \1</div>',
        text,
        flags=re.DOTALL
    )
    return text.strip()

def create_crop_recommendation_analysis(region, query, context="default"):
    """Create tailored crop recommendation analysis based on query"""
    st.markdown("### 🌾 **Crop Performance & Recommendations**")
    
    if region in ['Punjab', 'Haryana']:
        suitable_crops = ['Wheat', 'Rice', 'Maize', 'Cotton']
    elif region in ['Maharashtra', 'Gujarat']:
        suitable_crops = ['Cotton', 'Sugarcane', 'Soybean', 'Onion']
    elif region in ['Tamil Nadu', 'Karnataka']:
        suitable_crops = ['Rice', 'Turmeric', 'Mango', 'Coffee']
    else:
        suitable_crops = ['Rice', 'Wheat', 'Maize', 'Groundnut']
    
    query_lower = query.lower()
    filtered_crops = [
        crop for crop in suitable_crops 
        if crop.lower() in query_lower or any(keyword in query_lower for keyword in ['crop', 'recommend', 'plant', 'grow'])
    ] or suitable_crops
    
    crop_performance = []
    for crop in filtered_crops:
        if crop in BASE_COSTS and crop in YIELD_DATA:
            cost = BASE_COSTS[crop]
            yield_kg = YIELD_DATA[crop]['yield_kg']
            price_kg = YIELD_DATA[crop]['price_kg']
            
            if crop == 'Mango':
                revenue = 0
                profit = -cost
                roi = -100
            else:
                revenue = yield_kg * price_kg * 0.85
                profit = revenue - cost
                roi = (profit / cost * 100) if cost > 0 else 0
            
            crop_performance.append({
                'Crop': crop,
                'Investment': cost,
                'Expected_Yield_kg': yield_kg,
                'Revenue': revenue,
                'Profit': profit,
                'ROI_Percent': roi
            })
    
    df_crops = pd.DataFrame(crop_performance)
    
    if not df_crops.empty:
        df_positive_roi = df_crops[df_crops['ROI_Percent'] >= 0]
        
        if not df_positive_roi.empty:
            fig_roi = px.bar(
                df_positive_roi,
                x='Crop',
                y='ROI_Percent',
                title=f"ROI Comparison for {region} (Annual Crops Only)",
                color='ROI_Percent',
                color_continuous_scale='Greens',
                text='ROI_Percent'
            )
            fig_roi.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>ROI: %{y:.1f}%<extra></extra>'
            )
            fig_roi.update_layout(
                font=dict(size=14, color='#000000'), # Font color black
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title_font_color='#000000',
                height=500,
                hovermode='closest',
                legend=dict(
                    font=dict(color='#000000'), # Legend font color black
                    title_font=dict(color='#000000') # Legend title font color black
                ),
                xaxis=dict(
                    title_font=dict(color='#000000'),
                    tickfont=dict(color='#000000'),
                    color='#000000'
                ),
                yaxis=dict(
                    title_font=dict(color='#000000'),
                    tickfont=dict(color='#000000'),
                    color='#000000'
                )
            )
            st.plotly_chart(fig_roi, use_container_width=True, key=f"roi_chart_crop_recommendation_{context}")
        
        st.markdown("#### 🏆 **Top Crop Recommendations**")
        annual_crops = df_crops[df_crops['ROI_Percent'] >= 0].nlargest(3, 'ROI_Percent')
        perennial_crops = df_crops[df_crops['ROI_Percent'] < 0]
        
        for i, (_, crop) in enumerate(annual_crops.iterrows()):
            rank_emoji = ['🥇', '🥈', '🥉'][i]
            
            investment_str = f"{crop['Investment']:,}"
            yield_str = f"{crop['Expected_Yield_kg']:,}"
            revenue_str = f"{crop['Revenue']:,}"
            roi_str = f"{crop['ROI_Percent']:.1f}"
            
            html_content = f"""
            <div class='recommendation-box'>
                <h4>{rank_emoji} Rank {i+1}: {crop['Crop']} (Annual Crop)</h4>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
                    <div>
                        <p><strong>💰 Investment:</strong> ₹{investment_str}/acre</p>
                        <p><strong>🌾 Expected Yield:</strong> {yield_str} kg/acre</p>
                    </div>
                    <div>
                        <p><strong>💵 Expected Revenue:</strong> ₹{revenue_str}</p>
                        <p><strong>📈 ROI:</strong> {roi_str}%</p>
                    </div>
                </div>
            </div>
            """
            st.markdown(html_content, unsafe_allow_html=True)
        
        for _, crop in perennial_crops.iterrows():
            investment_str = f"{crop['Investment']:,}"
            
            html_content = f"""
            <div class='recommendation-box' style='border: 2px solid #f39c12;'>
                <h4>⚠️ {crop['Crop']} (Perennial Crop - Long-term Investment)</h4>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
                    <div>
                        <p><strong>💰 Initial Investment:</strong> ₹{investment_str}/acre</p>
                        <p><strong>⏰ Gestation Period:</strong> 4-5 years</p>
                    </div>
                    <div>
                        <p><strong>💵 Year 1-4 Revenue:</strong> ₹0 (No income)</p>
                        <p><strong>📈 Long-term ROI:</strong> 25-30% (after maturity)</p>
                    </div>
                </div>
                <p style='color: #856404; font-weight: 600; margin-top: 1rem;'>
                    ⚠️ <strong>Note:</strong> Requires patience and long-term planning. Good returns only after 5+ years.
                </p>
            </div>
            """
            st.markdown(html_content, unsafe_allow_html=True)
            
# def create_crop_recommendation_analysis(region, query, context="default"):
#     """Create tailored crop recommendation analysis based on query"""
#     st.markdown("### 🌾 **Crop Performance & Recommendations**")
    
#     if region in ['Punjab', 'Haryana']:
#         suitable_crops = ['Wheat', 'Rice', 'Maize', 'Cotton']
#     elif region in ['Maharashtra', 'Gujarat']:
#         suitable_crops = ['Cotton', 'Sugarcane', 'Soybean', 'Onion']
#     elif region in ['Tamil Nadu', 'Karnataka']:
#         suitable_crops = ['Rice', 'Turmeric', 'Mango', 'Coffee']
#     else:
#         suitable_crops = ['Rice', 'Wheat', 'Maize', 'Groundnut']
    
#     # Filter crops based on query (e.g., if user mentions specific crops)
#     query_lower = query.lower()
#     filtered_crops = [
#         crop for crop in suitable_crops 
#         if crop.lower() in query_lower or any(keyword in query_lower for keyword in ['crop', 'recommend', 'plant', 'grow'])
#     ] or suitable_crops  # Fallback to suitable crops if no specific crops mentioned
    
#     crop_performance = []
#     for crop in filtered_crops:
#         if crop in BASE_COSTS and crop in YIELD_DATA:
#             cost = BASE_COSTS[crop]
#             yield_kg = YIELD_DATA[crop]['yield_kg']
#             price_kg = YIELD_DATA[crop]['price_kg']
            
#             # Special handling for perennial crops like Mango
#             if crop == 'Mango':
#                 revenue = 0  # No revenue in first few years
#                 profit = -cost  # Pure loss initially
#                 roi = -100  # Negative ROI initially
#             else:
#                 revenue = yield_kg * price_kg * 0.85  # 85% success rate
#                 profit = revenue - cost
#                 roi = (profit / cost * 100) if cost > 0 else 0
            
#             crop_performance.append({
#                 'Crop': crop,
#                 'Investment': cost,
#                 'Expected_Yield_kg': yield_kg,
#                 'Revenue': revenue,
#                 'Profit': profit,
#                 'ROI_Percent': roi
#             })
    
#     df_crops = pd.DataFrame(crop_performance)
    
#     if not df_crops.empty:
#         # Filter out crops with negative ROI for the chart
#         df_positive_roi = df_crops[df_crops['ROI_Percent'] >= 0]
        
#         if not df_positive_roi.empty:
#             fig_roi = px.bar(df_positive_roi, x='Crop', y='ROI_Percent',
#                             title=f"ROI Comparison for {region} (Annual Crops Only)",
#                             color='ROI_Percent', color_continuous_scale='Greens',
#                             text='ROI_Percent')
#             fig_roi.update_traces(
#                 texttemplate='%{text:.1f}%', 
#                 textposition='outside',
#                 hovertemplate='<b>%{x}</b><br>ROI: %{y:.1f}%<extra></extra>'
#             )
#             fig_roi.update_layout(
#                 font=dict(size=14, color='#2d3436'),
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 plot_bgcolor='rgba(0,0,0,0)',
#                 title_font_color='#2d3436',
#                 height=500,
#                 hovermode='closest'
#             )
#             st.plotly_chart(fig_roi, use_container_width=True, key=f"roi_chart_crop_recommendation_{context}")
        
#         st.markdown("#### 🏆 **Top Crop Recommendations**")
#         # Sort by ROI but handle perennial crops separately
#         annual_crops = df_crops[df_crops['ROI_Percent'] >= 0].nlargest(3, 'ROI_Percent')
#         perennial_crops = df_crops[df_crops['ROI_Percent'] < 0]
        
#         for i, (_, crop) in enumerate(annual_crops.iterrows()):
#             rank_emoji = ['🥇', '🥈', '🥉'][i]
            
#             investment_str = f"{crop['Investment']:,}"
#             yield_str = f"{crop['Expected_Yield_kg']:,}"
#             revenue_str = f"{crop['Revenue']:,}"
#             roi_str = f"{crop['ROI_Percent']:.1f}"
            
#             html_content = f"""
#             <div class='recommendation-box'>
#                 <h4>{rank_emoji} Rank {i+1}: {crop['Crop']} (Annual Crop)</h4>
#                 <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
#                     <div>
#                         <p><strong>💰 Investment:</strong> ₹{investment_str}/acre</p>
#                         <p><strong>🌾 Expected Yield:</strong> {yield_str} kg/acre</p>
#                     </div>
#                     <div>
#                         <p><strong>💵 Expected Revenue:</strong> ₹{revenue_str}</p>
#                         <p><strong>📈 ROI:</strong> {roi_str}%</p>
#                     </div>
#                 </div>
#             </div>
#             """
#             st.markdown(html_content, unsafe_allow_html=True)
        
#         # Show perennial crops with warnings
#         for _, crop in perennial_crops.iterrows():
#             investment_str = f"{crop['Investment']:,}"
            
#             html_content = f"""
#             <div class='recommendation-box' style='border: 2px solid #f39c12;'>
#                 <h4>⚠️ {crop['Crop']} (Perennial Crop - Long-term Investment)</h4>
#                 <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
#                     <div>
#                         <p><strong>💰 Initial Investment:</strong> ₹{investment_str}/acre</p>
#                         <p><strong>⏰ Gestation Period:</strong> 4-5 years</p>
#                     </div>
#                     <div>
#                         <p><strong>💵 Year 1-4 Revenue:</strong> ₹0 (No income)</p>
#                         <p><strong>📈 Long-term ROI:</strong> 25-30% (after maturity)</p>
#                     </div>
#                 </div>
#                 <p style='color: #856404; font-weight: 600; margin-top: 1rem;'>
#                     ⚠️ <strong>Note:</strong> Requires patience and long-term planning. Good returns only after 5+ years.
#                 </p>
#             </div>
#             """
#             st.markdown(html_content, unsafe_allow_html=True)

def parse_gemini_response(response_text, question, region, farm_size, language="English"):
    """Parse and display Gemini response with improved formatting and alignment"""
    header_text = TRANSLATIONS.get(language, {}).get("expert_response", "Agricultural Expert Response")
    
    st.markdown(f"""
    <div class='expert-response-container'>
        <div class='response-header'>
            🧠 {header_text}
            <div style='font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;'>
                📍 {region} | 🏡 {farm_size} | 🌾 Personalized Analysis
            </div>
        </div>
        <div class='response-content'>
    """, unsafe_allow_html=True)
    
    if any(keyword in question.lower() for keyword in ['crop', 'recommend', 'plant', 'grow']):
        create_crop_recommendation_analysis(region, question, "ai_response")
        st.markdown("---")
    
    response_with_tables = extract_and_format_tables(response_text)
    section_cards = create_section_cards(response_with_tables)
    
    if section_cards:
        for card in section_cards:
            st.markdown(card, unsafe_allow_html=True)
    else:
        cleaned_response = clean_and_format_response(response_text)
        st.markdown(cleaned_response, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Detailed Analysis", use_container_width=True):
            create_financial_analysis(question, region, farm_size)
    
    with col2:
        if st.button("🎯 Government Schemes", use_container_width=True):
            create_government_schemes_analysis(question)
    
    with col3:
        if st.button("📅 Crop Planning", use_container_width=True):
            create_crop_plan_diagram(region, question)

def create_financial_analysis(query, region, farm_size):
    """Create ultra-realistic financial analysis based on query"""
    st.markdown("### 💰 **Ultra-Realistic Financial Analysis**")
    
    query_lower = query.lower()
    crop = next((c for c in BASE_COSTS if c.lower() in query_lower), 'Rice')
    
    # Parse farm size to get numeric value
    farm_size_multiplier = 1
    if "Small" in farm_size:
        farm_size_multiplier = 1
    elif "Medium" in farm_size:
        farm_size_multiplier = 5
    elif "Large" in farm_size:
        farm_size_multiplier = 25
    elif "Very Large" in farm_size:
        farm_size_multiplier = 75
    
    # Adjust costs based on farm size
    base_cost = BASE_COSTS[crop] * farm_size_multiplier
    
    # REALISTIC COST BREAKDOWN (based on agricultural studies)
    cost_components = {
        'Seeds & Planting Material': base_cost * 0.10,  # 10%
        'Fertilizers & Nutrients': base_cost * 0.22,    # 22% 
        'Labor & Operations': base_cost * 0.38,         # 38% (biggest cost)
        'Irrigation & Water': base_cost * 0.12,         # 12%
        'Pesticides & Protection': base_cost * 0.08,    # 8%
        'Equipment & Machinery': base_cost * 0.06,      # 6%
        'Other Expenses': base_cost * 0.04              # 4% (transport, storage)
    }
    
    df_costs = pd.DataFrame(list(cost_components.items()), columns=['Category', 'Amount'])
    
    st.markdown("#### 📊 **Investment Breakdown Analysis**")
    
    fig_pie = px.pie(df_costs, values='Amount', names='Category',
                    title=f"Investment Breakdown for {crop} in {region}",
                    color_discrete_sequence=['#8b7355', '#7a8471', '#a39081', '#9ca986', '#8b9a7e', '#aabbcc', '#ccddee'])
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(
        font=dict(size=14, color='#2d3436'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_color='#2d3436',
        height=500
    )
    st.plotly_chart(fig_pie, use_container_width=True, key="pie_chart_financial")
    
    st.markdown("#### 💡 **Realistic Financial Summary**")
    
    total_investment = sum(cost_components.values())
    yield_data = YIELD_DATA.get(crop, {"yield_kg": 2000, "price_kg": 20})
    
    # SPECIAL CALCULATIONS FOR PERENNIAL CROPS
    if crop == 'Mango':
        # First 4 years: only investment, no income
        years_to_maturity = 4
        mature_yield = 7000 * farm_size_multiplier  # kg after maturity
        mature_revenue = mature_yield * yield_data['price_kg']
        mature_profit = mature_revenue - (total_investment * 0.3)  # 30% annual maintenance
        annual_roi_after_maturity = (mature_profit / total_investment * 100)
        
        payback_period = f"{years_to_maturity + 2}-{years_to_maturity + 4} years"
        expected_revenue = 0  # No revenue in first year
        profit = -total_investment  # Loss in first year
        roi_percent = -100  # Loss in year 1
        
    else:
        # Annual crops with realistic success rates
        expected_yield = yield_data['yield_kg'] * farm_size_multiplier * 0.75  # 75% average success rate
        expected_revenue = expected_yield * yield_data['price_kg'] * 0.85  # 15% post-harvest losses
        profit = expected_revenue - total_investment
        roi_percent = (profit / total_investment * 100) if total_investment > 0 else 0
        
        if crop in ['Cotton', 'Sugarcane']:
            payback_period = "12-18 months"
        else:
            payback_period = "8-12 months"
    
    # RISK FACTORS
    risk_factors = {
        'Mango': "⚠️ No income for 4+ years, disease risk, market volatility",
        'Rice': "⚠️ Monsoon dependency, pest attacks, storage losses", 
        'Wheat': "⚠️ Hailstorm risk, price volatility, timely harvest critical",
        'Cotton': "⚠️ Bollworm attacks, quality issues, export dependency",
        'Sugarcane': "⚠️ Water intensive, mill payment delays, pest issues",
        'Onion': "⚠️ High price volatility, storage losses, export bans",
        'Tomato': "⚠️ Pest attacks, price crashes, perishable nature"
    }
    
    # DISPLAY METRICS
    col1, col2, col3, col4 = st.columns(4)
    
    if crop == 'Mango':
        metrics = [
            (f"₹{total_investment:,.0f}", "Initial Investment", "💰"),
            (f"{annual_roi_after_maturity:.1f}%", "ROI After Maturity", "📈"),
            (payback_period, "Payback Period", "⏰"),
            (f"₹{mature_profit:,.0f}", "Annual Profit (Mature)", "💵")
        ]
    else:
        metrics = [
            (f"₹{total_investment:,.0f}", "Total Investment", "💰"),
            (f"{roi_percent:.1f}%", "Expected ROI", "📈"),
            (payback_period, "Payback Period", "⏰"),
            (f"₹{profit:,.0f}", "Expected Profit", "💵")
        ]
    
    for col, (value, label, emoji) in zip([col1, col2, col3, col4], metrics):
        with col:
            html_content = f"""
            <div class='metric-card' style='text-align: center; padding: 1.5rem; margin: 0.5rem 0;'>
                <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>{emoji}</div>
                <div style='font-size: 1.8rem; font-weight: bold; color: #2d3436; margin-bottom: 0.5rem;'>{value}</div>
                <div style='font-size: 1rem; color: #636e72; font-weight: 600;'>{label}</div>
            </div>
            """
            st.markdown(html_content, unsafe_allow_html=True)
    
    # REALITY CHECK SECTION
    st.markdown("---")
    st.markdown("#### 🎯 **Reality Check**")
    
    if crop == 'Mango':
        st.error(f"""
        **MANGO FARMING REALITY:**
        • ❌ **No income for first 4-5 years**
        • ❌ **High water requirement: 4-5 lakh liters/tree/year**
        • ❌ **Pest & disease management critical**
        • ✅ **Good returns after year 6-8**
        • ✅ **25-30 year productive life**
        """)
    
    risk_factor = risk_factors.get(crop, "⚠️ Standard agricultural risks apply")
    st.warning(f"""
    **RISK FACTORS**: {risk_factor}
    
    **IMPORTANT DISCLAIMERS:**
    • Yields shown are OPTIMISTIC - expect 20-30% lower in reality
    • Prices fluctuate ±40% seasonally
    • First-time farmers typically get 50% lower yields
    • Climate change affecting traditional patterns
    • Input costs increasing 8-12% annually
    • Post-harvest losses: 15-25% for most crops
    """)
    
    # MARKET REALITY
    st.info(f"""
    💡 **CURRENT MARKET REALITY ({region})**:
    • **{crop.capitalize()} price range**: ₹{yield_data['price_kg']-8} - ₹{yield_data['price_kg']+12} per kg
    • **Typical farmer gets**: ₹{yield_data['price_kg']-5} per kg (after middleman)
    • **Storage losses**: 15-25% for most crops
    • **Transportation cost**: ₹2-4 per kg to market
    • **Success rate**: 75% for experienced farmers, 50% for beginners
    """)

def create_government_schemes_analysis(query):
    """Display government schemes relevant to the query"""
    st.markdown("### 🎯 **Government Schemes & Benefits**")
    
    query_lower = query.lower()
    relevant_schemes = {
        scheme: details for scheme, details in GOVERNMENT_SCHEMES.items()
        if any(keyword in query_lower for keyword in [scheme.lower(), 'subsidy', 'scheme', 'government'])
    } or GOVERNMENT_SCHEMES
    
    col1, col2 = st.columns(2)
    for i, (scheme, details) in enumerate(relevant_schemes.items()):
        container = col1 if i % 2 == 0 else col2
        with container:
            benefit_text = f"₹{details['benefit']:,}" if isinstance(details['benefit'], int) else details['benefit']
            
            html_content = f"""
            <div class='recommendation-box'>
                <h4>📋 {scheme}</h4>
                <p><strong>💰 Benefit:</strong> {benefit_text}</p>
                <p><strong>👥 Eligibility:</strong> {details['eligibility']}</p>
                <p><strong>📱 Apply:</strong> {details['application']}</p>
                <p><strong>☎️ Contact:</strong> {details['contact']}</p>
            </div>
            """
            st.markdown(html_content, unsafe_allow_html=True)
            
def create_crop_plan_diagram(region, query):
    """Create crop plan diagram with timeline based on query"""
    st.markdown("## 📅 **Crop Planning & Timeline**")
    
    query_lower = query.lower()
    crop = next((c for c in BASE_COSTS if c.lower() in query_lower), 'Rice')
    
    crop_plan_data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        crop: ['Prep', 'Plant', 'Grow', 'Grow', 'Grow', 'Harvest', 'Rest', 'Rest', 'Prep', 'Plant', 'Grow', 'Grow']
    }
    
    df_plan = pd.DataFrame(crop_plan_data)
    st.dataframe(df_plan, use_container_width=True, hide_index=True)

def create_contact_section(query):
    """Create contact directory relevant to the query"""
    st.markdown("## 📞 **Farmer Support Network**")
    st.markdown("*Relevant support services based on your query*")
    
    query_lower = query.lower()
    relevant_contacts = {
        service: details for service, details in CONTACT_DIRECTORY.items()
        if any(keyword in query_lower for keyword in [service.lower(), details['purpose'].lower()])
    } or CONTACT_DIRECTORY
    
    col1, col2 = st.columns(2)
    for i, (service, details) in enumerate(relevant_contacts.items()):
        container = col1 if i % 2 == 0 else col2
        with container:
            contact_info = details.get('number', details.get('website', 'N/A'))
            
            html_content = f"""
            <div class='recommendation-box'>
                <h4>{service}</h4>
                <p><strong>📱 Contact:</strong> {contact_info}</p>
                <p><strong>🎯 Purpose:</strong> {details['purpose']}</p>
            </div>
            """
            st.markdown(html_content, unsafe_allow_html=True)

def main():
    if 'selected_question' not in st.session_state:
        st.session_state.selected_question = ""

    st.markdown("""
    <div class='main-header'>
            <div style='font-size: 2.4rem; margin-top: 0.5rem; margin-bottom: 0.5rem; opacity: 0.9;'>
                 👩🏻‍🌾Nilam - Advanced Farming Assistant 
            </div>
        <p style='font-size: 16px; opacity: 0.9;'>Crop Recommendations • Financial Analysis • Government Schemes • Expert Support</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("### 🛠️ **Configuration Panel**")
    
    language = st.sidebar.selectbox(
        "🌍 Select Language / भाषा चुनें",
        ["English", "हिंदी (Hindi)", "தமிழ் (Tamil)", "తెలుగు (Telugu)", "ಕನ್ನಡ (Kannada)", "বাংলা (Bengali)"]
    )
    
    model = initialize_gemini()
    
    region = st.sidebar.selectbox(
        "📍 Your Region / आपका क्षेत्र",
        ["Punjab", "Maharashtra", "Tamil Nadu", "Karnataka", "Kerala", "Rajasthan", 
         "Gujarat", "Haryana", "Andhra Pradesh", "Uttar Pradesh", "Bihar", 
         "West Bengal", "Madhya Pradesh", "Odisha", "Assam", "Other"]
    )
    
    farm_size = st.sidebar.selectbox(
        "🏡 Farm Size / खेत का आकार",
        ["Small (< 2 acres)", "Medium (2-10 acres)", "Large (10-50 acres)", "Very Large (> 50 acres)"]
    )
    
    soil_type = st.sidebar.selectbox(
        "🌱 Soil Type / मिट्टी का प्रकार",
        ["Alluvial", "Black Cotton", "Red Soil", "Laterite", "Sandy", "Clay", "Loamy", "Mixed"]
    )
    
    irrigation = st.sidebar.selectbox(
        "💧 Irrigation / सिंचाई",
        ["Canal", "Borewell", "River", "Rain-fed", "Drip System", "Sprinkler", "Mixed"]
    )
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💬 Chat with AI Expert", "📊 Financial Analysis", 
        "🌾 Crop Intelligence", "📞 Contact Support", "🎯 Subsidy Schemes"
    ])
    
    with tab1:
        st.markdown("## 💬 **Chat with Agricultural Expert**")
        st.markdown("*Get instant, personalized farming advice powered by advanced AI*")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            user_question = st.text_area(
                "🗣️ **Ask your detailed farming question:**",
                value=st.session_state.selected_question,
                placeholder=f"Example: What are the best profitable crops for my {farm_size} {soil_type} soil farm in {region}?",
                height=120,
                help="Ask detailed questions about crops, costs, profits, schemes, or any farming topic",
                key="user_question_input"
            )
        
        with col2:
            st.markdown("#### 🔥 **Smart Quick Questions**")
            
            quick_questions = [
                f"💰 Profit analysis for {region} farming",
                f"🌾 Profitable crops for {soil_type} soil",
                f"🏛️ Subsidies for {farm_size} farms",
                f"📅 Crop calendar for {region}",
                f"💧 Irrigation methods for {soil_type} soil",
                "🌡️ Climate-smart farming techniques"
            ]
            
            for i, q in enumerate(quick_questions):
                if st.button(q, key=f"enhanced_quick_{i}", use_container_width=True):
                    st.session_state.selected_question = q
                    st.rerun()
            
            st.markdown("#### 🔥 **Trending Topics**")
            trending = ["Organic Certification", "Drone Technology", "Export Opportunities"]
            for trend in trending:
                st.info(f"🔥 {trend}")
        
        current_question = user_question if user_question else st.session_state.selected_question
        if st.session_state.selected_question and not user_question:
            st.session_state.selected_question = ""
        
        if st.button("🔍 **Get Comprehensive Analysis**", type="primary", use_container_width=True):
            if current_question and model:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                loading_messages = [
                    "🌾 Analyzing your query...",
                    "💰 Calculating costs...",
                    "📊 Checking relevant schemes...", 
                    "🎯 Preparing recommendations...",
                    "✅ Finalizing analysis..."
                ]
                
                for i, message in enumerate(loading_messages):
                    status_text.text(message)
                    progress_bar.progress((i + 1) * 20)
                    time.sleep(0.5)
                
                try:
                    lang_mapping = {
                        "English": "English",
                        "हिंदी (Hindi)": "Hindi",
                        "தமிழ் (Tamil)": "Tamil", 
                        "తెలుగు (Telugu)": "Telugu",
                        "ಕನ್ನಡ (Kannada)": "Kannada",
                        "বাংলা (Bengali)": "Bengali"
                    }
                    
                    selected_language = lang_mapping.get(language, "English")
                    
                    # Enhanced prompt for more innovative and insightful responses
                    prompt = f"""
                    You are Dr. Agricultural Expert, India's leading farming consultant with 25+ years experience.
                    Provide a concise, actionable response with deep insights, innovative recommendations, and data-driven analysis tailored to this farmer's query in {selected_language} language.
                    
                    FARMER PROFILE:
                    - Location: {region}, India
                    - Farm Size: {farm_size}
                    - Soil Type: {soil_type}
                    - Irrigation: {irrigation}
                    - Language: {selected_language}
                    
                    QUERY: {current_question}
                    
                    RESPONSE GUIDELINES:
                    - Answer the specific query with innovative, practical solutions
                    - Include cutting-edge farming techniques and technologies where relevant
                    - Provide data-driven insights with specific numbers, costs, and yields
                    - Use markdown tables for structured data (e.g., | Item | Quantity | Rate (₹) | Total Cost (₹) | Notes |)
                    - Use bullet points (•) for actionable recommendations
                    - Include market trends, government schemes, and risk mitigation strategies
                    - Use clear section headers with ## for different aspects
                    - Emphasize sustainable and profitable farming practices
                    - Provide forward-thinking advice considering climate change and market dynamics
                    - Keep the response concise yet comprehensive
                    - Focus on actionable insights that can increase productivity and profitability
                    - Respond in {selected_language} where possible
                    """
                    
                    response = model.generate_content(prompt)
                    progress_bar.progress(100)
                    status_text.text("✅ Analysis Complete!")
                    time.sleep(0.5)
                    progress_bar.empty()
                    status_text.empty()
                    
                    parse_gemini_response(response.text, current_question, region, farm_size, language)
                    
                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Error getting response: {str(e)}")
            elif not current_question:
                st.warning("⚠️ Please enter your farming question")
            else:
                st.warning("⚠️ Please configure Gemini API key in the sidebar")
    
    with tab2:
        st.markdown("## 📊 **Advanced Financial Analysis Tools**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💰 **Investment Calculator**")
            crop_type = st.selectbox("Select Crop for Analysis", list(BASE_COSTS.keys()))
            area = st.number_input("Farm Area (acres)", min_value=0.1, max_value=1000.0, value=1.0, step=0.1)
            
            if st.button("📊 **Calculate Investment**", type="primary"):
                create_financial_analysis(f"Investment analysis for {crop_type}", region, farm_size)
        
        with col2:
            st.markdown("### 📈 **ROI Calculator**")
            if 'crop_type' in locals():
                yield_data = YIELD_DATA.get(crop_type, {"yield_kg": 2000, "price_kg": 20})
                expected_yield = st.number_input("🌾 Expected Yield (kg/acre)", min_value=100, value=yield_data["yield_kg"])
                market_price = st.number_input("💰 Market Price (₹/kg)", min_value=1, value=yield_data["price_kg"])
                
                if st.button("📈 **Calculate ROI**", type="primary"):
                    total_revenue = expected_yield * market_price * area
                    total_cost = BASE_COSTS.get(crop_type, 30000) * area
                    profit = total_revenue - total_cost
                    roi_percent = (profit / total_cost) * 100 if total_cost > 0 else 0
                    
                    fig_roi = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=roi_percent,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': f"ROI for {crop_type}"},
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "#7a8471"},
                            'steps': [
                                {'range': [0, 20], 'color': "#f5f1e8"},
                                {'range': [20, 40], 'color': "#ede4d3"},
                                {'range': [40, 100], 'color': "#8b7355"}
                            ]
                        }
                    ))
                    fig_roi.update_layout(
                        height=300,
                        font=dict(color='#2d3436'),
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_roi, use_container_width=True)
    
    with tab3:
        st.markdown("## 🌾 **Crop Intelligence Dashboard**")
        create_crop_recommendation_analysis(region, "", "tab3")
    
    with tab4:
        create_contact_section("")
    
    with tab5:
        create_government_schemes_analysis("")

if __name__ == "__main__":
    main()
