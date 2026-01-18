"""
Image Detection System
A web-based application for detecting objects in images using YOLOv8.
Features: Object detection, location extraction, description generation.
"""

import os
import uuid
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Import our modules
from detector import Detector
from image_processor import ImageProcessor
from location import LocationExtractor
from description import DescriptionGenerator

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'tif', 'tiff'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
detector = Detector()
image_processor = ImageProcessor()
location_extractor = LocationExtractor()
description_generator = DescriptionGenerator()

# Google Maps API key (optional)
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle image upload and processing"""
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            return redirect(request.url)
            
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return redirect(request.url)
            
        # Validate and save file
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Process the image
            results = process_image(file_path)
            
            # Render results page
            return render_template('results.html', 
                                   results=results, 
                                   image_file=unique_filename,
                                   google_maps_api_key=GOOGLE_MAPS_API_KEY)
    
    # Show upload page
    return render_template('upload.html')


@app.route('/api/detect', methods=['POST'])
def api_detect():
    """API endpoint for programmatic access"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Process the image
        results = process_image(file_path)
        
        return jsonify(results)
    
    return jsonify({'error': 'File type not allowed'}), 400


def process_image(image_path):
    """
    Main image processing function
    This is where the magic happens!
    """
    print(f"Processing image: {image_path}")
    
    # Step 1: Load and preprocess image
    image = image_processor.load_image(image_path)
    if image is None:
        return {'error': 'Could not load image'}
    
    height, width = image.shape[:2]
    
    # Step 2: Detect objects using YOLOv8
    print("Detecting objects...")
    detected_objects = detector.detect_objects(image_path)
    
    # Step 3: Classify image type
    print("Classifying image...")
    image_class = detector.classify_image(detected_objects)
    
    # Step 4: Extract location (if available in metadata)
    print("Extracting location...")
    location_info = location_extractor.extract_location(image_path)
    
    # Step 5: Generate description
    print("Generating description...")
    description = description_generator.generate_description(
        detected_objects, image_class, location_info
    )
    
    # Step 6: Generate tags
    tags = description_generator.generate_tags(
        detected_objects, image_class, location_info
    )
    
    # Step 7: Create annotated image with bounding boxes
    print("Creating visualizations...")
    annotated_image = image_processor.draw_boxes(image, detected_objects)
    
    # Step 8: Create heatmap
    heatmap = image_processor.create_heatmap(image, detected_objects)
    
    # Step 9: Convert images to base64 for web display
    original_img_str = image_processor.image_to_base64(image)
    annotated_img_str = image_processor.image_to_base64(annotated_image)
    heatmap_img_str = image_processor.image_to_base64(heatmap)
    
    # Step 10: Generate Google Maps URL if location available
    maps_url = None
    if location_info and 'latitude' in location_info and 'longitude' in location_info:
        maps_url = location_extractor.generate_maps_url(
            location_info['latitude'], location_info['longitude']
        )
    
    # Prepare results
    results = {
        'objects': detected_objects,
        'classification': image_class,
        'location': location_info,
        'description': description,
        'tags': tags,
        'images': {
            'original': original_img_str,
            'annotated': annotated_img_str,
            'heatmap': heatmap_img_str
        },
        'maps_url': maps_url,
        'dimensions': {'width': width, 'height': height}
    }
    
    print("Processing complete!")
    return results


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Image Detection System")
    print("="*60)
    print("\n✓ Server starting...")
    print("✓ Open your browser: http://localhost:5000")
    print("✓ Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

