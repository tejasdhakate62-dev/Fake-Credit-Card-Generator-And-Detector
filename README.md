# SecurScan AI™ - Fake Credit Card Generator & Detector Suite

SecurScan AI™ is a modern, cyberpunk-themed web application designed to validate and generate synthetic test credit credentials. It combines a robust Flask-based math validation backend with an interactive client-side WASM OCR scanner, a persistent local credential vault, and immersive 3D physics mockups.

---

## 🌟 Key Features

### 1. Immersive 3D Credit Card Physics
- **Dynamic Tilt Parallax**: Hovering over the card applies smooth X- and Y-axis rotation based on cursor coordinates.
- **Flip Interaction**: Flips 180 degrees on click (or via a dedicated manual button) to showcase signature strips, CVVs, and magnetic bands on the back.
- **Flat Premium Layout**: Sleek, flat-black aesthetic featuring a custom Bank Name logo, gold chip lines, contactless waves, and network badge indicators.
- **Viewport Fluidity**: Optimized using CSS Container Query width units (`cqw`), allowing all fonts, card padding, and chip ratios to scale down proportionally on mobile viewports.

### 2. Multi-Network Validator & Luhn Calculator
- **Backend Validation (`/validate`)**: Analyzes card digit strings against network prefix rules and runs the Luhn algorithm to check checksum integrity.
- **Generator Engine (`/generate`)**: Dynamically computes correct check digits using network matching profiles to generate mathematically valid test credentials.
- **7 Major Networks Supported**: Visa, Mastercard, American Express, Discover, Diners Club, JCB, and RuPay.

### 3. Dynamic Credentials & API Integration
- **Infinite Unique Names**: Integrates with the public **RandomUser API** to retrieve unique, realistic cardholder names.
- **Massive Offline Dataset**: Falls back to a local combination list of **10,000+ unique name combinations** if the network is offline or times out (1.5s), avoiding repetitive data generation.

### 4. Advanced OCR Scanning & Fallbacks
- **Live Video Scanner**: Recognizes digit strings from video capture feeds.
- **Image Upload Fallback**: Supports loading static images directly into the canvas OCR pipeline if camera access is restricted or origin contexts are insecure.
- **Multi-Pass Regex Parsing**: Uses structured patterns to isolate card sequences, filtering out dates or CVVs from the raw text feed.

### 5. Decrypted Card Vault
- **Local Storage Buffer**: Saves scanned or generated credentials locally inside your browser's `localStorage` cache.
- **Quick-Actions**: Features styled network badges and lets you reload stored credentials back into the active visualizer or delete them instantly.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.x, Flask
- **Frontend**: HTML5, CSS3 (Container Query width metrics), Vanilla Javascript
- **Scanning Library**: Tesseract.js (WASM Client-side OCR)
- **External Integration**: RandomUser API (for cardholder names)

---

## 🚀 Getting Started

### 1. Clone & Navigate
```bash
git clone <your-repository-url>
cd Fake-Credit-Card-Generator-And-Detector
```

### 2. Create Virtual Environment & Install Dependencies
```bash
# Create environment
python -m venv .venv

# Activate environment (Windows)
.\.venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 3. Run the Server
```bash
python app.py
```

### 4. Open in Browser
Open your browser and navigate to:
**`http://localhost:5000`**

---

## ⚠️ Disclaimer
This tool is built strictly for **educational, testing, and system diagnostic purposes**. All generated credit details are synthetic mock numbers that pass Luhn arithmetic checks but contain no financial value.