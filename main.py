import streamlit as st
import sys
import os

# Page configuration
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="Nilam - Your Agricultural Assistant",
    page_icon="🌱"
)

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


    .main-header {
        background: linear-gradient(135deg, var(--earth-brown) 0%, var(--cream-dark) 50%, var(--earth-green) 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: black;  /* Changed to black */
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        font-weight: 700;
        border: 1px solid rgba(255,255,255,0.2);
        font-size: 8rem;
        text-shadow: none;
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
        background: linear-gradient(135deg, var(--earth-green) 0%, var(--earth-brown) 100%) !important;
        color: white !important;
        font-weight: bold !important;
        padding: 1.2rem !important;
        text-align: center !important;
        font-size: 1rem !important;
        border-bottom: 3px solid var(--earth-brown) !important;
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
        background: linear-gradient(135deg, var(--earth-green) 0%, var(--earth-brown) 100%) !important;
        color: white !important;
        border: 2px solid var(--earth-green) !important;
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
    
    /* Increase h1 font size */
    h1 {
        font-size: 2.5rem !important;
        line-height: 1.2 !important;
    }
    
    /* Large h1 header styling */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        background: linear-gradient(135deg, var(--earth-brown) 0%, var(--cream-dark) 50%, var(--earth-green) 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        padding: 1rem 0 !important;
    }
    
    p, li, span, div { 
        color: var(--text-primary) !important; 
        font-size: 16px;
    }
    
    /* Main app specific styles */
    .section-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
            
            /* Sidebar Selectbox label */
div[data-testid="stSidebar"] label {
    color: white !important;
    font-weight: 600 !important;
}

/* Selected value inside the selectbox */
div[data-testid="stSidebar"] .stSelectbox div[role="combobox"] input {
    color: white !important;
    font-weight: 600 !important;
}

/* Dropdown arrow icon */
div[data-testid="stSidebar"] .stSelectbox svg {
    fill: white !important;
}

/* Dropdown option text */
div[data-testid="stSidebar"] .stSelectbox div[role="listbox"] div {
    color: white !important;
}

/* Comprehensive dropdown list styling */
[data-testid="stSidebar"] .stSelectbox div[role="listbox"] *,
[data-testid="stSidebar"] .stSelectbox div[role="listbox"] div,
[data-testid="stSidebar"] .stSelectbox div[role="listbox"] span,
[data-testid="stSidebar"] .stSelectbox div[role="listbox"] p,
[data-testid="stSidebar"] .stSelectbox div[role="listbox"] li,
[data-testid="stSidebar"] .stSelectbox div[role="listbox"] ul,
[data-testid="stSidebar"] .stSelectbox div[role="listbox"] ol {
    color: white !important;
    background-color: var(--earth-green) !important;
}

/* Dropdown popup styling */
[data-testid="stSidebar"] div[data-baseweb="popover"] *,
[data-testid="stSidebar"] div[data-baseweb="popover"] div,
[data-testid="stSidebar"] div[data-baseweb="popover"] span,
[data-testid="stSidebar"] div[data-baseweb="popover"] p,
[data-testid="stSidebar"] div[data-baseweb="popover"] li,
[data-testid="stSidebar"] div[data-baseweb="popover"] ul,
[data-testid="stSidebar"] div[data-baseweb="popover"] ol {
    color: white !important;
    background-color: var(--earth-green) !important;
}

/* Force white text for all dropdown elements */
[data-testid="stSidebar"] .stSelectbox *,
[data-testid="stSidebar"] .stSelectbox div *,
[data-testid="stSidebar"] .stSelectbox div div *,
[data-testid="stSidebar"] .stSelectbox div div div * {
    color: white !important;
}

/* Ultra comprehensive dropdown styling - force white text */
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stSelectbox *,
[data-testid="stSidebar"] .stSelectbox > div,
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stSelectbox > div > div > div,
[data-testid="stSidebar"] .stSelectbox span,
[data-testid="stSidebar"] .stSelectbox div span,
[data-testid="stSidebar"] .stSelectbox div div span,
[data-testid="stSidebar"] .stSelectbox div div div span,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSelectbox div label,
[data-testid="stSidebar"] .stSelectbox div div label,
[data-testid="stSidebar"] .stSelectbox div div div label,
[data-testid="stSidebar"] .stSelectbox p,
[data-testid="stSidebar"] .stSelectbox div p,
[data-testid="stSidebar"] .stSelectbox div div p,
[data-testid="stSidebar"] .stSelectbox div div div p,
[data-testid="stSidebar"] .stSelectbox strong,
[data-testid="stSidebar"] .stSelectbox div strong,
[data-testid="stSidebar"] .stSelectbox div div strong,
[data-testid="stSidebar"] .stSelectbox div div div strong,
[data-testid="stSidebar"] .stSelectbox em,
[data-testid="stSidebar"] .stSelectbox div em,
[data-testid="stSidebar"] .stSelectbox div div em,
[data-testid="stSidebar"] .stSelectbox div div div em,
[data-testid="stSidebar"] .stSelectbox b,
[data-testid="stSidebar"] .stSelectbox div b,
[data-testid="stSidebar"] .stSelectbox div div b,
[data-testid="stSidebar"] .stSelectbox div div div b,
[data-testid="stSidebar"] .stSelectbox i,
[data-testid="stSidebar"] .stSelectbox div i,
[data-testid="stSidebar"] .stSelectbox div div i,
[data-testid="stSidebar"] .stSelectbox div div div i {
    color: white !important;
}

/* Force white text for all possible dropdown selectors */
[data-testid="stSidebar"] div[data-baseweb="select"] *,
[data-testid="stSidebar"] div[data-baseweb="select"] span,
[data-testid="stSidebar"] div[data-baseweb="select"] div,
[data-testid="stSidebar"] div[data-baseweb="select"] div span,
[data-testid="stSidebar"] div[data-baseweb="select"] div div,
[data-testid="stSidebar"] div[data-baseweb="select"] div div span,
[data-testid="stSidebar"] div[data-baseweb="select"] div div div,
[data-testid="stSidebar"] div[data-baseweb="select"] div div div span,
[data-testid="stSidebar"] div[data-baseweb="select"] label,
[data-testid="stSidebar"] div[data-baseweb="select"] div label,
[data-testid="stSidebar"] div[data-baseweb="select"] div div label,
[data-testid="stSidebar"] div[data-baseweb="select"] div div div label,
[data-testid="stSidebar"] div[data-baseweb="select"] p,
[data-testid="stSidebar"] div[data-baseweb="select"] div p,
[data-testid="stSidebar"] div[data-baseweb="select"] div div p,
[data-testid="stSidebar"] div[data-baseweb="select"] div div div p {
    color: white !important;
}

/* Force white text for dropdown options specifically */
[data-testid="stSidebar"] .stSelectbox option,
[data-testid="stSidebar"] .stSelectbox select option,
[data-testid="stSidebar"] div[data-baseweb="select"] option,
[data-testid="stSidebar"] div[data-baseweb="select"] select option,
[data-testid="stSidebar"] [role="option"],
[data-testid="stSidebar"] [role="option"] *,
[data-testid="stSidebar"] .stSelectbox [role="option"],
[data-testid="stSidebar"] .stSelectbox [role="option"] *,
[data-testid="stSidebar"] div[data-baseweb="select"] [role="option"],
[data-testid="stSidebar"] div[data-baseweb="select"] [role="option"] * {
    color: white !important;
    background-color: var(--earth-green) !important;
}

/* Force white text for all text elements in sidebar */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Make selectbox labels black - Ultra comprehensive */
.stSelectbox label,
div[data-baseweb="select"] label,
[data-testid="stSelectbox"] label {
    color: black !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
}

/* Force black color for all possible label selectors */
label,
.stSelectbox label,
div[data-baseweb="select"] label,
[data-testid="stSelectbox"] label,
.stSelectbox div label,
div[data-baseweb="select"] div label,
[data-testid="stSelectbox"] div label,
.stSelectbox div div label,
div[data-baseweb="select"] div div label,
[data-testid="stSelectbox"] div div label,
.stSelectbox div div div label,
div[data-baseweb="select"] div div div label,
[data-testid="stSelectbox"] div div div label {
    color: black !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    text-shadow: none !important;
    opacity: 1 !important;
}

/* Ultra specific targeting for selectbox labels */
.stSelectbox > div > label,
div[data-baseweb="select"] > div > label,
[data-testid="stSelectbox"] > div > label,
.stSelectbox > div > div > label,
div[data-baseweb="select"] > div > div > label,
[data-testid="stSelectbox"] > div > div > label {
    color: black !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    text-shadow: none !important;
    opacity: 1 !important;
}

/* Force black color for all label elements */
* label {
    color: black !important;
    font-weight: 600 !important;
    text-shadow: none !important;
    opacity: 1 !important;
}

/* Force white text for all selectbox elements in main content */
.stSelectbox *,
.stSelectbox label,
.stSelectbox span,
.stSelectbox div,
.stSelectbox div span,
.stSelectbox div div,
.stSelectbox div div span,
.stSelectbox div div div,
.stSelectbox div div div span,
.stSelectbox option,
.stSelectbox select,
.stSelectbox select option {
    color: white !important;
}

/* Force white text for all baseweb select elements */
div[data-baseweb="select"] *,
div[data-baseweb="select"] label,
div[data-baseweb="select"] span,
div[data-baseweb="select"] div,
div[data-baseweb="select"] div span,
div[data-baseweb="select"] div div,
div[data-baseweb="select"] div div span,
div[data-baseweb="select"] div div div,
div[data-baseweb="select"] div div div span,
div[data-baseweb="select"] option,
div[data-baseweb="select"] select,
div[data-baseweb="select"] select option {
    color: white !important;
}

/* Force white text for all testid selectbox elements */
[data-testid="stSelectbox"] *,
[data-testid="stSelectbox"] label,
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] div,
[data-testid="stSelectbox"] div span,
[data-testid="stSelectbox"] div div,
[data-testid="stSelectbox"] div div span,
[data-testid="stSelectbox"] div div div,
[data-testid="stSelectbox"] div div div span,
[data-testid="stSelectbox"] option,
[data-testid="stSelectbox"] select,
[data-testid="stSelectbox"] select option {
    color: white !important;
}

/* Force white text for dropdown popup content */
div[data-baseweb="popover"] *,
div[data-baseweb="popover"] label,
div[data-baseweb="popover"] span,
div[data-baseweb="popover"] div,
div[data-baseweb="popover"] div span,
div[data-baseweb="popover"] div div,
div[data-baseweb="popover"] div div span,
div[data-baseweb="popover"] div div div,
div[data-baseweb="popover"] div div div span,
div[data-baseweb="popover"] option,
div[data-baseweb="popover"] select,
div[data-baseweb="popover"] select option {
    color: white !important;
    background-color: var(--earth-green) !important;
}

/* Force white text for role option elements */
[role="option"] *,
[role="option"] label,
[role="option"] span,
[role="option"] div,
[role="option"] div span,
[role="option"] div div,
[role="option"] div div span,
[role="option"] div div div,
[role="option"] div div div span {
    color: white !important;
    background-color: var(--earth-green) !important;
}

/* Ultra comprehensive selectbox styling for main content */
.stSelectbox,
.stSelectbox *,
.stSelectbox > div,
.stSelectbox > div > div,
.stSelectbox > div > div > div,
.stSelectbox span,
.stSelectbox div span,
.stSelectbox div div span,
.stSelectbox div div div span,
.stSelectbox p,
.stSelectbox div p,
.stSelectbox div div p,
.stSelectbox div div div p,
.stSelectbox strong,
.stSelectbox div strong,
.stSelectbox div div strong,
.stSelectbox div div div strong,
.stSelectbox em,
.stSelectbox div em,
.stSelectbox div div em,
.stSelectbox div div div em,
.stSelectbox b,
.stSelectbox div b,
.stSelectbox div div b,
.stSelectbox div div div b,
.stSelectbox i,
.stSelectbox div i,
.stSelectbox div div i,
.stSelectbox div div div i {
    color: white !important;
}



/* Force white text for all sidebar titles and text */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] h5,
[data-testid="stSidebar"] h6,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] em,
[data-testid="stSidebar"] b,
[data-testid="stSidebar"] i,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] ul,
[data-testid="stSidebar"] ol {
    color: white !important;
}

/* Remove dark background from chat messages - Comprehensive override */
div[data-testid="stChatMessage"],
div[data-testid="stChatMessage"] > div,
div[data-testid="stChatMessage"] > div > div,
.stChatMessage,
.stChatMessage > div {
    background: transparent !important;
    background-color: transparent !important;
}

/* Assistant chat message - light background */
div[data-testid="stChatMessage"][data-message="assistant"],
div[data-testid="stChatMessage"][data-message="assistant"] > div,
div[data-testid="stChatMessage"][data-message="assistant"] > div > div,
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(135deg, var(--cream-light) 0%, var(--cream-medium) 100%) !important;
    background-color: var(--cream-light) !important;
    border: 1px solid var(--earth-green) !important;
    border-radius: 15px !important;
    padding: 1rem !important;
    margin: 0.5rem 0 !important;
}

/* User chat message - light blue background */
div[data-testid="stChatMessage"][data-message="user"],
div[data-testid="stChatMessage"][data-message="user"] > div,
div[data-testid="stChatMessage"][data-message="user"] > div > div,
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%) !important;
    background-color: #e3f2fd !important;
    border: 1px solid #2196f3 !important;
    border-radius: 15px !important;
    padding: 1rem !important;
    margin: 0.5rem 0 !important;
}

/* Remove any dark backgrounds from chat containers */
div[data-testid="stChatMessageContainer"],
div[data-testid="stChatMessageContainer"] > div {
    background: transparent !important;
    background-color: transparent !important;
}

/* Match app theme background behind st.chat_input - ULTRA AGGRESSIVE */
div[data-testid="stChatInputContainer"],
div[data-testid="stChatInputContainer"] > div,
div[data-testid="stChatInputContainer"] > div > div,
div[data-testid="stChatInputContainer"] > div > div > div,
div[data-testid="stChatInputContainer"] > div > div > div > div,
div:has(div[data-testid="stChatInputContainer"]),
div:has(div[data-testid="stChatInputContainer"]) > div,
div:has(div[data-testid="stChatInputContainer"]) > div > div,
div:has(div[data-testid="stChatInputContainer"]) > div > div > div,
div:has(div[data-testid="stChatInputContainer"]) > div > div > div > div,
/* Target all parent elements up the DOM tree */
div:has(div[data-testid="stChatInputContainer"]) > *,
div:has(div[data-testid="stChatInputContainer"]) > * > *,
/* Target any element with dark background containing chat input */
div[style*="background"][style*="#000"]:has(div[data-testid="stChatInputContainer"]),
div[style*="background"][style*="#2d3436"]:has(div[data-testid="stChatInputContainer"]),
div[style*="background"][style*="black"]:has(div[data-testid="stChatInputContainer"]),
div[style*="background-color"][style*="#000"]:has(div[data-testid="stChatInputContainer"]),
div[style*="background-color"][style*="#2d3436"]:has(div[data-testid="stChatInputContainer"]),
div[style*="background-color"][style*="black"]:has(div[data-testid="stChatInputContainer"]),
div[style*="background"][style*="rgb(45, 52, 54)"]:has(div[data-testid="stChatInputContainer"]),
div[style*="background"][style*="rgb(0, 0, 0)"]:has(div[data-testid="stChatInputContainer"]),
/* Target section and main containers */
section:has(div[data-testid="stChatInputContainer"]),
main:has(div[data-testid="stChatInputContainer"]),
[class*="block-container"]:has(div[data-testid="stChatInputContainer"]),
[class*="element-container"]:has(div[data-testid="stChatInputContainer"]),
[class*="stMain"]:has(div[data-testid="stChatInputContainer"]),
[data-testid="stAppViewContainer"]:has(div[data-testid="stChatInputContainer"]),
[data-testid="stAppViewContainer"] > div:has(div[data-testid="stChatInputContainer"]),
[data-testid="stAppViewContainer"] > div:has(div[data-testid="stChatInputContainer"]) > div,
[data-testid="stAppViewContainer"] > div:has(div[data-testid="stChatInputContainer"]) > div > div,
[data-testid="stAppViewContainer"] > div:has(div[data-testid="stChatInputContainer"]) > div > div > div {
    background: linear-gradient(135deg, var(--cream-light) 0%, var(--cream-medium) 100%) !important;
    background-color: var(--cream-light) !important;
    background-image: none !important;
}

/* Override inline styles - force app theme background */
div[data-testid="stChatInputContainer"][style],
div[data-testid="stChatInputContainer"][style] > div,
div:has(div[data-testid="stChatInputContainer"])[style] {
    background: linear-gradient(135deg, var(--cream-light) 0%, var(--cream-medium) 100%) !important;
    background-color: var(--cream-light) !important;
}

/* Target the bottom section where Streamlit places chat input - match app theme */
[data-testid="stAppViewContainer"] > div:last-child:has(div[data-testid="stChatInputContainer"]),
[data-testid="stAppViewContainer"] > div:last-child:has(div[data-testid="stChatInputContainer"]) > div,
[data-testid="stAppViewContainer"] > div:last-child:has(div[data-testid="stChatInputContainer"]) > div > div,
[data-testid="stAppViewContainer"] > div:last-child:has(div[data-testid="stChatInputContainer"]) > div > div > div,
[data-testid="stAppViewContainer"] > div:last-child:has(div[data-testid="stChatInputContainer"]) > div > div > div > div,
.stApp > div:last-child:has(div[data-testid="stChatInputContainer"]),
.stApp > div:last-child:has(div[data-testid="stChatInputContainer"]) > div,
.stApp > div:last-child:has(div[data-testid="stChatInputContainer"]) > div > div,
.stApp > div:last-child:has(div[data-testid="stChatInputContainer"]) > div > div > div,
/* Target block containers at bottom that contain chat input */
[class*="block-container"]:last-child:has(div[data-testid="stChatInputContainer"]),
[class*="block-container"]:last-child:has(div[data-testid="stChatInputContainer"]) > div,
[class*="block-container"]:last-child:has(div[data-testid="stChatInputContainer"]) > div > div,
[class*="element-container"]:last-child:has(div[data-testid="stChatInputContainer"]),
[class*="element-container"]:last-child:has(div[data-testid="stChatInputContainer"]) > div,
[class*="element-container"]:last-child:has(div[data-testid="stChatInputContainer"]) > div > div {
    background: linear-gradient(135deg, var(--cream-light) 0%, var(--cream-medium) 100%) !important;
    background-color: var(--cream-light) !important;
    background-image: none !important;
}

/* Chat input field itself - white background */
div[data-testid="stChatInputContainer"] input,
div[data-testid="stChatInputContainer"] textarea {
    background: white !important;
    background-color: white !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--earth-green) !important;
    border-radius: 15px !important;
}

/* MAXIMUM SPECIFICITY - Force app theme background on chat input container and ALL parents */
html body div[data-testid="stAppViewContainer"] div:has(div[data-testid="stChatInputContainer"]),
html body div[data-testid="stAppViewContainer"] div:has(div[data-testid="stChatInputContainer"]) > div,
html body div[data-testid="stAppViewContainer"] div:has(div[data-testid="stChatInputContainer"]) > div > div,
html body div[data-testid="stAppViewContainer"] div:has(div[data-testid="stChatInputContainer"]) > div > div > div,
html body div[data-testid="stAppViewContainer"] div:has(div[data-testid="stChatInputContainer"]) > div > div > div > div,
html body div[data-testid="stChatInputContainer"],
html body div[data-testid="stChatInputContainer"] > div,
html body div[data-testid="stChatInputContainer"] > div > div,
html body div[data-testid="stChatInputContainer"] > div > div > div {
    background: linear-gradient(135deg, var(--cream-light) 0%, var(--cream-medium) 100%) !important;
    background-color: var(--cream-light) !important;
    background-image: none !important;
}


/* Override any Streamlit dark theme for chat */
.stChatMessage,
[class*="chatMessage"],
[class*="ChatMessage"] {
    background: transparent !important;
    background-color: transparent !important;
}

/* Ultra comprehensive sidebar text styling */
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] * *,
[data-testid="stSidebar"] * * * {
    color: white !important;
}

/* Specific sidebar title styling */
[data-testid="stSidebar"] .css-1d391kg,
[data-testid="stSidebar"] .css-1lcbmhc,
[data-testid="stSidebar"] .css-1v0mbdj,
[data-testid="stSidebar"] [data-testid="stSidebar"] {
    color: white !important;
}

            
</style>
<script>
// ULTRA AGGRESSIVE: Remove black background behind chat input
function removeChatInputBackground() {
    const chatInput = document.querySelector('[data-testid="stChatInputContainer"]');
    if (!chatInput) return;
    
    // Set app theme background on chat input itself (but keep input field white)
    chatInput.style.background = 'linear-gradient(135deg, #fefcf8 0%, #f5f1e8 100%)';
    chatInput.style.backgroundColor = '#fefcf8';
    
    // Remove from all children (input field should stay white)
    chatInput.querySelectorAll('*').forEach(el => {
        // Don't change input/textarea backgrounds - keep them white
        if (el.tagName !== 'INPUT' && el.tagName !== 'TEXTAREA') {
            el.style.background = 'linear-gradient(135deg, #fefcf8 0%, #f5f1e8 100%)';
            el.style.backgroundColor = '#fefcf8';
        }
    });
    
    // Remove from ALL parent elements up to body
    let parent = chatInput.parentElement;
    while (parent && parent !== document.body && parent !== document.documentElement) {
        // Force set app theme background
        parent.style.setProperty('background', 'linear-gradient(135deg, #fefcf8 0%, #f5f1e8 100%)', 'important');
        parent.style.setProperty('background-color', '#fefcf8', 'important');
        parent.style.setProperty('background-image', 'none', 'important');
        
        // Check computed style and override if dark
        const computed = window.getComputedStyle(parent);
        const bgColor = computed.backgroundColor;
        if (bgColor && (
            bgColor.includes('rgb(45, 52, 54)') || 
            bgColor.includes('rgb(0, 0, 0)') || 
            bgColor === 'rgb(0, 0, 0)' || 
            bgColor === 'rgb(45, 52, 54)' ||
            bgColor.includes('#000') ||
            bgColor.includes('#2d3436')
        )) {
            parent.style.setProperty('background', 'linear-gradient(135deg, #fefcf8 0%, #f5f1e8 100%)', 'important');
            parent.style.setProperty('background-color', '#fefcf8', 'important');
        }
        
        parent = parent.parentElement;
    }
    
    // Also find and fix the last block container (where Streamlit places chat input)
    const appContainer = document.querySelector('[data-testid="stAppViewContainer"]');
    if (appContainer) {
        const mainContent = Array.from(appContainer.children).find(child => 
            child.getAttribute('data-testid') !== 'stSidebar' && 
            child.contains(chatInput)
        );
        
        if (mainContent) {
            // Get the last block container
            const blockContainers = mainContent.querySelectorAll('[class*="block-container"]');
            if (blockContainers.length > 0) {
                const lastBlock = blockContainers[blockContainers.length - 1];
                if (lastBlock.contains(chatInput)) {
                    lastBlock.style.setProperty('background', 'linear-gradient(135deg, #fefcf8 0%, #f5f1e8 100%)', 'important');
                    lastBlock.style.setProperty('background-color', '#fefcf8', 'important');
                    
                    // Fix all parents of last block
                    let blockParent = lastBlock.parentElement;
                    while (blockParent && blockParent !== document.body) {
                        blockParent.style.setProperty('background', 'linear-gradient(135deg, #fefcf8 0%, #f5f1e8 100%)', 'important');
                        blockParent.style.setProperty('background-color', '#fefcf8', 'important');
                        blockParent = blockParent.parentElement;
                    }
                }
            }
        }
    }
    
    // Find all divs containing chat input and remove dark backgrounds
    document.querySelectorAll('div').forEach(div => {
        if (div.contains(chatInput) && div !== chatInput) {
            const bg = window.getComputedStyle(div).backgroundColor;
            if (bg && (
                bg.includes('rgb(45, 52, 54)') || 
                bg.includes('rgb(0, 0, 0)') || 
                bg === 'rgb(0, 0, 0)' || 
                bg === 'rgb(45, 52, 54)' ||
                bg.includes('#000') ||
                bg.includes('#2d3436')
            )) {
                div.style.setProperty('background', 'linear-gradient(135deg, #fefcf8 0%, #f5f1e8 100%)', 'important');
                div.style.setProperty('background-color', '#fefcf8', 'important');
            }
        }
    });
}

// Run multiple times to ensure it works
function forceRemove() {
    removeChatInputBackground();
    setTimeout(removeChatInputBackground, 100);
    setTimeout(removeChatInputBackground, 500);
    setTimeout(removeChatInputBackground, 1000);
    setTimeout(removeChatInputBackground, 2000);
}

// Run immediately
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', forceRemove);
} else {
    forceRemove();
}

// Use MutationObserver
const observer = new MutationObserver(() => {
    removeChatInputBackground();
});

observer.observe(document.body, { 
    childList: true, 
    subtree: true,
    attributes: true,
    attributeFilter: ['style', 'class']
});

// Run periodically - very frequently
setInterval(removeChatInputBackground, 100);

// Inject a style element to override everything with app theme
const style = document.createElement('style');
style.textContent = `
    div[data-testid="stChatInputContainer"],
    div[data-testid="stChatInputContainer"] > *:not(input):not(textarea),
    div:has(div[data-testid="stChatInputContainer"]),
    div:has(div[data-testid="stChatInputContainer"]) > *,
    div:has(div[data-testid="stChatInputContainer"]) > * > *,
    div:has(div[data-testid="stChatInputContainer"]) > * > * > * {
        background: linear-gradient(135deg, #fefcf8 0%, #f5f1e8 100%) !important;
        background-color: #fefcf8 !important;
        background-image: none !important;
    }
`;
document.head.appendChild(style);

// Also add inline style directly to chat input when found
const addInlineStyle = () => {
    const chatInput = document.querySelector('[data-testid="stChatInputContainer"]');
    if (chatInput) {
        chatInput.setAttribute('style', 'background: linear-gradient(135deg, #fefcf8 0%, #f5f1e8 100%) !important; background-color: #fefcf8 !important;');
    }
};

// Run addInlineStyle frequently
setInterval(addInlineStyle, 100);
</script>
""", unsafe_allow_html=True)

def run_nilamchat():
    """Run nilamchat functionality directly"""
    try:
        # Add the current directory to Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)
        
        # Import nilamchat module
        import nilamchat
        
        # Run the nilamchat main function
        if hasattr(nilamchat, 'main'):
            nilamchat.main()
        else:
            st.error("No main function found in nilamchat.py")
            
    except Exception as e:
        st.error(f"Error loading Nilam Chat: {str(e)}")
        # st.info("Please ensure nilamchat.py is in the same directory.")

def run_leafine():
    """Run leafine functionality"""
    try:
        # Add the current directory to Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)
        
        # Import leafine module
        import leafine
        
        # Run the leafine main function
        if hasattr(leafine, 'main'):
            leafine.main()
        else:
            st.error("No main function found in leafine.py")
            
    except Exception as e:
        st.error(f"Error loading Leafine: {str(e)}")
        st.info("Please ensure leafine.py is in the same directory.")


def run_agent_system():
    """Run multi-agent system interface with enhanced UI"""
    try:
        # Import agent integration
        import agent_integration
        
        st.markdown("""
            <div class='main-header'>
                    <div style='font-size: 2.4rem; margin-top: 0.5rem; margin-bottom: 0.5rem; opacity: 0.9;'>
                        🤖 Multi-Agent System
                    </div>
                <p style='font-size: 16px; opacity: 0.9;'>MCP Tools • Agent Orchestration • Advanced AI • Real-time Processing</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Initialize agent system
        agent_system = agent_integration.initialize_agent_system()
        
        # Sidebar configuration
        st.sidebar.markdown("### 🛠️ **Agent Configuration**")
        
        # Pattern selection
        pattern_option = st.sidebar.selectbox(
            "🔄 Agent Pattern:",
            ["Sequential", "Parallel", "Loop"],
            help="Sequential: Agents run one after another\nParallel: Agents run simultaneously\nLoop: Agents run until condition met",
            index=0
        )
        
        from agents import AgentPattern
        pattern_map = {
            "Sequential": AgentPattern.SEQUENTIAL,
            "Parallel": AgentPattern.PARALLEL,
            "Loop": AgentPattern.LOOP
        }
        selected_pattern = pattern_map[pattern_option]
        
        # Display available tools
        st.sidebar.markdown("### 🔧 **Available Tools**")
        
        # MCP Tools
        st.sidebar.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0;'>
            <strong style='color: white;'>🔌 MCP Tools</strong>
            <ul style='color: white; margin: 0.5rem 0; padding-left: 1.2rem; font-size: 0.9rem;'>
                <li>Weather Data Tool</li>
                <li>Crop Recommendation Tool</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # OpenAPI Tools
        st.sidebar.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0;'>
            <strong style='color: white;'>🌐 OpenAPI Tools</strong>
            <ul style='color: white; margin: 0.5rem 0; padding-left: 1.2rem; font-size: 0.9rem;'>
                <li>Weather API</li>
                <li>Crop Data API</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Built-in Tools
        st.sidebar.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0;'>
            <strong style='color: white;'>⚙️ Built-in Tools</strong>
            <ul style='color: white; margin: 0.5rem 0; padding-left: 1.2rem; font-size: 0.9rem;'>
                <li>Google Search</li>
                <li>Calculator</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Display agent status
        agent_integration.display_agent_status(agent_system)
        
        # Main chat interface
        st.markdown("### 💬 Chat with Multi-Agent System")
        st.markdown("""
        <div style='background: linear-gradient(135deg, var(--cream-light) 0%, var(--cream-medium) 100%);
                    padding: 1.5rem; border-radius: 15px; border: 2px solid var(--earth-green);
                    margin: 1rem 0; box-shadow: 0 4px 15px rgba(122, 132, 113, 0.15);'>
            <p style='margin: 0; color: var(--text-primary); font-size: 0.95rem;'>
                <strong>💡 How it works:</strong> Your query is processed by specialized agents using 
                <strong style='color: #667eea;'>MCP tools</strong>, 
                <strong style='color: #f5576c;'>OpenAPI tools</strong>, and 
                <strong style='color: #4facfe;'>built-in tools</strong> to provide comprehensive agricultural assistance.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Chat interface
        if "agent_messages" not in st.session_state:
            st.session_state.agent_messages = []
        
        # Display chat history with enhanced styling
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.agent_messages:
                with st.chat_message(msg["role"]):
                    if msg["role"] == "assistant":
                        content = msg["content"]
                        # Format based on content type
                        if "🔍 Search Results" in content or "Search Results" in content:
                            # Format search results
                            st.markdown("### 🔍 Search Results")
                            # Extract and display search results nicely
                            st.markdown(content, unsafe_allow_html=True)
                        elif "🌾" in content or "Crop Recommendation" in content:
                            # Format crop recommendations
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
                                        padding: 1.5rem; border-radius: 15px; border-left: 5px solid #4caf50;
                                        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);'>
                                {content}
                            </div>
                            """, unsafe_allow_html=True)
                        elif "tool" in content.lower() or "mcp" in content.lower():
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                                        padding: 1rem; border-radius: 10px; border-left: 4px solid #2196f3;
                                        margin: 0.5rem 0;'>
                                {content}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            # Regular response
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, var(--cream-light) 0%, var(--cream-medium) 100%);
                                        padding: 1rem; border-radius: 10px; border: 1px solid var(--earth-green);
                                        margin: 0.5rem 0;'>
                                {content}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.write(msg["content"])
        
        # User input
        user_input = st.chat_input("Ask about crops, diseases, weather, or agricultural advice...")
        
        if user_input:
            # Add user message
            st.session_state.agent_messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)
            
            # Process with agents
            with st.chat_message("assistant"):
                with st.spinner("🤖 Processing with multi-agent system using MCP tools..."):
                    response = agent_integration.process_with_agents(
                        user_input,
                        agent_system,
                        pattern=selected_pattern
                    )
                    
                    # Enhanced response display with proper formatting
                    # Check if response contains structured data
                    if "Search Results" in response or "🔍" in response:
                        # Format search results
                        st.markdown("### 🔍 Search Results")
                        st.markdown(response, unsafe_allow_html=True)
                    elif "🌾" in response or "Crop Recommendation" in response:
                        # Format crop recommendations
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
                                    padding: 1.5rem; border-radius: 15px; border-left: 5px solid #4caf50;
                                    box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);'>
                            {response}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Regular response
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, var(--cream-light) 0%, var(--cream-medium) 100%);
                                    padding: 1.5rem; border-radius: 15px; border: 2px solid var(--earth-green);
                                    box-shadow: 0 4px 15px rgba(122, 132, 113, 0.15);'>
                            {response}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Show tool usage indicator
                    tool_used = False
                    if any(keyword in user_input.lower() for keyword in ['weather', 'temperature', 'rain', 'climate']):
                        tool_used = True
                        st.info("🔌 **MCP Weather Tool** was used to fetch real-time weather data")
                    if any(keyword in user_input.lower() for keyword in ['crop', 'recommend', 'plant', 'grow']):
                        tool_used = True
                        st.info("🔌 **MCP Crop Recommendation Tool** was used for crop analysis")
                    if any(keyword in user_input.lower() for keyword in ['search', 'find', 'lookup']):
                        tool_used = True
                        st.info("⚙️ **Google Search Tool** was used to find information")
                    
                    st.session_state.agent_messages.append({"role": "assistant", "content": response})
        
        # Additional tabs
        tab1, tab2, tab3 = st.tabs(["📊 Observability", "🌐 A2A Network", "📖 Documentation"])
        
        with tab1:
            agent_integration.display_observability_dashboard(agent_system)
        
        with tab2:
            agent_integration.display_a2a_network(agent_system)
        
        with tab3:
            st.header("📖 Agent System Documentation")
            
            # MCP Tools Section
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 2rem; border-radius: 15px; margin: 1rem 0;
                        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);'>
                <h2 style='color: white; margin-top: 0;'>🔌 MCP (Model Context Protocol) Tools</h2>
                <p style='color: white; font-size: 1.1rem;'>
                    MCP tools enable standardized communication between agents and external services.
                    Our system implements MCP-compatible tools for seamless integration.
                </p>
                <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
                    <h3 style='color: white;'>Available MCP Tools:</h3>
                    <ul style='color: white; font-size: 1rem;'>
                        <li><strong>MCP Weather Tool:</strong> Fetches real-time weather data for agricultural planning</li>
                        <li><strong>MCP Crop Recommendation Tool:</strong> Provides intelligent crop recommendations based on multiple factors</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # OpenAPI Tools Section
            st.markdown("""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                        padding: 2rem; border-radius: 15px; margin: 1rem 0;
                        box-shadow: 0 8px 25px rgba(245, 87, 108, 0.3);'>
                <h2 style='color: white; margin-top: 0;'>🌐 OpenAPI Tools</h2>
                <p style='color: white; font-size: 1.1rem;'>
                    OpenAPI-compatible tools for accessing external REST APIs and services.
                </p>
                <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
                    <h3 style='color: white;'>Available OpenAPI Tools:</h3>
                    <ul style='color: white; font-size: 1rem;'>
                        <li><strong>OpenAPI Weather Tool:</strong> Weather data via REST API</li>
                        <li><strong>OpenAPI Crop Tool:</strong> Crop data and recommendations via API</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Built-in Tools Section
            st.markdown("""
            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                        padding: 2rem; border-radius: 15px; margin: 1rem 0;
                        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.3);'>
                <h2 style='color: white; margin-top: 0;'>⚙️ Built-in Tools</h2>
                <p style='color: white; font-size: 1.1rem;'>
                    Core tools integrated directly into the agent system.
                </p>
                <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
                    <h3 style='color: white;'>Available Built-in Tools:</h3>
                    <ul style='color: white; font-size: 1rem;'>
                        <li><strong>Google Search Tool:</strong> Real-time web search capabilities</li>
                        <li><strong>Calculator Tool:</strong> Mathematical computations and calculations</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Other Features
            st.markdown("""
            ### ✅ Additional Features
            
            **Multi-Agent System**
            - LLM-powered agents (Gemini 2.5 Flash)
            - Sequential, Parallel, and Loop execution patterns
            - Agent orchestration and coordination
            
            **Sessions & Memory**
            - InMemorySessionService for session management
            - Memory Bank for long-term memory storage
            - Context compaction and optimization
            
            **Observability**
            - Comprehensive logging and tracing
            - Real-time metrics and performance monitoring
            - Agent evaluation and quality assessment
            
            **A2A Protocol**
            - Agent-to-agent communication
            - Agent discovery and routing
            - Message passing and coordination
            
            **Deployment**
            - Docker containerization
            - Docker Compose for orchestration
            - Health checks and monitoring
            """)
            
    except Exception as e:
        st.error(f"Error loading Agent System: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

def main():
    # Sidebar navigation
    st.sidebar.title("🌱 Nilam Navigation")
    st.sidebar.markdown("---")
    
    # Navigation options
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["Nilam Chat", "Leafine", "🤖 Agent System"],
        index=0  # Default to Nilam Chat
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.markdown("""
    **Nilam** - Your Agricultural Assistant
    
    Navigate between different sections:
    - **Nilam Chat**: AI-powered agricultural assistance
    - **Leafine**: Leaf disease detection
    - **Agent System**: Multi-agent system with MCP tools & advanced features
    """)
    
    # Main content area
    if page == "Nilam Chat": 
        run_nilamchat()
    
    elif page == "Leafine":
        st.markdown("""
            <div class='main-header'>
                    <div style='font-size: 1.8rem; opacity: 0.9;'>
                        🍃 Leafine
                    </div>
            </div>
        """, unsafe_allow_html=True)
        run_leafine()
    
    elif page == "🤖 Agent System":
        run_agent_system()

if __name__ == "__main__":
    main()
