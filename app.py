
import streamlit as st
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from PIL import Image
from pathlib import Path
import fitz

st.set_page_config(page_title="Modern Physics Simulator — Mohammad Imani", page_icon="Atom", layout="wide")

def load_image(path, default_size=(150, 150)):
    p = Path(path)
    if p.exists():
        try:
            img = Image.open(p)
            return img
        except:
            return None
    return None

cover = load_image("cover.png")
logo = load_image("logo.png", )

# ---------------------------
# Header
col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
with col1:
    if logo:
        st.image(logo, width=160)
with col2:
    st.markdown("""
    <audio autoplay>
                <source src="https://dl5.songsara.net/FRE/01-FAV/Study%20With%20Me%20(Playlist%20By%20SONGSARA.NET)/01%20The%20Music%20Box.mp3" type="audio/mpeg"/>
    </audio> 
    <div style="text-align:center; background: linear-gradient(90deg, #0b1a33, #0f2a55); padding:20px; border-radius:12px; box-shadow:0 6px 20px rgba(0,0,0,0.5);position:relative;right: 55px">
    <h1 style="color:#e6f2ff; margin:0; font-family:'Georgia', serif;">Modern Physics Interactive Simulator</h1>
    <p style="color:#a8c8e8; margin:8px 0 0 0; font-size:19px;">
    <b>Mohammad Imani</b> — Based on <i>Krane, Modern Physics (2nd Ed.)</i>
    </p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    if cover:
        st.image(cover, width=200)

st.markdown("---")

# ---------------------------
# Sidebar
st.sidebar.title("Chapters")
module = st.sidebar.radio("Select Chapter", (
    "Introduction",
    "1 — Special Relativity",
    "2 — Photoelectric Effect",
    "3 — Double-Slit Interference",
    "4 — Bohr Model",
    "5 — Particle in a Box",
    "Key Equations"
))

# Constants
h_eVs = 4.135667696e-15
c = 299792458

# Styles
BOX = "background:#1a2a44; padding:18px; border-radius:10px; border-left:5px solid #4a9eff; margin:15px 0; color:#e6f2ff; line-height:1.8;"
VAR = "color:#87cefa; font-weight:bold;"

# ========================
# Introduction
# ========================
if module == "Introduction":
    st.markdown("<h2 style='color:#4a9eff; text-align:center;'>Introduction</h2>", unsafe_allow_html=True)
    
    # Persian Poem in Nastaliq-style 
    st.markdown(f"""
    <div style="text-align:center; margin:30px 0; font-family:'Noto Nastaliq Urdu', serif; font-size:28px; color:#ffd700; line-height:2;">
    همه عمر بر ندارم سر از این خمار مستی<br>
    که هنوز من نبودم که تو بر دلم نشستی
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='{BOX}'>
    This interactive web application simulates key concepts from <b>Modern Physics</b> by Kenneth S. Krane (2nd Edition). 
    Each chapter includes:
    <ul>
    <li>Comprehensive lesson (5+ lines)</li>
    <li>Interactive controls and real-time explanations</li>
    <li>High-quality Plotly visualizations</li>
    <li>Accurate equations from the textbook</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align:center; margin-top:40px; color:#a8c8e8; font-size:14px;">
    <b>Department of Physics, University of Zanjan</b><br><br>
    Special thanks to:<br>
    <b>Dr. Reza Rasouli</b>, Faculty Member, University of Zanjan<br>
    <b>Dr. Mojtaba Nasiri</b>, Head of Physics Department, University of Zanjan
    </div>
    """, unsafe_allow_html=True)

# ========================
# 1. Special Relativity
# ========================
elif module == "1 — Special Relativity":
    st.markdown("<h2 style='color:#4a9eff;'>Chapter 1 — Special Relativity</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='{BOX}'>
    <b>Lesson:</b><br>
    Einstein's special relativity shows that space and time are not absolute. At speeds near light, length contracts, time dilates, and mass increases. These effects become significant only when v > 0.1c.<br><br>
    Two postulates: 1) Laws of physics are the same in all inertial frames. 2) Speed of light in vacuum is constant for all observers (c = 3×10⁸ m/s).<br><br>
    <b>Key Equations:</b><br>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"\gamma = \frac{1}{\sqrt{1 - \frac{v^2}{c^2}}}")
    st.latex(r"L = \frac{L_0}{\gamma}")
    st.latex(r"\Delta t = \gamma \Delta \tau")

    col1, col2 = st.columns([0.55, 0.45])
    with col1:
        v_frac = st.slider("v/c", 0.0, 0.99, 0.7, 0.01)
        L0 = st.number_input("Proper length L₀ (m)", 1.0, 100.0, 20.0)
        gamma = 1 / np.sqrt(1 - v_frac**2)
        L = L0 / gamma
        st.markdown(f"<div style='{BOX}'>γ = <span style='{VAR}'>{gamma:.4f}</span> | L = <span style='{VAR}'>{L:.2f} m</span></div>", unsafe_allow_html=True)
    
    with col2:
        if v_frac < 0.3: st.info("Negligible relativity")
        elif v_frac < 0.7: st.warning("Significant contraction")
        else: st.error("Near c! γ > 2")

    fig = make_subplots(rows=2, cols=1, row_heights=[0.4, 0.6])
    fig.add_shape(type="rect", x0=0, x1=L0, y0=0, y1=1, fillcolor="#87ceeb", opacity=0.3, row=1, col=1)
    fig.add_shape(type="rect", x0=5, x1=5+L, y0=0, y1=1, fillcolor="#ff6b6b", opacity=0.3, row=1, col=1)
    t = np.linspace(0, 10, 200)
    fig.add_trace(go.Scatter(x=v_frac*t, y=t, mode='lines', line=dict(color='#4a9eff')), row=2, col=1)
    fig.add_trace(go.Scatter(x=L0 + v_frac*t, y=t, mode='lines', line=dict(color='#ff6b6b')), row=2, col=1)
    fig.update_layout(height=700, paper_bgcolor="#0b1a33", plot_bgcolor="#0b1a33", font=dict(color="#e6f2ff"))
    st.plotly_chart(fig, use_container_=True)

# ========================
# 2. Photoelectric Effect
# ========================
elif module == "2 — Photoelectric Effect":
    st.markdown("<h2 style='color:#4a9eff;'>Chapter 2 — Photoelectric Effect</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='{BOX}'>
    <b>Lesson:</b><br>
    Einstein showed light behaves as photons with energy E = h f. If photon energy exceeds work function φ, electrons are ejected. Maximum kinetic energy: K_max = h f - φ.<br><br>
    Key insight: Light intensity affects number of photons (current), not energy. K_max depends only on frequency.<br><br>
    <b>Equations:</b><br>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"E = h f")
    st.latex(r"K_{max} = h f - \phi")

    freq_1e14 = st.slider("Frequency (×10¹⁴ Hz)", 1.0, 100.0, 15.0, 0.5)
    phi = st.slider("Work function φ (eV)", 1.0, 5.0, 2.2, 0.1)
    E = h_eVs * freq_1e14 * 1e14
    Kmax = max(E - phi, 0)
    st.markdown(f"<div style='{BOX}'>E = <span style='{VAR}'>{E:.3f} eV</span> | K_max = <span style='{VAR}'>{Kmax:.3f} eV</span></div>", unsafe_allow_html=True)
    if E > phi: st.success("Electrons emitted")
    else: st.error("Below threshold")

    f = np.linspace(0, 100, 500) * 1e14
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=f/1e14, y=np.maximum(h_eVs*f - phi, 0), line=dict(color='#4a9eff')))
    fig.add_trace(go.Scatter(x=[freq_1e14], y=[Kmax], mode='markers', marker=dict(size=12, color='red')))
    fig.update_layout(height=500, paper_bgcolor="#0b1a33", plot_bgcolor="#0b1a33", font=dict(color="#e6f2ff"))
    st.plotly_chart(fig, use_container_width=True)

# ========================
# 3. Double-Slit
# ========================
elif module == "3 — Double-Slit Interference":
    st.markdown("<h2 style='color:#4a9eff;'>Chapter 3 — Double-Slit Interference</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='{BOX}'>
    <b>Lesson:</b><br>
    Young's experiment proved light is a wave. Two slits act as coherent sources. Path difference Δ = d sinθ determines constructive/destructive interference. Bright fringes at Δ = mλ, dark at (m+½)λ.<br><br>
    Fringe spacing Δx ≈ λL/d. Increasing d or decreasing λ reduces spacing.<br><br>
    <b>Equations:</b><br>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"\Delta = d \sin\theta \approx \frac{d x}{L}")
    st.latex(r"\Delta x = \frac{\lambda L}{d}")

    d_mm = st.slider("Slit separation d (mm)", 0.1, 2.0, 0.5, 0.01)
    lam_nm = st.slider("Wavelength λ (nm)", 400, 700, 550, 10)
    L = st.slider("Screen distance L (m)", 0.5, 5.0, 1.0, 0.1)
    d = d_mm * 1e-3
    lam = lam_nm * 1e-9
    x = np.linspace(-0.05, 0.05, 1000)
    I = np.cos(np.pi * d * x / (lam * L))**2
    fig = go.Figure(go.Scatter(x=x*1000, y=I, line=dict(color='#87cefa')))
    fig.update_layout(height=500, paper_bgcolor="#0b1a33", plot_bgcolor="#0b1a33", font=dict(color="#e6f2ff"))
    st.plotly_chart(fig, use_container_width=True)

# ========================
# 4. Bohr Model
# ========================
elif module == "4 — Bohr Model":
    st.markdown("<h2 style='color:#4a9eff;'>Chapter 4 — Bohr Model</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='{BOX}'>
    <b>Lesson:</b><br>
    Bohr proposed electrons orbit in quantized states with radius r_n = n² a_0. Energy levels: E_n = -13.6/n² eV. Transitions emit/absorb photons with hν = |E_i - E_f|.<br><br>
    This explains hydrogen spectrum and resolves classical collapse paradox.<br><br>
    <b>Equations:</b><br>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"r_n = n^2 a_0")
    st.latex(r"E_n = -\frac{13.6}{n^2} \text{ eV}")

    n1 = st.slider("Initial state n₁", 1, 6, 3)
    n2 = st.slider("Final state n₂", 1, 6, 2)
    r1 = n1**2 * 0.529
    dE = abs(-13.6/n1**2 + 13.6/n2**2)
    st.markdown(f"<div style='{BOX}'>r = <span style='{VAR}'>{r1:.1f} Å</span> | ΔE = <span style='{VAR}'>{dE:.3f} eV</span></div>", unsafe_allow_html=True)

    fig = go.Figure()
    for n in range(1,7):
        E = -13.6/n**2
        color = "#ffd700" if n==n1 else ("#87cefa" if n==n2 else "#555")
        fig.add_trace(go.Scatter(x=[0,1], y=[E,E], line=dict(color=color, width=5)))
    fig.update_layout(height=500, yaxis_autorange="reversed", paper_bgcolor="#0b1a33", plot_bgcolor="#0b1a33")
    st.plotly_chart(fig, use_container_width=True)

# ========================
# 5. Particle in a Box
# ========================
elif module == "5 — Particle in a Box":
    st.markdown("<h2 style='color:#4a9eff;'>Chapter 5 — Particle in Infinite Well</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='{BOX}'>
    <b>Lesson:</b><br>
    A particle in an infinite well can only have wavelengths that fit: λ_n = 2L/n. This leads to quantized energy E_n ∝ n². Superposition of two states with different n causes time-dependent probability density.<br><br>
    This demonstrates wave nature of particles.<br><br>
    <b>Equations:</b><br>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"\psi_n(x) = \sqrt{\frac{2}{L}} \sin(\frac{n\pi x}{L})")
    st.latex(r"E_n \propto n^2")

    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        n1 = st.slider("State n₁", 1, 5, 1)
        n2 = st.slider("State n₂", 1, 5, 2)
        amp = st.slider("Amplitude of ψ₂", 0.0, 1.0, 0.7, 0.05)
        play = st.button("Play Time Evolution", type="primary")
    
    L = 1.0
    x = np.linspace(0, L, 500)
    
    if not play:
        psi_t = np.sqrt(2/L) * np.sin(n1 * np.pi * x / L) + amp * np.sqrt(2/L) * np.sin(n2 * np.pi * x / L)
        prob = np.abs(psi_t)**2
        prob /= prob.max() + 1e-12
        fig = go.Figure(go.Scatter(x=x, y=prob, line=dict(color='#90ee90')))
        fig.update_layout(height=500, paper_bgcolor="#0b1a33", plot_bgcolor="#0b1a33")
        st.plotly_chart(fig, use_container_width=True)
        st.info("Stationary superposition")
    else:
        placeholder = st.empty()
        for t in np.linspace(0, 4, 100):
            psi1 = np.sqrt(2/L) * np.sin(n1 * np.pi * x / L) * np.exp(-1j * n1**2 * t)
            psi2 = amp * np.sqrt(2/L) * np.sin(n2 * np.pi * x / L) * np.exp(-1j * n2**2 * t)
            prob = np.abs(psi1 + psi2)**2
            prob /= prob.max() + 1e-12
            fig = go.Figure(go.Scatter(x=x, y=prob, line=dict(color='#90ee90')))
            fig.update_layout(height=500, paper_bgcolor="#0b1a33", plot_bgcolor="#0b1a33", font=dict(color="#e6f2ff"))
            placeholder.plotly_chart(fig, use_container_width=True)
            st.rerun() 

# ========================
# Key Equations
# ========================
elif module == "Key Equations":
    st.markdown("<h2 style='color:#4a9eff;'>Key Equations — Krane</h2>", unsafe_allow_html=True)
    st.latex(r"\gamma = \frac{1}{\sqrt{1 - v^2/c^2}}")
    st.latex(r"K_{max} = h f - \phi")
    st.latex(r"\Delta x = \frac{\lambda L}{d}")
    st.latex(r"E_n = -\frac{13.6}{n^2} \text{ eV}")
    st.latex(r"\psi_n(x) = \sqrt{\frac{2}{L}} \sin(\frac{n\pi x}{L})")