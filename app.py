import streamlit as st
import cv2
import numpy as np
import pandas as pd

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VisionStudio Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── STATE MANAGEMENT ─────────────────────────────────────────────────────────
def reset_views():
    for key in ['core_view', 'arith_view', 'logic_view', 'hist_view', 'conv_view', 'morph_view']:
        st.session_state[key] = None

for key in ['core_view', 'arith_view', 'logic_view', 'hist_view', 'conv_view', 'morph_view']:
    if key not in st.session_state:
        st.session_state[key] = None

# ── AESTHETIC LIGHT MODE CSS (High Contrast & Clean) ─────────────────────────
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

# ── HELPER FUNCTION: RENDER CANVAS ───────────────────────────────────────────
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

# ── CACHED IMAGE PROCESSING FUNCTIONS ────────────────────────────────────────
@st.cache_data
def to_grayscale(img): return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

@st.cache_data
def to_binary(img, threshold=128):
    _, binary = cv2.threshold(to_grayscale(img), threshold, 255, cv2.THRESH_BINARY)
    return binary

@st.cache_data
def arithmetic_ops(img, operation, value):
    f = img.astype(np.float32)
    if   operation == "Tambah (+)": res = cv2.add(f, value)
    elif operation == "Kurang (-)": res = cv2.subtract(f, value)
    elif operation == "Kali (×)":   res = cv2.multiply(f, value)
    elif operation == "Bagi (÷)":   res = cv2.divide(f, value)
    return np.clip(res, 0, 255).astype(np.uint8)

@st.cache_data
def logic_ops(img1, mask, operation):
    if operation == "NOT": return cv2.bitwise_not(img1)
    if operation == "AND": return cv2.bitwise_and(img1, mask)
    if operation == "OR":  return cv2.bitwise_or(img1, mask)
    if operation == "XOR": return cv2.bitwise_xor(img1, mask)

def plot_histogram(img):
    if len(img.shape) == 2:
        st.area_chart(pd.DataFrame(cv2.calcHist([img], [0], None, [256], [0, 256]).flatten(), columns=["Intensity"]), color="#4F46E5", height=200)
    else:
        data = { "Red": cv2.calcHist([img], [2], None, [256], [0, 256]).flatten(), "Green": cv2.calcHist([img], [1], None, [256], [0, 256]).flatten(), "Blue": cv2.calcHist([img], [0], None, [256], [0, 256]).flatten() }
        st.line_chart(pd.DataFrame(data), color=["#EF4444", "#10B981", "#3B82F6"], height=200)

@st.cache_data
def apply_filter(img, filter_type):
    if filter_type == "Gaussian Blur": return cv2.GaussianBlur(img, (9, 9), 0)
    elif filter_type == "Sharpening":  return cv2.filter2D(img, -1, np.array([[0,-1,0],[-1,5,-1],[0,-1,0]]))
    elif filter_type == "Sobel Edge":
        gray = to_grayscale(img)
        return cv2.magnitude(cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3), cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)).astype(np.uint8)

@st.cache_data
def apply_morphology(img, operation, se_shape, se_size):
    _, binary = cv2.threshold(to_grayscale(img), 127, 255, cv2.THRESH_BINARY_INV)
    shapes = {"Persegi": cv2.MORPH_RECT, "Silang": cv2.MORPH_CROSS, "Elips": cv2.MORPH_ELLIPSE}
    se = cv2.getStructuringElement(shapes[se_shape], (se_size, se_size))
    if   operation == "Dilasi":  return cv2.dilate(binary, se, iterations=1)
    elif operation == "Erosi":   return cv2.erode(binary, se, iterations=1)
    elif operation == "Opening": return cv2.morphologyEx(binary, cv2.MORPH_OPEN, se)
    elif operation == "Closing": return cv2.morphologyEx(binary, cv2.MORPH_CLOSE, se)

# ── LAYOUT UTAMA ────────────────────────────────────────────────────────────
st.markdown("""
<div class="vs-topbar">
    <div><div class="vs-logo">VisionStudio.</div><div class="vs-caption">Digital Image Processing Laboratory</div></div>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 3.2], gap="large")

# ═════ SIDEBAR KIRI: ASSET MANAGER ═════
with col_left:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="img-lbl" style="width:100%; text-align:center;">📁 ASSET MANAGER</div>', unsafe_allow_html=True)
    
    uploaded_file1 = st.file_uploader("🖼 Image Target", type=["jpg", "jpeg", "png"], key="m_in", on_change=reset_views)
    img1 = img1_rgb = None
    
    if uploaded_file1:
        img1 = cv2.imdecode(np.asarray(bytearray(uploaded_file1.read()), dtype=np.uint8), cv2.IMREAD_COLOR)
        img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        st.image(img1_rgb, use_container_width=True)
        st.success("Target Load Success", icon="✅")

# ═════ AREA KANAN: WORKSPACE & TABS ═════
with col_right:
    st.markdown("<br>", unsafe_allow_html=True)
    if img1 is not None:
        t1, t2, t3, t4, t5, t6 = st.tabs(["🎨 Core Vision", "✦ Arithmetic", "⊕ Logic Ops", "📊 Histogram", "🌀 Convolution", "⬡ Morphology"])

        # ── TAB 1: CORE VISION ──
        with t1:
            c_tools, c_canvas = st.columns([1, 2.5], gap="large")
            with c_tools:
                st.markdown('<div class="tools-panel"><div class="tools-title">⚙️ Basic Converter</div>', unsafe_allow_html=True)
                if st.button("Jadikan Grayscale"): st.session_state.core_view = "gray"
                st.markdown("<hr style='margin:15px 0'>", unsafe_allow_html=True)
                thresh = st.slider("Batas Threshold", 0, 255, 128)
                if st.button("Jadikan Biner"): 
                    st.session_state.core_view = "binary"
                    st.session_state.core_thresh = thresh
                st.markdown('</div>', unsafe_allow_html=True)
                
            with c_canvas:
                if st.session_state.core_view == "gray":
                    show_canvas(img1_rgb, to_grayscale(img1), "Grayscale Output", is_gray_after=True)
                elif st.session_state.core_view == "binary":
                    show_canvas(img1_rgb, to_binary(img1, st.session_state.core_thresh), f"Binary (Th:{st.session_state.core_thresh})", is_gray_after=True)
                else: show_canvas(img1_rgb)

        # ── TAB 2: ARITHMETIC ──
        with t2:
            c_tools, c_canvas = st.columns([1, 2.5], gap="large")
            with c_tools:
                st.markdown('<div class="tools-panel"><div class="tools-title">➕ Math Operators</div>', unsafe_allow_html=True)
                op = st.selectbox("Jenis Aritmatika", ["Tambah (+)", "Kurang (-)", "Kali (×)", "Bagi (÷)"])
                val = st.slider("Nilai Konstanta", 1, 255, 50)
                if st.button("Proses Aritmatika"): st.session_state.arith_view = (op, val)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with c_canvas:
                if st.session_state.arith_view is not None:
                    curr_op, curr_val = st.session_state.arith_view
                    res = arithmetic_ops(img1, curr_op, curr_val)
                    show_canvas(img1_rgb, cv2.cvtColor(res, cv2.COLOR_BGR2RGB), f"Hasil {curr_op} {curr_val}")
                else: show_canvas(img1_rgb)

        # ── TAB 3: LOGIC OPS (1 FOTO - AUTO MASK) ──
        with t3:
            c_tools, c_canvas = st.columns([1, 2.5], gap="large")
            with c_tools:
                st.markdown('<div class="tools-panel"><div class="tools-title">🧠 Bitwise Engine</div>', unsafe_allow_html=True)
                logic_op = st.selectbox("Gerbang Logika", ["AND", "OR", "XOR", "NOT"])
                st.caption("Sistem otomatis menggunakan mask internal (lingkaran) untuk operasi AND/OR/XOR.")
                    
                if st.button("Eksekusi Logika"): 
                    st.session_state.logic_view = logic_op
                st.markdown('</div>', unsafe_allow_html=True)
                
            with c_canvas:
                if st.session_state.logic_view is not None:
                    curr_op = st.session_state.logic_view
                    if curr_op == "NOT":
                        show_canvas(img1_rgb, cv2.cvtColor(logic_ops(img1, None, "NOT"), cv2.COLOR_BGR2RGB), "NOT (Invert)")
                    else:
                        mask = np.zeros_like(img1)
                        h, w = img1.shape[:2]
                        cv2.circle(mask, (w//2, h//2), min(h, w)//3, (255, 255, 255), -1)
                        
                        res = logic_ops(img1, mask, curr_op)
                        show_canvas(img1_rgb, cv2.cvtColor(res, cv2.COLOR_BGR2RGB), f"Bitwise {curr_op}")
                else: show_canvas(img1_rgb)

        # ── TAB 4: HISTOGRAM ──
        with t4:
            c_tools, c_canvas = st.columns([1, 2.5], gap="large")
            with c_tools:
                st.markdown('<div class="tools-panel"><div class="tools-title">📊 Visualizer</div>', unsafe_allow_html=True)
                if st.button("Ekstrak Histogram"): st.session_state.hist_view = True
                st.markdown('</div>', unsafe_allow_html=True)
                
            with c_canvas:
                if st.session_state.hist_view:
                    hc1, hc2 = st.columns([1, 1.5])
                    with hc1:
                        st.markdown('<div class="img-lbl">🖼️ ORIGINAL</div>', unsafe_allow_html=True)
                        st.image(img1_rgb, use_container_width=True)
                    with hc2:
                        st.markdown('<div class="img-lbl lbl-result">✨ PIXEL HISTOGRAM</div>', unsafe_allow_html=True)
                        plot_histogram(img1)
                else: show_canvas(img1_rgb)

        # ── TAB 5: CONVOLUTION ──
        with t5:
            c_tools, c_canvas = st.columns([1, 2.5], gap="large")
            with c_tools:
                st.markdown('<div class="tools-panel"><div class="tools-title">🌀 Spatial Filter</div>', unsafe_allow_html=True)
                f_type = st.selectbox("Jenis Kernel", ["Gaussian Blur", "Sharpening", "Sobel Edge"])
                if st.button("Terapkan Filter"): st.session_state.conv_view = f_type
                st.markdown('</div>', unsafe_allow_html=True)
                
            with c_canvas:
                if st.session_state.conv_view is not None:
                    curr_f = st.session_state.conv_view
                    res = apply_filter(img1, curr_f)
                    is_gray = len(res.shape) == 2
                    show_canvas(img1_rgb, res if is_gray else cv2.cvtColor(res, cv2.COLOR_BGR2RGB), f"Filter {curr_f}", is_gray_after=is_gray)
                else: show_canvas(img1_rgb)

        # ── TAB 6: MORPHOLOGY ──
        with t6:
            c_tools, c_canvas = st.columns([1, 2.5], gap="large")
            with c_tools:
                st.markdown('<div class="tools-panel"><div class="tools-title">⬡ Math Morphology</div>', unsafe_allow_html=True)
                m_op = st.selectbox("Operasi", ["Erosi", "Dilasi", "Opening", "Closing"])
                se_shape = st.selectbox("Element (SE)", ["Persegi", "Silang", "Elips"])
                se_size = st.slider("Ukuran Kernel", 3, 21, 5, step=2)
                if st.button("Proses Morfologi"): st.session_state.morph_view = (m_op, se_shape, se_size)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with c_canvas:
                if st.session_state.morph_view is not None:
                    curr_m, curr_s, curr_z = st.session_state.morph_view
                    res = apply_morphology(img1, curr_m, curr_s, curr_z)
                    
                    # PERBAIKAN: Memastikan foto original (berwarna) tetap ada di kiri
                    show_canvas(img1_rgb, res, f"{curr_m} ({curr_s})", is_gray_after=True, is_gray_before=False)
                else:
                    st.info("💡 Pilih alat di kiri, sistem akan memproses citra menjadi biner di belakang layar.")
                    show_canvas(img1_rgb)

    else:
        st.markdown("""
        <div style="text-align:center; padding: 100px 20px; border:2px dashed #CBD5E1; border-radius: 16px; background:#FFFFFF;">
            <div style="font-size: 3rem;">✨</div>
            <h3 style="color: #334155; font-weight: 800;">WORKSPACE STANDBY</h3>
            <p style="color: #64748B;">Upload gambar utama di Asset Manager (Kiri) untuk mulai mengeksplorasi.</p>
        </div>
        """, unsafe_allow_html=True)