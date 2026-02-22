import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import json
import os
import hashlib
import base64
from pathlib import Path

# ─── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="AWS Cloud Clubs Mecs – Certificate Generator",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Logo helper ────────────────────────────────────────────────
LOGO_PATH = str(Path(__file__).parent / "assets" / "logo.png")

def get_base64_image(image_path: str) -> str:
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_b64 = get_base64_image(LOGO_PATH)

# ─── Purple AWS Cloud Clubs Theme CSS ───────────────────────────
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    :root {{
        --purple-50:  #F5F0FF;
        --purple-100: #E8D5F5;
        --purple-200: #D4B0F0;
        --purple-300: #B87DE8;
        --purple-400: #9B59D0;
        --purple-500: #7B2D8E;
        --purple-600: #6A1B7A;
        --purple-700: #4A1259;
        --purple-800: #2D1B4E;
        --purple-900: #1A0A2E;
        --accent:     #A855F7;
        --accent-glow: rgba(168, 85, 247, 0.35);
        --gold:       #F59E0B;
    }}

    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Inter', sans-serif !important;
    }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #1e0836 0%, #2D1B4E 50%, #1A0A2E 100%) !important;
        border-right: 1px solid rgba(168,85,247,0.2);
    }}
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li,
    [data-testid="stSidebar"] label {{
        color: #E8D5F5 !important;
    }}

    /* ── Headings ── */
    h1, h2, h3 {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
    }}
    h1 {{
        background: linear-gradient(135deg, #A855F7, #D946EF, #F59E0B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    /* ── Buttons ── */
    .stButton > button {{
        background: linear-gradient(135deg, var(--purple-500), var(--accent)) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.02em;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px var(--accent-glow) !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px var(--accent-glow) !important;
    }}
    /* Primary download button */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, #7B2D8E, #A855F7) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        padding: 0.75rem 2rem !important;
        box-shadow: 0 4px 20px var(--accent-glow) !important;
        transition: all 0.3s ease !important;
    }}
    .stDownloadButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(168,85,247,0.45) !important;
    }}

    /* ── Inputs ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {{
        background: rgba(45,27,78,0.8) !important;
        border: 1px solid rgba(168,85,247,0.3) !important;
        border-radius: 10px !important;
        color: #E8D5F5 !important;
    }}
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px var(--accent-glow) !important;
    }}
    .stSelectbox > div > div {{
        background: rgba(45,27,78,0.8) !important;
        border: 1px solid rgba(168,85,247,0.3) !important;
        border-radius: 10px !important;
        color: #E8D5F5 !important;
    }}

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: rgba(168,85,247,0.08) !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        color: #E8D5F5 !important;
        font-weight: 500 !important;
        border: 1px solid transparent !important;
        transition: all 0.3s ease;
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, var(--purple-500), var(--accent)) !important;
        color: white !important;
        border: 1px solid var(--accent) !important;
        box-shadow: 0 4px 15px var(--accent-glow);
    }}
    .stTabs [data-baseweb="tab-highlight"] {{
        display: none;
    }}

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {{
        background: rgba(45,27,78,0.4) !important;
        border: 2px dashed rgba(168,85,247,0.35) !important;
        border-radius: 14px !important;
        padding: 16px !important;
    }}

    /* ── Slider ── */
    .stSlider > div > div > div > div {{
        background: var(--accent) !important;
    }}

    /* ── Alerts ── */
    .stSuccess {{
        background: rgba(34,197,94,0.1) !important;
        border: 1px solid rgba(34,197,94,0.3) !important;
        border-radius: 12px !important;
    }}
    .stWarning {{
        background: rgba(245,158,11,0.1) !important;
        border: 1px solid rgba(245,158,11,0.3) !important;
        border-radius: 12px !important;
    }}
    .stError {{
        background: rgba(239,68,68,0.1) !important;
        border: 1px solid rgba(239,68,68,0.3) !important;
        border-radius: 12px !important;
    }}

    /* ── Hero card ── */
    .hero-card {{
        background: linear-gradient(135deg, #2D1B4E 0%, #3D2260 40%, #4A1259 100%);
        border: 1px solid rgba(168,85,247,0.3);
        border-radius: 20px;
        padding: 36px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(168,85,247,0.15);
        position: relative;
        overflow: hidden;
    }}
    .hero-card::before {{
        content: '';
        position: absolute;
        top: -50%; right: -50%;
        width: 100%; height: 100%;
        background: radial-gradient(circle, rgba(168,85,247,0.1) 0%, transparent 70%);
        pointer-events: none;
    }}

    /* ── Info card ── */
    .info-card {{
        background: linear-gradient(135deg, #2D1B4E, #3D2260);
        border: 1px solid rgba(168,85,247,0.2);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }}
    .info-card:hover {{
        border-color: rgba(168,85,247,0.5);
        box-shadow: 0 8px 24px rgba(168,85,247,0.15);
        transform: translateY(-2px);
    }}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {{ width: 8px; }}
    ::-webkit-scrollbar-track {{ background: var(--purple-900); }}
    ::-webkit-scrollbar-thumb {{ background: var(--purple-600); border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: var(--accent); }}

    hr {{ border-color: rgba(168,85,247,0.2) !important; }}

    .footer {{
        text-align: center;
        padding: 2rem 0 1rem;
        color: rgba(232,213,245,0.4);
        font-size: 0.8rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════════════
#  ORIGINAL CERTIFICATE GENERATOR LOGIC (KEPT INTACT)
# ═══════════════════════════════════════════════════════════════

# Admin credentials (change these!)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()

# Initialize session state for storing configuration
if 'config' not in st.session_state:
    st.session_state.config = {
        'template_path': None,
        'template_image': None,
        'name_x': 500,
        'name_y': 400,
        'font_size': 60,
        'font_color': (0, 0, 0),
        'font_style': 'Times New Roman Italic',
        'stroke_width': 0,
        'stroke_color': (0, 0, 0),
        'participants': []
    }

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'show_login' not in st.session_state:
    st.session_state.show_login = False

# Available font styles with fallback options
FONT_STYLES = {
    'Arial': ['arial.ttf', 'Arial.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'],
    'Arial Bold': ['arialbd.ttf', 'Arial-Bold.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'],
    'Arial Narrow': ['arialn.ttf', 'Arial-Narrow.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'],
    'Times New Roman': ['times.ttf', 'Times-New-Roman.ttf', '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'],
    'Times New Roman Bold': ['timesbd.ttf', 'Times-New-Roman-Bold.ttf', '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'],
    'Times New Roman Italic': ['timesi.ttf', 'Times-New-Roman-Italic.ttf', '/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'],
    'Courier New': ['cour.ttf', 'Courier-New.ttf', '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf'],
    'Courier New Bold': ['courbd.ttf', 'Courier-New-Bold.ttf', '/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf'],
    'Georgia': ['georgia.ttf', 'Georgia.ttf', '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'],
    'Georgia Bold': ['georgiab.ttf', 'Georgia-Bold.ttf', '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'],
    'Comic Sans MS': ['comic.ttf', 'Comic-Sans-MS.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'],
    'Impact': ['impact.ttf', 'Impact.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'],
    'Verdana': ['verdana.ttf', 'Verdana.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'],
    'Verdana Bold': ['verdanab.ttf', 'Verdana-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'],
    'Trebuchet MS': ['trebuc.ttf', 'Trebuchet-MS.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'],
    'Trebuchet MS Bold': ['trebucbd.ttf', 'Trebuchet-MS-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'],
}


def save_config():
    """Save configuration to a JSON file"""
    config_to_save = {
        'name_x': st.session_state.config['name_x'],
        'name_y': st.session_state.config['name_y'],
        'font_size': st.session_state.config['font_size'],
        'font_color': st.session_state.config['font_color'],
        'font_style': st.session_state.config.get('font_style', 'Times New Roman Italic'),
        'stroke_width': st.session_state.config.get('stroke_width', 0),
        'stroke_color': st.session_state.config.get('stroke_color', (0, 0, 0)),
        'participants': st.session_state.config['participants'],
        'template_path': st.session_state.config['template_path']
    }
    with open('cert_config.json', 'w') as f:
        json.dump(config_to_save, f)


def load_config():
    """Load configuration from JSON file"""
    if os.path.exists('cert_config.json'):
        with open('cert_config.json', 'r') as f:
            config = json.load(f)
            if 'font_color' in config and isinstance(config['font_color'], list):
                config['font_color'] = tuple(config['font_color'])
            if 'stroke_color' in config and isinstance(config['stroke_color'], list):
                config['stroke_color'] = tuple(config['stroke_color'])
            st.session_state.config.update(config)


def check_password(username, password):
    """Check if username and password are correct"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return username == ADMIN_USERNAME and password_hash == ADMIN_PASSWORD_HASH


def login_page():
    """Display login page for admin"""
    st.markdown(
        """
        <div class="info-card" style="text-align:center; max-width:480px; margin:2rem auto;">
            <div style="font-size:2.5rem; margin-bottom:8px;">🔐</div>
            <h2 style="color:#A855F7; margin:0 0 8px;">Admin Login</h2>
            <p style="color:#C4A8E0; font-size:0.9rem;">Enter your credentials to access the admin panel.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("🔓  Login", use_container_width=True)

            if submit:
                if check_password(username, password):
                    st.session_state.authenticated = True
                    st.session_state.show_login = False
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")


def logout():
    """Logout admin"""
    st.session_state.authenticated = False
    st.session_state.show_login = False


def generate_certificate(name, template_img, x, y, font_size, color,
                         font_style='Times New Roman Italic',
                         stroke_width=0, stroke_color=(0, 0, 0)):
    """Generate certificate with name on template"""
    img = template_img.copy()
    draw = ImageDraw.Draw(img)

    if isinstance(color, (list, tuple)):
        color = tuple(int(c) for c in color)
    else:
        color = (0, 0, 0)

    if isinstance(stroke_color, (list, tuple)):
        stroke_color = tuple(int(c) for c in stroke_color)
    else:
        stroke_color = (0, 0, 0)

    font = None
    font_paths = FONT_STYLES.get(font_style, FONT_STYLES['Times New Roman Italic'])

    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, int(font_size))
            break
        except Exception:
            continue

    if font is None:
        fallback_fonts = [
            "arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/Library/Fonts/Arial.ttf",
        ]
        for fallback in fallback_fonts:
            try:
                font = ImageFont.truetype(fallback, int(font_size))
                break
            except Exception:
                continue

    if font is None:
        font = ImageFont.load_default()

    try:
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
    except Exception:
        text_width = len(name) * (int(font_size) // 2)

    stroke_width = int(stroke_width)
    if stroke_width > 0:
        draw.text((int(x) - text_width // 2, int(y)), name, font=font,
                  fill=color, stroke_width=stroke_width, stroke_fill=stroke_color)
    else:
        draw.text((int(x) - text_width // 2, int(y)), name, font=font, fill=color)

    return img


# Load saved configuration
load_config()


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR  — AWS Cloud Clubs branded
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    if logo_b64:
        st.markdown(
            f"""
            <div style="text-align:center; padding:1.5rem 0 0.5rem;">
                <img src="data:image/png;base64,{logo_b64}"
                     style="width:160px; filter:drop-shadow(0 0 10px rgba(255,255,255,0.5)) drop-shadow(0 4px 12px rgba(168,85,247,0.4));" />
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="text-align:center; margin-bottom:0.5rem;">
            <span style="font-size:0.78rem; color:#C4A8E0;">☁️ Certificate Portal</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    mode = st.radio(
        "🧭  Navigate",
        ["📜 Download Certificate", "🔧 Admin Panel"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center; opacity:0.55; font-size:0.78rem; line-height:1.6;">
            Powered by<br/>
            <strong style="color:#A855F7;">AWS Cloud Clubs – Mecs</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("")
    st.markdown(
        """
        <div style="text-align:center; opacity:0.4; font-size:0.72rem;">
            💡 Users download certificates from the main page.<br/>
            Admins configure via the Admin Panel.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════
#  PAGE: DOWNLOAD CERTIFICATE
# ═══════════════════════════════════════════════════════════════
if mode == "📜 Download Certificate":
    # Hero banner
    hero_logo = f'<img src="data:image/png;base64,{logo_b64}" style="width:90px; filter:drop-shadow(0 0 12px rgba(255,255,255,0.6)) drop-shadow(0 4px 16px rgba(168,85,247,0.5));" />' if logo_b64 else ""
    st.markdown(
        f"""
        <div class="hero-card">
            <div style="display:flex; align-items:center; gap:24px; flex-wrap:wrap;">
                {hero_logo}
                <div>
                    <h1 style="margin:0; font-size:2rem;">Download Your Certificate</h1>
                    <p style="color:#D4B0F0; font-size:1rem; margin-top:6px;">
                        Enter your full name below to generate &amp; download your certificate 🎓
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Load template if exists
    if st.session_state.config.get('template_path') and os.path.exists(st.session_state.config['template_path']):
        try:
            st.session_state.config['template_image'] = Image.open(st.session_state.config['template_path'])
        except Exception as e:
            st.error(f"Error loading template: {e}")
            st.session_state.config['template_image'] = None

    # Name input — always visible
    st.markdown("#### ✍️ Enter your name")
    user_name = st.text_input("Your Full Name", placeholder="e.g., John Doe",
                              key="download_name_input", label_visibility="collapsed")

    # No template warning
    if not st.session_state.config.get('template_image'):
        st.warning("⚠️ No certificate template has been uploaded yet. Please contact the administrator.")
        st.info("🔧 Admin: Go to the **Admin Panel** and upload a certificate template.")

    # Generate if name + template exist
    if user_name and st.session_state.config.get('template_image'):
        if st.session_state.config.get('participants') and user_name not in st.session_state.config['participants']:
            st.error("❌ Name not found in participant list. Please check your spelling or contact the administrator.")
            st.info(f"📋 Total participants registered: {len(st.session_state.config['participants'])}")
        else:
            try:
                cert_color = st.session_state.config.get('font_color', (0, 0, 0))
                if isinstance(cert_color, list):
                    cert_color = tuple(cert_color)

                cert_stroke_color = st.session_state.config.get('stroke_color', (0, 0, 0))
                if isinstance(cert_stroke_color, list):
                    cert_stroke_color = tuple(cert_stroke_color)

                certificate = generate_certificate(
                    user_name,
                    st.session_state.config['template_image'],
                    st.session_state.config.get('name_x', 500),
                    st.session_state.config.get('name_y', 400),
                    st.session_state.config.get('font_size', 60),
                    cert_color,
                    st.session_state.config.get('font_style', 'Times New Roman Italic'),
                    st.session_state.config.get('stroke_width', 0),
                    cert_stroke_color,
                )

                st.success("✅ Certificate generated successfully!")
                st.image(certificate, caption="Your Certificate", use_container_width=True)

                buf = io.BytesIO()
                certificate.save(buf, format='PNG')
                buf.seek(0)

                st.download_button(
                    label="⬇️  Download Certificate",
                    data=buf,
                    file_name=f"certificate_{user_name.replace(' ', '_')}.png",
                    mime="image/png",
                    type="primary",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"❌ Error generating certificate: {str(e)}")
                st.info("Please contact the administrator if this error persists.")


# ═══════════════════════════════════════════════════════════════
#  PAGE: ADMIN PANEL
# ═══════════════════════════════════════════════════════════════
elif mode == "🔧 Admin Panel":
    if not st.session_state.authenticated:
        login_page()
    else:
        # Logout button
        with st.sidebar:
            if st.button("🚪  Logout", use_container_width=True):
                logout()
                st.rerun()

        st.markdown("# 🔧 Admin Panel")

        # ── 1. Template Upload ──
        st.markdown(
            """
            <div class="info-card">
                <h3 style="color:#A855F7; margin-top:0;">1️⃣  Upload Certificate Template</h3>
                <p style="color:#C4A8E0; font-size:0.88rem;">Upload a PNG/JPG image to use as the certificate background.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader("Choose a certificate template image",
                                         type=['png', 'jpg', 'jpeg'])

        if uploaded_file:
            template_img = Image.open(uploaded_file)
            st.session_state.config['template_image'] = template_img
            template_img.save('certificate_template.png')
            st.session_state.config['template_path'] = 'certificate_template.png'
            st.success("Template uploaded successfully!")
            st.image(template_img, caption="Certificate Template", use_container_width=True)
        elif st.session_state.config['template_path'] and os.path.exists(st.session_state.config['template_path']):
            template_img = Image.open(st.session_state.config['template_path'])
            st.session_state.config['template_image'] = template_img
            st.image(template_img, caption="Current Certificate Template", use_container_width=True)

        st.markdown("")

        # ── 2. Configure Text Placement ──
        st.markdown(
            """
            <div class="info-card">
                <h3 style="color:#A855F7; margin-top:0;">2️⃣  Configure Text Placement</h3>
                <p style="color:#C4A8E0; font-size:0.88rem;">Adjust position, font, and styling for the participant name.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            name_x = st.number_input("Name X Position (horizontal)",
                                     min_value=0,
                                     value=st.session_state.config['name_x'])
            name_y = st.number_input("Name Y Position (vertical)",
                                     min_value=0,
                                     value=st.session_state.config['name_y'])
        with col2:
            font_size = st.slider("Font Size", 20, 150,
                                  st.session_state.config['font_size'])
            font_style = st.selectbox(
                "Font Style & Weight",
                options=list(FONT_STYLES.keys()),
                index=list(FONT_STYLES.keys()).index(
                    st.session_state.config.get('font_style', 'Times New Roman Italic')),
                help="Choose font family and weight.",
            )

        st.markdown("##### 🎨 Text Styling")
        col3, col4 = st.columns(2)
        with col3:
            color_hex = st.color_picker("Text Color", "#000000")
            font_color = tuple(int(color_hex[i:i + 2], 16) for i in (1, 3, 5))
        with col4:
            stroke_width = st.slider("Text Outline Thickness", 0, 10,
                                     st.session_state.config.get('stroke_width', 0),
                                     help="0 = No outline")

        if stroke_width > 0:
            stroke_color_hex = st.color_picker("Outline Color", "#000000")
            stroke_color = tuple(int(stroke_color_hex[i:i + 2], 16) for i in (1, 3, 5))
        else:
            stroke_color = (0, 0, 0)

        # Update config
        st.session_state.config['name_x'] = name_x
        st.session_state.config['name_y'] = name_y
        st.session_state.config['font_size'] = font_size
        st.session_state.config['font_style'] = font_style
        st.session_state.config['font_color'] = font_color
        st.session_state.config['stroke_width'] = stroke_width
        st.session_state.config['stroke_color'] = stroke_color

        st.markdown("")

        # ── 3. Preview ──
        st.markdown(
            """
            <div class="info-card">
                <h3 style="color:#A855F7; margin-top:0;">3️⃣  Preview</h3>
                <p style="color:#C4A8E0; font-size:0.88rem;">See how the certificate looks with a sample name.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_prev1, col_prev2 = st.columns([3, 1])
        with col_prev1:
            preview_name = st.text_input("Preview Name", "John Doe", key="preview_name_input")
        with col_prev2:
            st.write("")
            st.write("")
            if st.button("🔄 Refresh Preview", use_container_width=True):
                st.rerun()

        if st.session_state.config['template_image']:
            preview_cert = generate_certificate(
                preview_name,
                st.session_state.config['template_image'],
                int(name_x), int(name_y), int(font_size),
                font_color, font_style, int(stroke_width), stroke_color,
            )
            st.image(preview_cert,
                     caption=f"Preview (Font: {font_style}, Size: {font_size})",
                     use_container_width=True)

        outline_text = f", Outline: {stroke_width}px" if stroke_width > 0 else ""
        st.info(f"💡 Current: Font={font_style}, Size={font_size}, "
                f"Position=({name_x}, {name_y}){outline_text}")
        st.caption("💡 Change settings above and click **Refresh Preview** to see changes.")

        st.markdown("")

        # ── 4. Participants ──
        st.markdown(
            """
            <div class="info-card">
                <h3 style="color:#A855F7; margin-top:0;">4️⃣  Manage Participants</h3>
                <p style="color:#C4A8E0; font-size:0.88rem;">Add individual or bulk participant names.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        new_participant = st.text_input("Add Participant Name")
        if st.button("➕ Add Participant"):
            if new_participant and new_participant not in st.session_state.config['participants']:
                st.session_state.config['participants'].append(new_participant)
                save_config()
                st.success(f"Added **{new_participant}**")
                st.rerun()

        st.markdown("##### 📋 Bulk Add")
        bulk_participants = st.text_area("Enter names (one per line)")
        if st.button("➕ Add All"):
            names = [n.strip() for n in bulk_participants.split('\n') if n.strip()]
            for name in names:
                if name not in st.session_state.config['participants']:
                    st.session_state.config['participants'].append(name)
            save_config()
            st.success(f"Added **{len(names)}** participants")
            st.rerun()

        if st.session_state.config['participants']:
            st.markdown(f"##### 👥 Current Participants ({len(st.session_state.config['participants'])})")
            for i, participant in enumerate(st.session_state.config['participants']):
                col_p1, col_p2 = st.columns([4, 1])
                with col_p1:
                    st.text(participant)
                with col_p2:
                    if st.button("🗑️", key=f"remove_{i}"):
                        st.session_state.config['participants'].remove(participant)
                        save_config()
                        st.rerun()

        st.markdown("")
        if st.button("💾  Save All Settings", type="primary", use_container_width=True):
            save_config()
            st.success("✅ Configuration saved successfully!")


# ═══════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    """
    <div class="footer">
        © 2026 AWS Cloud Clubs – Mecs &nbsp;|&nbsp; Built with 💜 and Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)