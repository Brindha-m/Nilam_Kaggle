import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stMainBlockContainer {
        padding: 0rem;
    }
    .stMain {
        padding: 0rem;
    }
    iframe {
        width: 100%;
        height: 100vh; 
        border: none;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown(
        """
        <iframe src="https://brindha-m-leafine.streamlit.app/?embed=true&embed_options=disable_scrolling,dark_theme"
                width="100%" 
                height="100%" 
                frameborder="0"
                loading="lazy">
        </iframe>
        """, 
        unsafe_allow_html=True
    )
    
    APP_URL = "https://brindha-m-leafine.streamlit.app/"
    
    st.markdown("""
    <style>
    .custom-button {
        background: linear-gradient(135deg, #8b7355 0%, #ede4d3 50%, #7a8471 100%);
        padding: 1rem 2.5rem;
        border-radius: 20px;
        color: #4a4a4a !important;  /* Dark grey color with !important */
        text-align: center;
        font-weight: 700;
        font-size: 1.5rem;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        text-decoration: none !important; 
        display: inline-block;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
    }
    .custom-button:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 40px rgba(0,0,0,0.2);
        text-decoration: none !important;
        color: #4a4a4a !important;  /* Maintain dark grey on hover */
    }
    .custom-button:visited {
        color: #4a4a4a !important;  /* Maintain dark grey for visited links */
    }
    .custom-button:active {
        color: #4a4a4a !important;  /* Maintain dark grey when clicked */
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Updated link to open in full screen
    st.markdown(
        f'<a href="{APP_URL}?embed=false" target="_blank" class="custom-button">🚀 Open Leafine.. </a>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
