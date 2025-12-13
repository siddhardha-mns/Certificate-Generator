import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import json
import os
import hashlib

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
        'font_color': (0, 0, 0),  # RGB
        'font_style': 'Arial',
        'stroke_width': 0,
        'stroke_color': (0, 0, 0),
        'participants': []
    }

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

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'show_login' not in st.session_state:
    st.session_state.show_login = False

def save_config():
    """Save configuration to a JSON file"""
    config_to_save = {
        'name_x': st.session_state.config['name_x'],
        'name_y': st.session_state.config['name_y'],
        'font_size': st.session_state.config['font_size'],
        'font_color': st.session_state.config['font_color'],
        'participants': st.session_state.config['participants']
    }
    with open('cert_config.json', 'w') as f:
        json.dump(config_to_save, f)

def load_config():
    """Load configuration from JSON file"""
    if os.path.exists('cert_config.json'):
        with open('cert_config.json', 'r') as f:
            config = json.load(f)
            # Convert font_color list to tuple if it exists
            if 'font_color' in config and isinstance(config['font_color'], list):
                config['font_color'] = tuple(config['font_color'])
            # Convert stroke_color list to tuple if it exists
            if 'stroke_color' in config and isinstance(config['stroke_color'], list):
                config['stroke_color'] = tuple(config['stroke_color'])
            st.session_state.config.update(config)

def check_password(username, password):
    """Check if username and password are correct"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return username == ADMIN_USERNAME and password_hash == ADMIN_PASSWORD_HASH

def login_page():
    """Display login page for admin"""
    st.title("🔐 Admin Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", type="primary")
        
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

def generate_certificate(name, template_img, x, y, font_size, color, font_style='Arial', stroke_width=0, stroke_color=(0, 0, 0)):
    """Generate certificate with name on template"""
    img = template_img.copy()
    draw = ImageDraw.Draw(img)
    
    # Ensure color is a tuple of integers
    if isinstance(color, (list, tuple)):
        color = tuple(int(c) for c in color)
    else:
        color = (0, 0, 0)  # Default to black
    
    # Ensure stroke_color is a tuple of integers
    if isinstance(stroke_color, (list, tuple)):
        stroke_color = tuple(int(c) for c in stroke_color)
    else:
        stroke_color = (0, 0, 0)  # Default to black
    
    # Try to load the selected font style
    font = None
    font_paths = FONT_STYLES.get(font_style, FONT_STYLES['Arial'])
    
    # Try each font path for the selected style
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, int(font_size))
            break
        except Exception as e:
            continue
    
    # If no font loaded, try common fallbacks
    if font is None:
        fallback_fonts = [
            "arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/Library/Fonts/Arial.ttf"
        ]
        for fallback in fallback_fonts:
            try:
                font = ImageFont.truetype(fallback, int(font_size))
                break
            except:
                continue
    
    # Last resort: use default font (but scale it if possible)
    if font is None:
        try:
            font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
    
    # Get text bounding box for centering if needed
    try:
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
    except:
        text_width = len(name) * (int(font_size) // 2)
    
    # Draw the name with stroke (outline) if stroke_width > 0
    stroke_width = int(stroke_width)
    if stroke_width > 0:
        draw.text((int(x) - text_width//2, int(y)), name, font=font, fill=color, stroke_width=stroke_width, stroke_fill=stroke_color)
    else:
        draw.text((int(x) - text_width//2, int(y)), name, font=font, fill=color)
    
    return img

# Load saved configuration
load_config()

# Sidebar for mode selection
st.sidebar.title("Certificate Generator")
mode = st.sidebar.radio("Select Mode", ["Admin Panel", "Download Certificate"])

# Admin Panel - Show login if not authenticated
if mode == "Admin Panel":
    if not st.session_state.authenticated:
        login_page()
    else:
        # Logout button in sidebar
        if st.sidebar.button("🚪 Logout"):
            logout()
            st.rerun()
        
        st.title("🔧 Admin Panel")
    
        # Template Upload
        st.header("1. Upload Certificate Template")
        uploaded_file = st.file_uploader("Choose a certificate template image", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            template_img = Image.open(uploaded_file)
            st.session_state.config['template_image'] = template_img
            
            # Save template to disk
            template_img.save('certificate_template.png')
            st.session_state.config['template_path'] = 'certificate_template.png'
            
            st.success("Template uploaded successfully!")
            st.image(template_img, caption="Certificate Template", use_column_width=True)
        elif st.session_state.config['template_path'] and os.path.exists(st.session_state.config['template_path']):
            template_img = Image.open(st.session_state.config['template_path'])
            st.session_state.config['template_image'] = template_img
            st.image(template_img, caption="Current Certificate Template", use_column_width=True)
        
        # Configuration Settings
        st.header("2. Configure Text Placement")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name_x = st.number_input("Name X Position (horizontal)", 
                                      min_value=0, 
                                      value=st.session_state.config['name_x'])
            name_y = st.number_input("Name Y Position (vertical)", 
                                      min_value=0, 
                                      value=st.session_state.config['name_y'])
        
        with col2:
            font_size = st.slider("Font Size", 20, 150, st.session_state.config['font_size'])
            
            # Font style selector - organized by weight
            font_style = st.selectbox(
                "Font Style & Weight",
                options=list(FONT_STYLES.keys()),
                index=list(FONT_STYLES.keys()).index(st.session_state.config.get('font_style', 'Arial')),
                help="Choose font family and weight (Regular/Bold/Italic). Regular fonts are thinner, Bold fonts are thicker."
            )
        
        # Text styling options
        st.subheader("Text Styling")
        col3, col4 = st.columns(2)
        
        with col3:
            # Color picker
            color_hex = st.color_picker("Text Color", "#000000")
            # Convert hex to RGB
            font_color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
        
        with col4:
            # Stroke/outline options
            stroke_width = st.slider("Text Outline Thickness", 0, 10, st.session_state.config.get('stroke_width', 0), 
                                     help="0 = No outline, higher values = thicker outline")
        
        # Stroke color (only show if stroke_width > 0)
        if stroke_width > 0:
            stroke_color_hex = st.color_picker("Outline Color", "#000000")
            stroke_color = tuple(int(stroke_color_hex[i:i+2], 16) for i in (1, 3, 5))
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
        
        # Preview
        st.header("3. Preview")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            preview_name = st.text_input("Preview Name", "John Doe", key="preview_name_input")
        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            if st.button("🔄 Refresh Preview", use_container_width=True):
                st.rerun()
        
        if st.session_state.config['template_image']:
            # Force preview to update by using current values directly
            preview_cert = generate_certificate(
                preview_name,
                st.session_state.config['template_image'],
                int(name_x), int(name_y), int(font_size), font_color, font_style, int(stroke_width), stroke_color
            )
            
            # Display preview
            st.image(preview_cert, caption=f"Preview Certificate (Font: {font_style}, Size: {font_size})", use_column_width=True)
        
        outline_text = f", Outline: {stroke_width}px" if stroke_width > 0 else ""
        st.info(f"💡 Current settings: Font={font_style}, Size={font_size}, Position=({name_x}, {name_y}){outline_text}")
        
        st.caption("💡 Tip: Change any setting above and click 'Refresh Preview' to see changes.")
        
        # Participant Management
        st.header("4. Manage Participants")
        
        # Add single participant
        new_participant = st.text_input("Add Participant Name")
        if st.button("Add Participant"):
            if new_participant and new_participant not in st.session_state.config['participants']:
                st.session_state.config['participants'].append(new_participant)
                save_config()
                st.success(f"Added {new_participant}")
                st.rerun()
        
        # Bulk add participants
        st.subheader("Bulk Add Participants")
        bulk_participants = st.text_area("Enter names (one per line)")
        if st.button("Add All"):
            names = [name.strip() for name in bulk_participants.split('\n') if name.strip()]
            for name in names:
                if name not in st.session_state.config['participants']:
                    st.session_state.config['participants'].append(name)
            save_config()
            st.success(f"Added {len(names)} participants")
            st.rerun()
        
        # Display and remove participants
        if st.session_state.config['participants']:
            st.subheader(f"Current Participants ({len(st.session_state.config['participants'])})")
            for i, participant in enumerate(st.session_state.config['participants']):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.text(participant)
                with col2:
                    if st.button("Remove", key=f"remove_{i}"):
                        st.session_state.config['participants'].remove(participant)
                        save_config()
                        st.rerun()
        
        # Save Configuration
        if st.button("💾 Save All Settings", type="primary"):
            save_config()
            st.success("Configuration saved successfully!")

else:  # Download Certificate Mode
    st.title("📜 Download Your Certificate")
    
    # Load template if exists
    if st.session_state.config['template_path'] and os.path.exists(st.session_state.config['template_path']):
        st.session_state.config['template_image'] = Image.open(st.session_state.config['template_path'])
    
    if not st.session_state.config['template_image']:
        st.warning("⚠️ No certificate template has been uploaded yet. Please contact the administrator.")
    else:
        st.write("Enter your name to download your certificate:")
        
        user_name = st.text_input("Your Name", placeholder="Enter your full name")
        
        if user_name:
            # Check if participant is in the list
            if st.session_state.config['participants'] and user_name not in st.session_state.config['participants']:
                st.error("❌ Name not found in participant list. Please check your spelling or contact the administrator.")
            else:
                # Generate certificate
                # Ensure color is properly formatted
                cert_color = st.session_state.config.get('font_color', (0, 0, 0))
                if isinstance(cert_color, list):
                    cert_color = tuple(cert_color)
                
                # Ensure stroke_color is properly formatted
                cert_stroke_color = st.session_state.config.get('stroke_color', (0, 0, 0))
                if isinstance(cert_stroke_color, list):
                    cert_stroke_color = tuple(cert_stroke_color)
                
                certificate = generate_certificate(
                    user_name,
                    st.session_state.config['template_image'],
                    st.session_state.config['name_x'],
                    st.session_state.config['name_y'],
                    st.session_state.config['font_size'],
                    cert_color,
                    st.session_state.config.get('font_style', 'Arial'),
                    st.session_state.config.get('stroke_width', 0),
                    cert_stroke_color
                )
                
                # Display certificate
                st.image(certificate, caption="Your Certificate", use_column_width=True)
                
                # Download button
                buf = io.BytesIO()
                certificate.save(buf, format='PNG')
                buf.seek(0)
                
                st.download_button(
                    label="⬇️ Download Certificate",
                    data=buf,
                    file_name=f"certificate_{user_name.replace(' ', '_')}.png",
                    mime="image/png",
                    type="primary"
                )
                
                st.success("✅ Certificate generated successfully!")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("💡 Tip: Use Admin Panel to configure the certificate template and add participants.")
