# modern_physics_streamlit_PERSIAN_PERFECT.py
# شبیه‌ساز تعاملی فیزیک جدید — کرین (ویرایش دوم)
# نویسنده: محمد ایمانی | دانشگاه زنجان
import streamlit as st
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from PIL import Image
from pathlib import Path
import fitz
import time

st.set_page_config(page_title="شبیه‌ساز فیزیک جدید — محمد ایمانی", page_icon="Atom", layout="wide")

# ---------------------------
# بارگذاری و تغییر اندازهٔ تصاویر
def resize_image(img, size):
    img.thumbnail(size, Image.LANCZOS)
    return img

def load_image(path, size):
    p = Path(path)
    if p.exists():
        try:
            img = Image.open(p)
            return resize_image(img, size)
        except:
            return None
    return None

# استخراج جلد از PDF (صفحه اول)
def extract_cover():
    pdf_path = Path("فیزیک جدید کرین.pdf")
    if pdf_path.exists():
        try:
            doc = fitz.open(str(pdf_path))
            page = doc.load_page(0)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img_path = "cover_extracted.png"
            pix.save(img_path)
            return resize_image(Image.open(img_path), (80, 110))
        except Exception as e:
            st.warning(f"خطا در استخراج جلد: {e}")
    return None

cover = extract_cover() or load_image("cover.png", (80, 110))
logo = load_image("logo.png", (80, 80))

# ---------------------------
# سربرگ — تقارن کامل
col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
with col1:
    if logo:
        st.image(logo, width=80)
with col2:
    st.markdown("""
    <div style="text-align:center; background:linear-gradient(90deg,#0b1a33,#0f2a55);
                padding:18px; border-radius:12px; box-shadow:0 6px 20px rgba(0,0,0,0.5);">
        <h1 style="color:#e6f2ff; margin:0; font-size:30px;">شبیه‌ساز تعاملی فیزیک جدید</h1>
        <p style="color:#a8c8e8; margin:6px 0 0 0; font-size:16px;">
            <b>محمد ایمانی</b> — کرین، ویرایش دوم
        </p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    if cover:
        st.image(cover, width=80)

st.markdown("---")

# ---------------------------
# نوار کناری
st.sidebar.title("فصل‌ها")
module = st.sidebar.radio("انتخاب فصل", (
    "مقدمه",
    "۱ — نسبیت خاص",
    "۲ — اثر فوتوالکتریک",
    "۳ — تداخل دو شکاف",
    "۴ — مدل بور",
    "۵ — ذره در جعبه",
    "معادلات کلیدی"
))

# ثابت‌ها
h_eVs = 4.135667696e-15
c = 299792458

# استایل‌ها
BOX_STYLE = ("background:#1a2a44; padding:16px; border-radius:10px; "
             "border-left:5px solid #4a9eff; margin:14px 0; color:#e6f2ff; "
             "line-height:1.8; font-size:15px;")
VAR_STYLE = "color:#87cefa; font-weight:bold;"

# ========================
# مقدمه
# ========================
if module == "مقدمه":
    st.markdown("<h2 style='color:#4a9eff; text-align:center; font-size:24px;'>مقدمه</h2>", unsafe_allow_html=True)

    # شعر نستعلیق — فونت کوچکتر
    st.markdown("""
    <div style="text-align:center; margin:25px 0; font-family:'Noto Nastaliq Urdu',serif;
                font-size:19px; color:#ffd700; line-height:2;">
        همه عمر بر ندارم سر از این خمار مستی<br>
        که هنوز من نبودم که تو بر دلم نشستی
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='{BOX_STYLE}'>
    این برنامه تعاملی، مفاهیم کلیدی کتاب <b>فیزیک جدید</b> نوشته کنت اس. کرین (ویرایش دوم، ترجمه منیژه رهبر و بهرام معلمی) را شبیه‌سازی می‌کند.
    هر فصل شامل موارد زیر است:
    <ul style="margin:10px 0; padding-left:22px;">
        <li>درسنامه کامل (حداقل پنج خط)</li>
        <li>کنترل‌های تعاملی با توضیحات لحظه‌ای</li>
        <li>نمودارهای باکیفیت</li>
        <li>معادلات دقیق کتاب</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin:30px 0; color:#a8c8e8; font-size:14px; line-height:1.8;">
        <b>دانشکده فیزیک، دانشگاه زنجان</b><br><br>
        با تشکر ویژه از:<br>
        <b>دکتر رضا رسولی</b> — عضو هیئت علمی دانشگاه زنجان<br>
        <b>دکتر مجتبی نصیری</b> — مدیرگروه دانشکده فیزیک دانشگاه زنجان
    </div>
    """, unsafe_allow_html=True)

# ========================
# ۱ — نسبیت خاص
# ========================
elif module == "۱ — نسبیت خاص":
    st.markdown("<h2 style='color:#4a9eff; font-size:24px;'>فصل ۱ — نسبیت خاص</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='{BOX_STYLE}'>
    <b>درسنامه:</b><br>
    نسبیت خاص اینشتین نشان می‌دهد که فضا و زمان مطلق نیستند. در سرعت‌های نزدیک به سرعت نور، طول در جهت حرکت کوتاه می‌شود، زمان کندتر می‌گذرد و جرم افزایش می‌یابد. این اثرات تنها در سرعت‌های بالاتر از یک‌دهم سرعت نور قابل توجه هستند.<br><br>
    دو اصل اساسی: ۱) قوانین فیزیک در تمام چارچوب‌های اینرسی یکسان است. ۲) سرعت نور در خلأ برای همه ناظران ثابت است (۳×۱۰⁸ متر بر ثانیه).<br><br>
    <b>معادلات کلیدی:</b><br>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"\gamma = \frac{1}{\sqrt{1 - \frac{v^2}{c^2}}}")
    st.latex(r"L = \frac{L_0}{\gamma}")
    st.latex(r"\Delta t = \gamma \Delta \tau")

    col1, col2 = st.columns([0.55, 0.45])
    with col1:
        v_c = st.slider("نسبت سرعت به سرعت نور", 0.0, 0.99, 0.7, 0.01)
        L0 = st.number_input("طول اصلی (متر)", 1.0, 100.0, 20.0)
        gamma = 1 / np.sqrt(1 - v_c**2)
        L = L0 / gamma
        st.markdown(f"<div style='{BOX_STYLE}'>γ = <span style='{VAR_STYLE}'>{gamma:.4f}</span> | طول = <span style='{VAR_STYLE}'>{L:.2f} متر</span></div>", unsafe_allow_html=True)

    with col2:
        if v_c < 0.3:
            st.info("اثر نسبیتی ناچیز")
        elif v_c < 0.7:
            st.warning("کوتاه‌شدگی قابل توجه")
        else:
            st.error("نزدیک سرعت نور! γ بزرگ‌تر از ۲")

    fig = make_subplots(rows=2, cols=1, row_heights=[0.4, 0.6])
    fig.add_shape(type="rect", x0=0, x1=L0, y0=0, y1=1, fillcolor="#87ceeb", opacity=0.3, row=1, col=1)
    fig.add_shape(type="rect", x0=5, x1=5+L, y0=0, y1=1, fillcolor="#ff6b6b", opacity=0.3, row=1, col=1)
    t = np.linspace(0, 10, 200)
    fig.add_trace(go.Scatter(x=v_c*t, y=t, mode='lines', line=dict(color='#4a9eff')), row=2, col=1)
    fig.add_trace(go.Scatter(x=L0 + v_c*t, y=t, mode='lines', line=dict(color='#ff6b6b')), row=2, col=1)
    fig.update_layout(height=700, paper_bgcolor="#0b1a33", plot_bgcolor="#0b1a33", font=dict(color="#e6f2ff"))
    st.plotly_chart(fig, use_container_width=True)

# ========================
# ۲ — اثر فوتوالکتریک
# ========================
elif module == "۲ — اثر فوتوالکتریک":
    st.markdown("<h2 style='color:#4a9eff; font-size:24px;'>فصل ۲ — اثر فوتوالکتریک</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='{BOX_STYLE}'>
    <b>درسنامه:</b><br>
    اینشتین نشان داد نور به صورت فوتون با انرژی E = h f است. اگر انرژی فوتون از کارکرد φ بیشتر باشد، الکترون‌ها خارج می‌شوند. حداکثر انرژی جنبشی: K_max = h f - φ.<br><br>
    نکته کلیدی: شدت نور تعداد فوتون‌ها (جریان) را تغییر می‌دهد، نه انرژی آن‌ها. K_max تنها به بسامد بستگی دارد.<br><br>
    <b>معادلات:</b><br>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"E = h f")
    st.latex(r"K_{max} = h f - \phi")

    freq = st.slider("بسامد (×۱۰¹⁴ هرتز)", 1.0, 100.0, 15.0, 0.5)
    phi = st.slider("کارکرد φ (الکترون‌ولت)", 1.0, 5.0, 2.2, 0.1)
    E = h_eVs * freq * 1e14
    Kmax = max(E - phi, 0)
    st.markdown(f"<div style='{BOX_STYLE}'>انرژی = <span style='{VAR_STYLE}'>{E:.3f} الکترون‌ولت</span> | K_max = <span style='{VAR_STYLE}'>{Kmax:.3f} الکترون‌ولت</span></div>", unsafe_allow_html=True)
    if E > phi:
        st.success("الکترون‌ها خارج می‌شوند")
    else:
        st.error("زیر آستانه")

    f_axis = np.linspace(0, 100, 500) * 1e14
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=f_axis/1e14, y=np.maximum(h_eVs*f_axis - phi, 0), line=dict(color='#4a9eff')))
    fig.add_trace(go.Scatter(x=[freq], y=[Kmax], mode='markers', marker=dict(size=12, color='red')))
    fig.update_layout(height=500, paper_bgcolor="#0b1a33", plot_bgcolor="#0b1a33", font=dict(color="#e6f2ff"))
    st.plotly_chart(fig, use_container_width=True)

# ========================
# ۳ — تداخل دو شکاف
# ========================
elif module == "۳ — تداخل دو شکاف":
    st.markdown("<h2 style='color:#4a9eff; font-size:24px;'>فصل ۳ — تداخل دو شکاف</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='{BOX_STYLE}'>
    <b>درسنامه:</b><br>
    آزمایش یانگ ثابت کرد نور موج است. دو شکاف به عنوان منابع همدوس عمل می‌کنند. اختلاف مسیر تعیین‌کننده تداخل سازنده یا مخرب است. نوارهای روشن در اختلاف مسیر برابر با طول موج‌های صحیح، نوارهای تاریک در اختلاف مسیر برابر با نیم‌طول موج.<br><br>
    فاصله نوارها تقریباً برابر است با طول موج × فاصله صفحه / فاصله شکاف‌ها. افزایش فاصله شکاف یا کاهش طول موج، فاصله نوارها را کم می‌کند.<br><br>
    <b>معادلات:</b><br>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"\Delta = d \sin\theta \approx \frac{d x}{L}")
    st.latex(r"\Delta x = \frac{\lambda L}{d}")

    d_mm = st.slider("فاصله شکاف‌ها (میلی‌متر)", 0.1, 2.0, 0.5, 0.01)
    lam_nm = st.slider("طول موج (نانومتر)", 400, 700, 550, 10)
    L = st.slider("فاصله صفحه (متر)", 0.5, 5.0, 1.0, 0.1)
    d = d_mm * 1e-3
    lam = lam_nm * 1e-9
    x = np.linspace(-0.05, 0.05, 1000)
    I = np.cos(np.pi * d * x / (lam * L))**2
    fig = go.Figure(go.Scatter(x=x*1000, y=I, line=dict(color='#87cefa')))
    fig.update_layout(height=500, paper_bgcolor="#0b1a33", plot_bgcolor="#0b1a33", font=dict(color="#e6f2ff"))
    st.plotly_chart(fig, use_container_width=True)

# ========================
# ۴ — مدل بور
# ========================
elif module == "۴ — مدل بور":
    st.markdown("<h2 style='color:#4a9eff; font-size:24px;'>فصل ۴ — مدل بور</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='{BOX_STYLE}'>
    <b>درسنامه:</b><br>
    بور پیشنهاد کرد الکترون‌ها در مدارهای کوانتیده با شعاع r_n = n² a_0 حرکت می‌کنند. سطوح انرژی: E_n = -13.6/n² الکترون‌ولت. گذارها فوتون منتشر یا جذب می‌کنند با hν = |E_i - E_f|.<br><br>
    این مدل طیف هیدروژن را توضیح می‌دهد و پارادوکس فروپاشی کلاسیک را حل می‌کند.<br><br>
    <b>معادلات:</b><br>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"r_n = n^2 a_0")
    st.latex(r"E_n = -\frac{13.6}{n^2} \text{ الکترون‌ولت}")

    n1 = st.slider("حالت اولیه", 1, 6, 3)
    n2 = st.slider("حالت نهایی", 1, 6, 2)
    r = n1**2 * 0.529
    dE = abs(-13.6/n1**2 + 13.6/n2**2)
    st.markdown(f"<div style='{BOX_STYLE}'>شعاع = <span style='{VAR_STYLE}'>{r:.1f} آنگستروم</span> | ΔE = <span style='{VAR_STYLE}'>{dE:.3f} الکترون‌ولت</span></div>", unsafe_allow_html=True)

    fig = go.Figure()
    for n in range(1, 7):
        E = -13.6 / n**2
        color = "#ffd700" if n == n1 else ("#87cefa" if n == n2 else "#555")
        fig.add_trace(go.Scatter(x=[0, 1], y=[E, E], line=dict(color=color, width=5)))
    fig.update_layout(height=500, yaxis_autorange="reversed", paper_bgcolor="#0b1a33", plot_bgcolor="#0b1a33")
    st.plotly_chart(fig, use_container_width=True)

# ========================
# ۵ — ذره در جعبه
# ========================
elif module == "۵ — ذره در جعبه":
    st.markdown("<h2 style='color:#4a9eff; font-size:24px;'>فصل ۵ — ذره در جعبه بی‌نهایت</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='{BOX_STYLE}'>
    <b>درسنامه:</b><br>
    ذره در جعبه بی‌نهایت تنها می‌تواند طول موج‌هایی داشته باشد که در جعبه جا شوند: λ_n = 2L/n. این منجر به انرژی کوانتیده E_n ∝ n² می‌شود. سوپرپوزیشن دو حالت با n متفاوت، چگالی احتمال وابسته به زمان ایجاد می‌کند.<br><br>
    این پدیده ماهیت موجی ذرات را نشان می‌دهد.<br><br>
    <b>معادلات:</b><br>
    </div>
    """, unsafe_allow_html=True)
    st.latex(r"\psi_n(x) = \sqrt{\frac{2}{L}} \sin\left(\frac{n\pi x}{L}\right)")
    st.latex(r"E_n \propto n^2")

    col1, _ = st.columns([0.7, 0.3])
    with col1:
        n1 = st.slider("حالت یک", 1, 5, 1)
        n2 = st.slider("حالت دو", 1, 5, 2)
        amp = st.slider("دامنه حالت دو", 0.0, 1.0, 0.7, 0.05)
        play = st.button("پخش تکامل زمانی", type="primary")

    L = 1.0
    x = np.linspace(0, L, 500)
    placeholder = st.empty()

    if play:
        for t in np.linspace(0, 4, 80):
            psi1 = np.sqrt(2/L) * np.sin(n1*np.pi*x/L) * np.exp(-1j*n1**2*t)
            psi2 = amp * np.sqrt(2/L) * np.sin(n2*np.pi*x/L) * np.exp(-1j*n2**2*t)
            prob = np.abs(psi1 + psi2)**2
            prob /= prob.max() + 1e-12
            fig = go.Figure(go.Scatter(x=x, y=prob, line=dict(color='#90ee90')))
            fig.update_layout(height=400, paper_bgcolor="#0b1a33", plot_bgcolor="#0b1a33", margin=dict(l=0,r=0,t=0,b=0))
            placeholder.plotly_chart(fig, use_container_width=True)
            time.sleep(0.05)
    else:
        psi = np.sqrt(2/L) * (np.sin(n1*np.pi*x/L) + amp*np.sin(n2*np.pi*x/L))
        prob = np.abs(psi)**2
        prob /= prob.max() + 1e-12
        fig = go.Figure(go.Scatter(x=x, y=prob, line=dict(color='#90ee90')))
        fig.update_layout(height=400, paper_bgcolor="#0b1a33", plot_bgcolor="#0b1a33")
        placeholder.plotly_chart(fig, use_container_width=True)

# ========================
# معادلات کلیدی
# ========================
elif module == "معادلات کلیدی":
    st.markdown("<h2 style='color:#4a9eff; font-size:24px;'>معادلات کلیدی — کرین</h2>", unsafe_allow_html=True)
    st.latex(r"\gamma = \frac{1}{\sqrt{1 - v^2/c^2}}")
    st.latex(r"K_{max} = h f - \phi")
    st.latex(r"\Delta x = \frac{\lambda L}{d}")
    st.latex(r"E_n = -\frac{13.6}{n^2} \text{ الکترون‌ولت}")
    st.latex(r"\psi_n(x) = \sqrt{\frac{2}{L}} \sin\left(\frac{n\pi x}{L}\right)")