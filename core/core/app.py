import streamlit as st
import cv2
import numpy as np

# Import dari folder core yang sudah kita buat
from core.ui_components import load_css, render_topbar, show_canvas
from core.image_filters import to_grayscale, to_binary, arithmetic_ops, logic_ops, plot_histogram, apply_filter, apply_morphology

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VisionStudio Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Render Custom CSS
load_css()
render_topbar()

# ── STATE MANAGEMENT ─────────────────────────────────────────────────────────
def reset_views():
    for key in ['core_view', 'arith_view', 'logic_view', 'hist_view', 'conv_view', 'morph_view']:
        st.session_state[key] = None

for key in ['core_view', 'arith_view', 'logic_view', 'hist_view', 'conv_view', 'morph_view']:
    if key not in st.session_state:
        st.session_state[key] = None

# ── LAYOUT UTAMA ────────────────────────────────────────────────────────────
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

        # ── TAB 3: LOGIC OPS ──
        with t3:
            c_tools, c_canvas = st.columns([1, 2.5], gap="large")
            with c_tools:
                st.markdown('<div class="tools-panel"><div class="tools-title">🧠 Bitwise Engine</div>', unsafe_allow_html=True)
                logic_op = st.selectbox("Gerbang Logika", ["AND", "OR", "XOR", "NOT"])
                st.caption("Sistem otomatis menggunakan mask internal untuk operasi AND/OR/XOR.")
                    
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