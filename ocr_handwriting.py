import cv2
import pytesseract
from PIL import Image
from difflib import SequenceMatcher
import matplotlib.pyplot as plt

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    """Convert image to grayscale and apply thresholding to improve OCR."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 3)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def extract_handwritten_text(image_path):
    """Extract handwritten text from image using Tesseract OCR."""
    preprocessed_img = preprocess_image(image_path)
    pil_img = Image.fromarray(preprocessed_img)
    text = pytesseract.image_to_string(pil_img, lang='eng')
    return text.strip()

def calculate_accuracy(predicted, actual):
    """Calculate and return character-level accuracy (in percentage)."""
    char_accuracy = SequenceMatcher(None, predicted, actual).ratio() * 100
    return round(char_accuracy, 2)

def plot_accuracy_graph(accuracy):
    """Plot a bar chart for character-level accuracy."""
    plt.figure(figsize=(8, 6))  # Set figure size for better readability

    # Plotting the character-level accuracy as a bar chart
    plt.bar(["Character-Level Accuracy"], [accuracy], color='blue')

    # Adding title and labels
    plt.title("OCR Handwritten Text Accuracy")
    plt.ylabel("Accuracy (%)")
    plt.ylim(0, 100)  # Ensure the y-axis is always between 0 and 100%

    # Show the graph
    plt.show()

if __name__ == "__main__":
    # 🔁 Replace with the path to your test image
    image_path = "images/sample.jpg"

    # ✍️ Provide the actual ground truth text for the test image
    ground_truth = """A Quality Product by:
Navneet Education Limited
Reg Off: Navneet Bhavan,
Bhavani Shankar Road, Dadar (West).
Mumbai 400 028, Maharashtra

For Consumer Complaint/Query:
Consumer Care Cell at the above address
Customer Care No.: 022 66626300.
www.youvaworld.com © 2021"""

    print("\n🔍 Extracting handwritten text from image...")
    extracted_text = extract_handwritten_text(image_path)
    print("\n📜 Extracted Text:\n")
    print(extracted_text)

    print("\n📏 Evaluating OCR Accuracy...")
    char_acc = calculate_accuracy(extracted_text, ground_truth)

    print(f"\n✅ Character-Level Accuracy: {char_acc:.2f}%")

    # Plot accuracy graph
    plot_accuracy_graph(char_acc)
