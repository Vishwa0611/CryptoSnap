# Password Generator with Image Steganography

A Flask-based web application that generates secure passwords and embeds them into colorful pixel art images using LSB (Least Significant Bit) steganography.

## Features

- **Secure Password Generation**: Generate cryptographically secure random passwords with customizable length
- **Pixel Art Image Embedding**: Automatically embed passwords into colorful pixel art images
- **Image Steganography**: Use LSB steganography to hide passwords in PNG images
- **Password Extraction**: Upload images to extract hidden passwords
- **Modern UI**: Clean, responsive web interface with smooth animations
- **Download & Share**: Download generated images or copy shareable links

## How It Works

### Password Generation
- Uses Python's `secrets` module for cryptographically secure random generation
- Supports passwords with letters, digits, and punctuation characters
- Customizable password length (8-100 characters)

### Image Steganography
- Generates colorful pixel art backgrounds with random color blocks
- Embeds password data using LSB (Least Significant Bit) technique in RGBA channels
- Uses a 16-bit delimiter (`1111111111111110`) to mark the end of password data
- Ensures data integrity with proper error handling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/CryptoSnap.git
cd CryptoSnap
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Generate a password:
   - Enter desired password length
   - Click "Generate Password"
   - Download the image or copy the shareable link

4. Extract a password:
   - Navigate to the decode page
   - Upload an image containing an embedded password
   - View the extracted password

## Project Structure

```
password-generator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── static/
│    └── css/
│       └── style.css     # Styling and animations
└── templates/
    ├── index.html        # Main password generation page
    └── decode.html       # Password extraction page
```

## API Endpoints

- `GET /` - Main application interface
- `POST /` - Generate password and embed in image
- `GET /image?password=<password>` - Generate image with embedded password
- `GET /decode` - Password extraction interface
- `POST /decode` - Extract password from uploaded image

## Technologies Used

- **Backend**: Flask 3.1.1
- **Image Processing**: Pillow 11.2.1
- **Numerical Computing**: NumPy 2.3.1
- **Frontend**: HTML5, CSS3, JavaScript
- **Security**: Python secrets module

## Security Considerations

- Uses cryptographically secure random number generation
- Passwords are never stored on the server
- All image processing happens in memory
- Secure handling of file uploads with validation

## Limitations

- Maximum password length depends on image dimensions (currently 200x200 pixels)
- Only PNG format is supported for embedding/extraction
- Image compression may affect password extraction

## Contributing

Feel free to submit issues and enhancement requests!

## License


This project is open source and available under the [MIT License](LICENSE).
