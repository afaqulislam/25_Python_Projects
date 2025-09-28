# Enhanced QR Code Tool

A powerful Streamlit application for generating and scanning QR codes with advanced customization and detection capabilities.

![QR Code Tool](https://hebbkx1anhila5yf.public.blob.vercel-storage.com/placeholder-ob7miW3mUreePYfXdVwkpFWHthzoR5.svg?height=300&width=600)

## Features

### QR Code Generator
- Create QR codes from text or URLs
- Automatic URL shortening for long URLs
- Customization options:
  - Size adjustment
  - Error correction level selection (Low 7%, Medium 15%, Quartile 25%, High 30%)
  - Custom foreground and background colors
  - Adjustable border size
- Real-time preview
- One-click download

### QR Code Scanner
- Upload and scan QR code images
- Advanced image preprocessing options:
  - Auto detection (tries all methods)
  - Contrast enhancement
  - Image sharpening
  - Basic and adaptive thresholding
  - Edge detection
  - Morphological operations
- Intelligent detection strategies:
  - Multiple rotation angles
  - Various scaling factors
  - Debug visualization
- Special content parsing:
  - URL detection with direct links
  - vCard contact information extraction
  - WiFi network configuration details

## Installation

\`\`\`bash
# Clone the repository
git clone https://github.com/yourusername/enhanced-qr-code-tool.git
cd enhanced-qr-code-tool

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
\`\`\`

## Requirements

- Python 3.7+
- Streamlit
- qrcode
- Pillow (PIL)
- OpenCV (cv2)
- NumPy
- Requests

## Usage

### Generating QR Codes

1. Enter text or URL in the input field
2. Customize your QR code using the available options
3. Click "Generate QR Code"
4. Download the generated QR code using the download button

### Scanning QR Codes

1. Upload a QR code image using the file uploader
2. Select preprocessing methods based on image quality
3. Enable additional detection options if needed
4. View the decoded content and any special formatting

## Tips for Better Scanning

- Ensure the QR code is well-lit and in focus
- Make sure all corners of the QR code are visible
- Try different preprocessing methods for difficult images:
  - Enhance Contrast works well for low-contrast images
  - Threshold works well for clear, high-contrast images
  - Adaptive Threshold works well for unevenly lit images
  - Edge Detection can help with complex backgrounds

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [qrcode](https://github.com/lincolnloop/python-qrcode) for QR code generation
- [OpenCV](https://opencv.org/) for image processing and QR detection

## 🙋‍♂️ Author

**Afaq Ul Islam**  
Full Stack Developer | Python Developer | Tech Enthusiast

- 🌐 Portfolio: [Afaq Ul Islam](https://aui-portfolio.vercel.app/)
- 💼 LinkedIn: [Afaq Ul Islam](https://www.linkedin.com/in/afaqulislam/)
- 🐙 GitHub: [Afaq Ul Islam](https://github.com/afaqulislam)


## 💬 Feedback

If you find bugs or want to suggest features, feel free to open an issue or submit a pull request. Contributions are welcome!