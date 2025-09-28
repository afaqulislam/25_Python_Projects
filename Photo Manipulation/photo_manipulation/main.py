import cv2
import numpy as np

# Load image
image = cv2.imread("sample.jpg")
if image is None:
    print("Image not found.")
    exit()

image = cv2.resize(image, (600, 400))
cv2.namedWindow("Image Manipulation")


# Trackbars
def nothing(x):
    pass


cv2.createTrackbar("Brightness", "Image Manipulation", 50, 100, nothing)
cv2.createTrackbar("Contrast", "Image Manipulation", 50, 100, nothing)
cv2.createTrackbar("Blur", "Image Manipulation", 0, 20, nothing)

# Mode: 0 = normal, 1 = grayscale, 2 = sepia, 3 = edge
mode = 0

print("\n🎮 Keyboard Controls:")
print("  G: Grayscale")
print("  S: Sepia")
print("  E: Edge Detection")
print("  N: Normal View")
print("  W: Save Image")
print("  ESC: Exit\n")

while True:
    edited = image.copy()

    # Get trackbar values
    brightness = cv2.getTrackbarPos("Brightness", "Image Manipulation") - 50
    contrast = cv2.getTrackbarPos("Contrast", "Image Manipulation") / 50
    blur_val = cv2.getTrackbarPos("Blur", "Image Manipulation")

    # Brightness & Contrast
    edited = cv2.convertScaleAbs(edited, alpha=contrast, beta=brightness * 2)

    # Blur
    if blur_val % 2 == 0:
        blur_val += 1
    if blur_val > 1:
        edited = cv2.GaussianBlur(edited, (blur_val, blur_val), 0)

    # Mode filters
    if mode == 1:  # Grayscale
        edited = cv2.cvtColor(edited, cv2.COLOR_BGR2GRAY)
    elif mode == 2:  # Sepia
        kernel = np.array(
            [[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]
        )
        edited = cv2.transform(edited, kernel)
        edited = np.clip(edited, 0, 255).astype(np.uint8)
    elif mode == 3:  # Edge Detection
        edited = cv2.Canny(edited, 100, 200)

    # Display image
    window_name = ["Normal", "Grayscale", "Sepia", "Edge Detection"][mode]
    cv2.imshow("Image Manipulation", edited)
    cv2.setWindowTitle("Image Manipulation", f"Image Manipulation - {window_name}")

    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC to exit
        break
    elif key == ord("g"):
        mode = 1
    elif key == ord("s"):
        mode = 2
    elif key == ord("e"):
        mode = 3
    elif key == ord("n"):
        mode = 0
    elif key == ord("w"):
        filename = f"output_{window_name.lower().replace(' ', '_')}.jpg"
        cv2.imwrite(filename, edited)
        print(f"✅ Image saved as {filename}")

cv2.destroyAllWindows()
