import streamlit as st

def load_css():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

    *, *::before, *::after { box-sizing: border-box; }
    #MainMenu, footer, header { visibility: hidden !important; }
    .block-container { padding: 0rem !important; max-width: 100% !important; }
    html, body, [class*="css"], label, p { font-family: 'Plus Jakarta Sans', sans-serif !important; color: #1E293B !important; }

    .stApp {
        background-color: #F8FAFC;
        background-image: radial-gradient(#E2E8F0 1px, transparent 1px);
        background-size: 24px 24px;
    }

    div[data-testid="stVerticalBlock"] > div {
        background: transparent !important; border: none !important;
        box-shadow: none !important; padding: 0 !important; margin-bottom: 0 !important;
    }

    .vs-topbar {
        display: flex; align-items: center; justify-content: space-between;
        padding: 16px 32px; background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(12px); border-bottom: 1px solid #E2E8F0;
        position: sticky; top: 0; z-index: 999; box-shadow: 0 4px 20px rgba(0,0,0,0.02);
    }
    .vs-logo {
        font-size: 1.6rem; font-weight: 800; letter-spacing: -0.5px;
        background: linear-gradient(135deg, #4F46E5 0%, #EC4899 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.2;
    }
    .vs-caption { font-family: 'Space Mono', monospace; font-size: 0.65rem; color: #64748B; letter-spacing: 0.5px; text-transform: uppercase; }

    .stTabs [data-baseweb="tab-list"] {
        background: #FFFFFF !important; border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important; padding: 6px !important; gap: 6px !important; margin-bottom: 1rem !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important; border: none !important; border-radius: 8px !important;
        color: #64748B !important; font-weight: 600 !important; font-size: 0.8rem !important;
        padding: 10px 18px !important; transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background: #EEF2FF !important; color: #4F46E5 !important; font-weight: 700 !important;
    }
    div[data-testid="stTabsContent"] {
        background: #FFFFFF !important; border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important; padding: 24px !important; box-shadow: 0 10px 30px rgba(0,0,0,0.03) !important;
    }

    .tools-panel {
        background: #F8FAFC; border: 1px solid #E2E8F0;
        border-radius: 12px; padding: 16px; margin-bottom: 16px;
    }
    .tools-title {
        font-size: 0.8rem; font-weight: 700; color: #334155;
        margin-bottom: 12px; display: flex; align-items: center; gap: 8px;
        border-bottom: 1px solid #E2E8F0; padding-bottom: 8px;
    }

    .stButton button {
        background: #FFFFFF !important; border: 1px solid #CBD5E1 !important;
        color: #334155 !important; font-weight: 600 !important; border-radius: 8px !important;
        transition: all 0.2s ease !important; padding: 12px !important; width: 100% !important;
    }
    .stButton button:hover {
        border-color: #4F46E5 !important; color: #4F46E5 !important;
        background: #EEF2FF !important; transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.15) !important;
    }

    label { color: #334155 !important; font-weight: 700 !important; font-size: 0.8rem !important; }
    .stSlider div[data-baseweb="slider"] > div > div > div { background-color: #4F46E5 !important; }

    .img-lbl {
        font-family: 'Space Mono', monospace; font-size: 0.65rem; font-weight: 700;
        letter-spacing: 1px; text-transform: uppercase; padding: 6px 12px;
        border-radius: 6px; margin-bottom: 12px; display: inline-block;
        background: #F1F5F9; color: #475569; border: 1px solid #E2E8F0;
    }
    .lbl-result { background: #EEF2FF; border-color: #C7D2FE; color: #4F46E5; }
    img { border-radius: 12px !important; border: 1px solid #E2E8F0 !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }

    div[data-testid="stFileUploadDropzone"] {
        background: #FFFFFF !important; border: 1.5px dashed #CBD5E1 !important;
        border-radius: 12px !important; padding: 16px !important;
    }
    div[data-testid="stFileUploadDropzone"]:hover { border-color: #4F46E5 !important; background: #EEF2FF !important; }
    </style>""", unsafe_allow_html=True)

def render_topbar():
    st.markdown("""
    <div class="vs-topbar">
        <div><div class="vs-logo">VisionStudio.</div><div class="vs-caption">Digital Image Processing Laboratory</div></div>
    </div>
    """, unsafe_allow_html=True)

def show_canvas(before, after=None, title_after="", is_gray_after=False, is_gray_before=False):
    if after is None:
        c_space1, c_img, c_space2 = st.columns([1, 2, 1])
        with c_img:
            st.markdown('<div class="img-lbl">🖼️ ORIGINAL ASSET</div>', unsafe_allow_html=True)
            st.image(before, use_container_width=True, channels="GRAY" if is_gray_before else "RGB")
            st.info("👈 Pilih alat di panel sebelah kiri lalu tekan tombol proses untuk melihat hasil.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="img-lbl">🖼️ ORIGINAL</div>', unsafe_allow_html=True)
            st.image(before, use_container_width=True, channels="GRAY" if is_gray_before else "RGB")
        with col2:
            st.markdown(f'<div class="img-lbl lbl-result">✨ HASIL: {title_after.upper()}</div>', unsafe_allow_html=True)
            st.image(after, use_container_width=True, channels="GRAY" if is_gray_after else "RGB")