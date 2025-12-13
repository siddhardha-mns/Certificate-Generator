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
        'participants': []
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
    
    st.info("💡 Default credentials: username='admin', password='admin123'")
    st.warning("⚠️ Please change the default credentials in the code for security!")

def logout():
    """Logout admin"""
    st.session_state.authenticated = False
    st.session_state.show_login = False

def generate_certificate(name, template_img, x, y, font_size, color):
    """Generate certificate with name on template"""
    img = template_img.copy()
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use a nice font, fallback to default if not available
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Get text bounding box for centering if needed
    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]
    
    # Draw the name
    draw.text((x - text_width//2, y), name, font=font, fill=color)
    
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
            
            # Color picker
            color_hex = st.color_picker("Text Color", "#000000")
            # Convert hex to RGB
            font_color = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
        
        # Update config
        st.session_state.config['name_x'] = name_x
        st.session_state.config['name_y'] = name_y
        st.session_state.config['font_size'] = font_size
        st.session_state.config['font_color'] = font_color
        
        # Preview
        st.header("3. Preview")
        preview_name = st.text_input("Preview Name", "John Doe")
        
        if st.session_state.config['template_image']:
            preview_cert = generate_certificate(
                preview_name,
                st.session_state.config['template_image'],
                name_x, name_y, font_size, font_color
            )
            st.image(preview_cert, caption="Preview Certificate", use_column_width=True)
        
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
                certificate = generate_certificate(
                    user_name,
                    st.session_state.config['template_image'],
                    st.session_state.config['name_x'],
                    st.session_state.config['name_y'],
                    st.session_state.config['font_size'],
                    st.session_state.config['font_color']
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
