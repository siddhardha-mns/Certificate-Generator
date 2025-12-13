# 📜 Certificate Generator App

A simple and elegant Streamlit application for generating personalized event certificates. Admins can upload templates and manage participants, while users can download their certificates instantly.

## ✨ Features

### Admin Features
- 📤 Upload custom certificate templates (PNG/JPG)
- 🎨 Configure text placement (X/Y coordinates)
- 🔤 Customize font size and color
- 👀 Live preview of certificate design
- 👥 Add participants individually or in bulk
- 💾 Persistent configuration storage

### User Features
- ✍️ Enter name to generate certificate
- ✅ Name verification against participant list
- 📥 One-click certificate download
- 🖼️ High-quality PNG output

## 🚀 Installation

1. **Clone or download the repository**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 📖 Usage

### Starting the Application

Run the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Admin Setup

1. **Switch to Admin Panel** (using sidebar)

2. **Upload Certificate Template**
   - Click "Choose a certificate template image"
   - Select your template file (PNG/JPG)

3. **Configure Text Placement**
   - Adjust "Name X Position" (horizontal placement)
   - Adjust "Name Y Position" (vertical placement)
   - Set desired font size (20-150)
   - Choose text color using color picker

4. **Preview Your Design**
   - Enter a sample name in "Preview Name"
   - View how the certificate will look

5. **Add Participants**
   - **Single Addition**: Enter name and click "Add Participant"
   - **Bulk Addition**: Paste names (one per line) and click "Add All"
   - Remove participants using "Remove" button

6. **Save Settings**
   - Click "💾 Save All Settings" to persist configuration

### User Certificate Download

1. **Switch to "Download Certificate"** (using sidebar)

2. **Enter Your Name**
   - Type your full name exactly as registered

3. **Download Certificate**
   - Preview your certificate
   - Click "⬇️ Download Certificate" button
   - Certificate saves as PNG file

## 📁 File Structure

```
certificate-generator/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── cert_config.json           # Auto-generated config (after first save)
└── certificate_template.png   # Auto-saved template (after upload)
```

## 🔧 Configuration Files

The app automatically creates these files:
- `cert_config.json` - Stores text placement, font settings, and participant list
- `certificate_template.png` - Stores the uploaded certificate template

## 💡 Tips

### For Admins
- Use high-resolution templates (1920x1080 or higher) for best quality
- Test with various name lengths in preview mode
- The X position centers text horizontally around that point
- Save settings after any changes to persist them

### For Users
- Enter your name exactly as it appears in the participant list
- If your name isn't found, contact the event administrator
- Downloaded certificates are named: `certificate_YourName.png`

## 🎨 Customization Ideas

- Use dark colored text on light templates
- Position names to align with pre-designed text areas
- Typical Y positions: 350-500 for standard certificates
- Font sizes: 50-70 work well for most templates

## 🐛 Troubleshooting

**Template not showing:**
- Ensure the image file is PNG or JPG format
- Check file isn't corrupted

**Font looks different:**
- App tries to use Arial, DejaVu Sans, then defaults
- Font availability depends on your system

**Name not found:**
- Verify spelling matches participant list exactly
- Check if admin has added the participant

**Settings not saving:**
- Ensure you click "💾 Save All Settings" button
- Check write permissions in app directory

## 📋 Requirements

- Python 3.7+
- streamlit 1.31.0
- Pillow 10.2.0

## 🤝 Contributing

Feel free to fork this project and customize it for your needs!

## 📄 License

This project is open source and available for personal and commercial use.

## 📧 Support

For issues or questions, please contact your event administrator.

---

**Made with ❤️ using Streamlit**
