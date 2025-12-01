from flask import Flask, render_template, request, send_file, abort
from PIL import Image
import io
import secrets
import string
import numpy as np
import random

app = Flask(__name__)

def generate_password(length=16):
    """Generate a secure random password"""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def text_to_bits(text):
    """Convert text to binary"""
    return ''.join(format(ord(char), '08b') for char in text)

def bits_to_text(bits):
    """Convert binary to text"""
    return ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))

def generate_pixel_art_image(size=(200, 200)):
    """Generate a colorful pixel art image with random blocks"""
    img = Image.new('RGBA', size, color='white')
    pixels = np.array(img)
    block_sizes = [10, 15, 20]  # Possible block sizes
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (255, 165, 0),  # Orange
        (128, 0, 128)   # Purple
    ]
    
    # Create random blocks of color
    for _ in range(20):  # Generate 20 random blocks
        block_size = random.choice(block_sizes)
        x = random.randint(0, size[0] - block_size)
        y = random.randint(0, size[1] - block_size)
        color = random.choice(colors)
        
        for i in range(x, x + block_size):
            for j in range(y, y + block_size):
                if 0 <= i < size[0] and 0 <= j < size[1]:
                    pixels[j][i] = (  # note: numpy image indexing is [row=y][col=x]
                        color[0],
                        color[1],
                        color[2],
                        255  # Alpha channel
                    )
    
    img = Image.fromarray(pixels.astype(np.uint8))
    return img

def embed_password_in_image(password, size=(200, 200)):
    """Generate a pixel art image and embed the password using LSB steganography"""

    img = generate_pixel_art_image(size)
    pixels = np.array(img).astype(np.uint8)

    # Convert password to binary
    binary_password = text_to_bits(password) + '1111111111111110'  # delimiter

    required_bits = len(binary_password)
    available_bits = pixels.size  # 4 channels included automatically

    if required_bits > available_bits:
        raise ValueError("Password is too long to embed in the image")

    data_index = 0
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            for k in range(pixels.shape[2]):
                if data_index < required_bits:
                    
                    # FIX: ensure operations do not produce negative numbers
                    base_value = int(pixels[i][j][k])
                    new_value = (base_value // 2) * 2 + int(binary_password[data_index])
                    new_value = max(0, min(255, new_value))  # clamp 0–255
                    
                    pixels[i][j][k] = new_value
                    data_index += 1
                else:
                    break
            if data_index >= required_bits:
                break
        if data_index >= required_bits:
            break

    img = Image.fromarray(pixels.astype(np.uint8))

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

    return img_byte_arr

def extract_password_from_image(image):
    """Extract password from an image"""
    img = Image.open(image)
    pixels = np.array(img)
    binary_data = []
    
    for row in range(pixels.shape[0]):
        for col in range(pixels.shape[1]):
            for ch in range(pixels.shape[2]):
                binary_data.append(pixels[row][col][ch] & 1)
    
    binary_str = ''.join(str(bit) for bit in binary_data)
    delimiter = '1111111111111110'
    if delimiter not in binary_str:
        return ''
    password_binary = binary_str.split(delimiter)[0]
    password = bits_to_text(password_binary)
    return password

@app.route('/', methods=['GET', 'POST'])
def index():
    password = ''
    if request.method == 'POST':
        # Auto-generate password using the length provided
        try:
            length = int(request.form.get('length', 16))
            length = max(1, min(length, 100))  # clamp length
        except ValueError:
            length = 16
        password = generate_password(length)
    return render_template('index.html', password=password)

@app.route('/custom-input', methods=['POST'])
def custom_input():
    """Accept custom password and render index with that password so /image can generate it"""
    password = request.form.get('custom_password', '').strip()
    if not password:
        return render_template('index.html', password='', error="Custom password cannot be empty.")
    # Quick capacity check: attempt to embed to ensure it fits (using default image size)
    try:
        _ = embed_password_in_image(password)  # we discard result; this checks capacity/possible errors
    except Exception as e:
        return render_template('index.html', password='', error=f"Cannot embed password: {str(e)}")
    return render_template('index.html', password=password)

@app.route('/image')
def get_image():
    password = request.args.get('password', '')
    if password == '':
        return abort(400, description="Missing password parameter")
    try:
        image_data = embed_password_in_image(password)
        return send_file(image_data, mimetype='image/png')
    except Exception as e:
        return f"Error generating image: {str(e)}", 500

@app.route('/decode', methods=['GET', 'POST'])
def decode():
    extracted_password = ''
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('decode.html', error='No image uploaded')
        image_file = request.files['image']
        try:
            img_data = image_file.read()
            extracted_password = extract_password_from_image(io.BytesIO(img_data))
            if extracted_password == '':
                return render_template('decode.html', error='No embedded password found or wrong delimiter.')
        except Exception as e:
            return render_template('decode.html', error=f"Error: {str(e)}")
    return render_template('decode.html', password=extracted_password)

if __name__ == '__main__':
    app.run(debug=True)
