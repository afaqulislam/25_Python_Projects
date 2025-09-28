import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from datetime import datetime
import io
import base64
import cv2
import numpy as np
import re
import requests
from io import BytesIO

# Page configuration
st.set_page_config(page_title="Enhanced QR Code Tool", page_icon="📱", layout="wide")

# Simple header
st.title("QR Code Generator and Scanner")

# Tabs for Generator and Scanner
tab1, tab2 = st.tabs(["Generate QR Code", "Scan QR Code"])

# QR Code Generator Tab
with tab1:
    col1, col2 = st.columns([3, 2])

    with col1:
        # QR code content with character counter
        qr_data = st.text_area(
            "Enter text or URL", placeholder="https://example.com", height=100
        )
        char_count = len(qr_data)
        st.caption(
            f"Character count: {char_count} (Recommended: keep under 300 for best results)"
        )

        # URL shortening option
        if (
            qr_data
            and char_count > 100
            and (qr_data.startswith("http://") or qr_data.startswith("https://"))
        ):
            if st.checkbox("Shorten URL to improve QR code readability"):
                try:
                    # Using TinyURL API for URL shortening
                    tiny_url_api = f"https://tinyurl.com/api-create.php?url={qr_data}"
                    shortened_url = requests.get(tiny_url_api).text
                    if shortened_url and shortened_url.startswith("https://"):
                        qr_data = shortened_url
                        st.success(f"URL shortened to: {shortened_url}")
                except:
                    st.warning("Could not shorten URL. Using original URL.")

        # QR code customization options
        st.subheader("Customization")

        col_a, col_b = st.columns(2)

        with col_a:
            # QR code size
            qr_size = st.slider("QR Code Size", 100, 500, 300, 20)

            # Error correction level
            error_correction_options = {
                "Low (7%)": qrcode.constants.ERROR_CORRECT_L,
                "Medium (15%)": qrcode.constants.ERROR_CORRECT_M,
                "Quartile (25%)": qrcode.constants.ERROR_CORRECT_Q,
                "High (30%)": qrcode.constants.ERROR_CORRECT_H,
            }
            error_level = st.selectbox(
                "Error Correction Level",
                list(error_correction_options.keys()),
                index=1,
                help="Higher levels make QR code more resistant to damage but increase size",
            )

        with col_b:
            # QR code colors
            fg_color = st.color_picker("Foreground Color", "#000000")
            bg_color = st.color_picker("Background Color", "#FFFFFF")

            # Border size
            border_size = st.slider("Border Size", 0, 10, 4)

    with col2:
        # Preview area
        st.subheader("Preview")
        preview_placeholder = st.empty()

        # Generate button
        if st.button("Generate QR Code", type="primary") and qr_data:
            try:
                # Create QR code with selected options
                qr = qrcode.QRCode(
                    version=1,  # Auto-fit
                    error_correction=error_correction_options[error_level],
                    box_size=10,
                    border=border_size,
                )

                # Add data
                qr.add_data(qr_data)

                # Make QR code
                try:
                    qr.make(fit=True)
                except qrcode.exceptions.DataOverflowError:
                    st.error(
                        "The data is too large for a QR code. Please reduce the text or use URL shortening."
                    )
                    st.stop()

                # Generate QR code image with custom colors
                qr_img = qr.make_image(
                    fill_color=fg_color, back_color=bg_color
                ).convert("RGB")

                # Resize to requested size
                qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)

                # Display the QR code - FIXED: use_container_width instead of use_column_width
                preview_placeholder.image(
                    qr_img, caption="Generated QR Code", use_container_width=True
                )

                # Convert image to bytes for download
                img_byte_arr = io.BytesIO()
                qr_img.save(img_byte_arr, format="PNG")
                img_byte_arr.seek(0)

                # Create download button
                st.download_button(
                    label="Download QR Code",
                    data=img_byte_arr.getvalue(),
                    file_name="qrcode.png",
                    mime="image/png",
                )

                # Show encoded data
                with st.expander("QR Code Information"):
                    st.write(f"**Data encoded:** {qr_data}")
                    st.write(f"**QR Version:** {qr.version} (of 40)")
                    st.write(f"**Error Correction:** {error_level}")
                    st.write(
                        f"**Module Count:** {17 + 4 * qr.version} × {17 + 4 * qr.version}"
                    )

            except ValueError as e:
                if "Invalid version" in str(e):
                    st.error(
                        "The text is too long for a QR code. Please enter less text or use URL shortening."
                    )
                else:
                    st.error(f"Error generating QR code: {e}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            # Show placeholder image
            placeholder_img = Image.new("RGB", (qr_size, qr_size), color=bg_color)
            draw = ImageDraw.Draw(placeholder_img)
            draw.text((qr_size // 2 - 60, qr_size // 2), "QR Preview", fill=fg_color)
            preview_placeholder.image(
                placeholder_img, caption="QR Preview", use_container_width=True
            )

# QR Code Scanner Tab
with tab2:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Upload QR Code")
        uploaded_qr = st.file_uploader(
            "Upload QR Code Image", type=["png", "jpg", "jpeg"]
        )

        # Advanced scanning options
        scan_options = st.expander("Advanced Scanning Options", expanded=True)
        with scan_options:
            # Image preprocessing options
            st.subheader("Image Preprocessing")

            preprocessing_method = st.selectbox(
                "Preprocessing Method",
                [
                    "Auto (Try All)",
                    "None",
                    "Enhance Contrast",
                    "Sharpen",
                    "Threshold",
                    "Adaptive Threshold",
                    "Edge Detection",
                    "Morphological Operations",
                ],
            )

            # Show specific options based on selected preprocessing
            if preprocessing_method in ["Auto (Try All)", "Enhance Contrast"]:
                contrast_factor = st.slider("Contrast Factor", 1.0, 3.0, 1.5, 0.1)

            if preprocessing_method in ["Auto (Try All)", "Sharpen"]:
                sharpen_factor = st.slider("Sharpen Factor", 1.0, 5.0, 2.0, 0.1)

            if preprocessing_method in ["Auto (Try All)", "Threshold"]:
                threshold_value = st.slider("Threshold Value", 0, 255, 127, 1)

            if preprocessing_method in ["Auto (Try All)", "Adaptive Threshold"]:
                block_size = st.slider("Block Size (must be odd)", 3, 51, 11, 2)
                if block_size % 2 == 0:  # Ensure block size is odd
                    block_size += 1

            if preprocessing_method in ["Auto (Try All)", "Morphological Operations"]:
                kernel_size = st.slider("Kernel Size", 1, 9, 5, 2)

            # Detection options
            st.subheader("Detection Options")

            try_rotations = st.checkbox(
                "Try different rotations",
                value=True,
                help="Tries to detect QR codes at different angles",
            )

            try_multiple_scales = st.checkbox(
                "Try different scales",
                value=True,
                help="Tries to detect QR codes at different sizes",
            )

            show_debug_images = st.checkbox(
                "Show debug images",
                value=False,
                help="Shows the preprocessed images used for detection",
            )

    with col2:
        if uploaded_qr:
            st.subheader("Scanning Results")

            # Display the uploaded image
            image = Image.open(uploaded_qr)
            st.image(image, caption="Uploaded QR Code", width=300)

            # Scanning status
            with st.spinner("Scanning QR code..."):
                # Convert to numpy array for OpenCV
                image_np = np.array(image)

                # Results container
                results = []
                debug_images = []

                # Helper function to try QR detection on an image
                def try_detect_qr(img, label=""):
                    try:
                        # Create QR code detector
                        qr_detector = cv2.QRCodeDetector()
                        data, bbox, _ = qr_detector.detectAndDecode(img)
                        if data:
                            if data not in results:  # Avoid duplicates
                                results.append(data)
                            return True
                        return False
                    except Exception as e:
                        st.warning(f"Detection error with {label}: {str(e)}")
                        return False

                # Helper function to add debug image
                def add_debug_image(img, title):
                    if show_debug_images:
                        # Convert to PIL for display
                        if len(img.shape) == 2:  # Grayscale
                            pil_img = Image.fromarray(img)
                        else:  # Color
                            pil_img = Image.fromarray(
                                cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            )
                        debug_images.append((pil_img, title))

                # Convert to grayscale if needed
                if len(image_np.shape) == 3 and image_np.shape[2] == 3:
                    color_img = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
                    gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
                else:
                    gray = image_np
                    color_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

                add_debug_image(gray, "Original Grayscale")

                # Try original image first
                if try_detect_qr(color_img, "Original Color"):
                    st.success("QR code detected in original image!")

                if not results:
                    try_detect_qr(gray, "Original Grayscale")

                # Apply selected preprocessing or try all if Auto is selected
                preprocess_methods = []

                if (
                    preprocessing_method == "Auto (Try All)"
                    or preprocessing_method == "Enhance Contrast"
                ):
                    # Enhance contrast with PIL
                    pil_img = Image.fromarray(gray)
                    enhanced = ImageEnhance.Contrast(pil_img).enhance(contrast_factor)
                    enhanced_np = np.array(enhanced)
                    add_debug_image(
                        enhanced_np, f"Enhanced Contrast ({contrast_factor}x)"
                    )
                    preprocess_methods.append((enhanced_np, "Enhanced Contrast"))

                if (
                    preprocessing_method == "Auto (Try All)"
                    or preprocessing_method == "Sharpen"
                ):
                    # Sharpen with PIL
                    pil_img = Image.fromarray(gray)
                    sharpened = pil_img.filter(
                        ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3)
                    )
                    sharpened_np = np.array(sharpened)
                    add_debug_image(sharpened_np, f"Sharpened")
                    preprocess_methods.append((sharpened_np, "Sharpened"))

                if (
                    preprocessing_method == "Auto (Try All)"
                    or preprocessing_method == "Threshold"
                ):
                    # Basic thresholding
                    _, thresh = cv2.threshold(
                        gray, threshold_value, 255, cv2.THRESH_BINARY
                    )
                    add_debug_image(thresh, f"Threshold ({threshold_value})")
                    preprocess_methods.append((thresh, "Threshold"))

                    # Inverse threshold might help with inverted QR codes
                    _, thresh_inv = cv2.threshold(
                        gray, threshold_value, 255, cv2.THRESH_BINARY_INV
                    )
                    add_debug_image(
                        thresh_inv, f"Inverse Threshold ({threshold_value})"
                    )
                    preprocess_methods.append((thresh_inv, "Inverse Threshold"))

                if (
                    preprocessing_method == "Auto (Try All)"
                    or preprocessing_method == "Adaptive Threshold"
                ):
                    # Adaptive thresholding
                    adapt_thresh = cv2.adaptiveThreshold(
                        gray,
                        255,
                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                        cv2.THRESH_BINARY,
                        block_size,
                        2,
                    )
                    add_debug_image(
                        adapt_thresh, f"Adaptive Threshold (block={block_size})"
                    )
                    preprocess_methods.append((adapt_thresh, "Adaptive Threshold"))

                    # Inverse adaptive threshold
                    adapt_thresh_inv = cv2.adaptiveThreshold(
                        gray,
                        255,
                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                        cv2.THRESH_BINARY_INV,
                        block_size,
                        2,
                    )
                    add_debug_image(
                        adapt_thresh_inv,
                        f"Inverse Adaptive Threshold (block={block_size})",
                    )
                    preprocess_methods.append(
                        (adapt_thresh_inv, "Inverse Adaptive Threshold")
                    )

                if (
                    preprocessing_method == "Auto (Try All)"
                    or preprocessing_method == "Edge Detection"
                ):
                    # Edge detection
                    edges = cv2.Canny(gray, 100, 200)
                    add_debug_image(edges, "Edge Detection")
                    preprocess_methods.append((edges, "Edge Detection"))

                if (
                    preprocessing_method == "Auto (Try All)"
                    or preprocessing_method == "Morphological Operations"
                ):
                    # Morphological operations
                    kernel = np.ones((kernel_size, kernel_size), np.uint8)

                    # Dilation followed by erosion (closing) - helps connect broken parts
                    closing = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
                    add_debug_image(closing, f"Closing (kernel={kernel_size})")
                    preprocess_methods.append((closing, "Closing"))

                    # Erosion followed by dilation (opening) - helps remove noise
                    opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
                    add_debug_image(opening, f"Opening (kernel={kernel_size})")
                    preprocess_methods.append((opening, "Opening"))

                # Try each preprocessing method
                for img, label in preprocess_methods:
                    if try_detect_qr(img, label):
                        st.success(f"QR code detected with {label} preprocessing!")
                        if len(results) >= 1:  # If we found at least one, we can stop
                            break

                # If still no results and rotations are enabled, try rotating the image
                if not results and try_rotations:
                    st.info("Trying different rotations...")
                    angles = [90, 180, 270]  # Try 90, 180, and 270 degrees

                    for angle in angles:
                        # Rotate with OpenCV
                        height, width = gray.shape[:2]
                        center = (width / 2, height / 2)
                        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
                        rotated = cv2.warpAffine(gray, rotation_matrix, (width, height))
                        add_debug_image(rotated, f"Rotated {angle}°")

                        if try_detect_qr(rotated, f"Rotated {angle}°"):
                            st.success(f"QR code detected after rotating {angle}°!")
                            break

                # If still no results and multiple scales are enabled, try resizing the image
                if not results and try_multiple_scales:
                    st.info("Trying different scales...")
                    scales = [0.5, 1.5, 2.0]  # Try 50%, 150%, and 200% scaling

                    for scale in scales:
                        # Resize with OpenCV
                        width = int(gray.shape[1] * scale)
                        height = int(gray.shape[0] * scale)
                        resized = cv2.resize(
                            gray, (width, height), interpolation=cv2.INTER_CUBIC
                        )
                        add_debug_image(resized, f"Scaled {scale}x")

                        if try_detect_qr(resized, f"Scaled {scale}x"):
                            st.success(f"QR code detected after scaling {scale}x!")
                            break

                # Display debug images if enabled
                if show_debug_images and debug_images:
                    st.subheader("Debug Images")
                    cols = st.columns(2)
                    for i, (img, title) in enumerate(debug_images):
                        # FIXED: use_container_width instead of use_column_width
                        cols[i % 2].image(img, caption=title, use_container_width=True)

                # Display results
                if results:
                    st.success(f"Found {len(results)} QR code(s)!")

                    for i, data in enumerate(results):
                        with st.expander(f"QR Code {i+1} Content", expanded=True):
                            st.code(data)

                            # Check if it's a URL and provide a button to open it
                            if re.match(r"^https?://", data):
                                st.markdown(f"[Open URL]({data})")

                            # Check if it's a vCard
                            elif data.startswith("BEGIN:VCARD") and data.endswith(
                                "END:VCARD"
                            ):
                                st.write("**vCard Detected:**")
                                # Extract name
                                name_match = re.search(r"FN:(.*?)(?:\r?\n|$)", data)
                                if name_match:
                                    st.write(f"Name: {name_match.group(1)}")
                                # Extract email
                                email_match = re.search(r"EMAIL:(.*?)(?:\r?\n|$)", data)
                                if email_match:
                                    st.write(f"Email: {email_match.group(1)}")
                                # Extract phone
                                phone_match = re.search(r"TEL:(.*?)(?:\r?\n|$)", data)
                                if phone_match:
                                    st.write(f"Phone: {phone_match.group(1)}")

                            # Check if it's a WiFi config
                            elif "WIFI:" in data:
                                st.write("**WiFi Network Detected:**")
                                # Extract SSID
                                ssid_match = re.search(r"S:(.*?);", data)
                                if ssid_match:
                                    st.write(f"Network Name: {ssid_match.group(1)}")
                                # Extract password
                                pw_match = re.search(r"P:(.*?);", data)
                                if pw_match:
                                    st.write(f"Password: {pw_match.group(1)}")
                                # Extract encryption type
                                type_match = re.search(r"T:(.*?);", data)
                                if type_match:
                                    st.write(f"Encryption: {type_match.group(1)}")
                else:
                    st.error(
                        "No QR code detected. Try different preprocessing options."
                    )

                    # Offer suggestions
                    st.info("Tips for better scanning:")
                    st.markdown(
                        """
                    1. **Try different preprocessing methods:**
                       - Enhance Contrast works well for low-contrast images
                       - Threshold works well for clear, high-contrast images
                       - Adaptive Threshold works well for unevenly lit images
                       - Edge Detection can help with complex backgrounds
                    
                    2. **Image quality tips:**
                       - Make sure the QR code is well-lit and in focus
                       - Ensure all corners of the QR code are visible
                       - Try a different image format or higher resolution
                       - Remove any glare or shadows from the image
                    
                    3. **Advanced options:**
                       - Enable "Try different rotations" if your QR code might be sideways
                       - Enable "Try different scales" if your QR code is very small or large
                       - Enable "Show debug images" to see how preprocessing affects your image
                    """
                    )
        else:
            # Show instructions when no image is uploaded
            st.info("Upload a QR code image to scan")
            st.markdown(
                """
            **Supported formats:**
            - PNG
            - JPG/JPEG
            
            For best results, ensure the QR code is:
            - Clear and not blurry
            - Well-lit
            - Completely visible in the image
            """
            )

# Clean, professional footer with Linktree icon
current_year = datetime.now().year

st.markdown("---")
st.markdown(
    f"""
    <style>
        .footer {{
            text-align: center;
            color: #5f6368;
            font-size: 0.85rem;
            padding: 15px 0;
        }}
        .footer-content {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }}
        .footer a {{
            color: #3949ab;
            text-decoration: none;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }}
        .footer a:hover {{
            color: #1a237e;
        }}
        .footer-divider {{
            width: 30px;
            height: 1px;
            background-color: #e0e0e0;
            margin: 5px auto;
        }}
        .linktree-icon {{
            width: 14px;
            height: 14px;
            fill: currentColor;
        }}
    </style>
    <div class='footer'>
        <div class='footer-content'>
            <div>🔳 QR Code Generator and Scanner</div>
            <div class='footer-divider'></div>
            <div>
                Copyright © {current_year} 
                <a href="https://linktr.ee/afaqulislam" target="_blank" rel="noopener noreferrer">
                    <svg class="linktree-icon" viewBox="0 0 24 24">
                        <path d="M12 1.5a.5.5 0 01.5.5v6.5l4.5-4.5a.5.5 0 01.7.7L13 9.5h6.5a.5.5 0 010 1H13l4.7 4.8a.5.5 0 01-.7.7L12 11.5 7.3 16a.5.5 0 01-.7-.7l4.7-4.8H4.5a.5.5 0 010-1H11L6.3 4.7a.5.5 0 01.7-.7l4.5 4.5V2a.5.5 0 01.5-.5zm0 13a.5.5 0 01.5.5v7a.5.5 0 01-1 0v-7a.5.5 0 01.5-.5z"/>
                    </svg>
                    Afaq Ul Islam
                </a>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
