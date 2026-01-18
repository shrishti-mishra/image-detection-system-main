# Getting Started Guide - Image Detection System

Welcome! This guide will help you understand and set up the Image Detection System from scratch, even if you're a complete beginner.

## 📚 Table of Contents
1. [What is This Project?](#what-is-this-project)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Understanding the Project Structure](#understanding-the-project-structure)
5. [Running the Application](#running-the-application)
6. [How It Works](#how-it-works)
7. [Troubleshooting](#troubleshooting)

---

## What is This Project?

This is an **Image Detection System** that can:
- Upload and analyze images (satellite images, regular photos, etc.)
- Detect objects in images (buildings, vehicles, people, etc.)
- Classify the type of image (urban area, landscape, etc.)
- Extract location information from image metadata
- Generate descriptions and tags for images
- Display results with visual annotations

**Think of it as:** A smart image analyzer that can tell you what's in a picture and where it might be from!

---

## Prerequisites

Before you start, you need:

1. **Python 3.8 or higher** installed on your computer
   - Check if you have Python: Open Command Prompt (Windows) or Terminal (Mac/Linux) and type:
     ```
     python --version
     ```
   - If you don't have Python, download it from: https://www.python.org/downloads/

2. **Basic understanding of:**
   - How to use Command Prompt/Terminal
   - How to navigate folders
   - Basic file operations

---

## Step-by-Step Setup

### Step 1: Navigate to the Project Folder

1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
2. Navigate to the project folder:
   ```bash
   cd "C:\Users\kumar\Downloads\image-detection-system-main\image-detection-system-main\project"
   ```
   *(Adjust the path based on where you saved the project)*

### Step 2: Create a Virtual Environment

A virtual environment keeps your project's dependencies separate from other Python projects.

**Windows:**
```bash
python -m venv venv
```

**Mac/Linux:**
```bash
python3 -m venv venv
```

This creates a folder called `venv` in your project directory.

### Step 3: Activate the Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command line, indicating the virtual environment is active.

### Step 4: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- OpenCV (image processing)
- Pillow (image handling)
- NumPy (numerical operations)
- And other necessary libraries

**Note:** This may take a few minutes. Be patient!

### Step 5: Create Required Folders

The application needs these folders to store uploaded images:

```bash
# Windows PowerShell
New-Item -ItemType Directory -Force -Path "static\uploads"
New-Item -ItemType Directory -Force -Path "uploads"
```

Or manually create:
- `static/uploads/` folder
- `uploads/` folder (at project root)

### Step 6: (Optional) Set Up Google Maps API Key

If you want location features to work better:

1. Get a Google Maps API key from: https://developers.google.com/maps/documentation/javascript/get-api-key
2. Create a file named `.env` in the project folder
3. Add this line to `.env`:
   ```
   GOOGLE_MAPS_API_KEY=your_api_key_here
   ```

**Note:** This is optional. The app will work without it, but location features may be limited.

---

## Understanding the Project Structure

Here's what each file and folder does:

```
project/
│
├── app.py                 # 🎯 MAIN FILE - Start here! Flask web application
├── api.py                 # API endpoints for programmatic access
├── requirements.txt       # List of all Python packages needed
├── README.md             # Project documentation
│
├── detector.py           # Object detection logic (uses ML models)
├── demo.py               # Demo/fallback version (works without ML models)
├── image_processor.py    # Image processing and visualization
├── location.py           # Location extraction from image metadata
├── description.py        # Generates descriptions and tags
│
├── templates/            # HTML templates for web interface
│   ├── index.html        # Home page
│   ├── upload.html       # Image upload page
│   └── results.html      # Results display page
│
├── static/               # Static files (CSS, JavaScript, images)
│   ├── css/
│   │   └── style.css     # Website styling
│   ├── js/
│   │   └── main.js       # Website JavaScript
│   └── uploads/          # Folder for uploaded images
│
├── uploads/              # Another folder for uploaded images
├── scripts/              # Utility scripts
│   └── create_ppt.py    # Script to create PowerPoint presentations
│
└── test.py               # Unit tests for the system
```

### Key Files Explained:

1. **app.py** - This is the heart of the application. It:
   - Creates the web server
   - Handles image uploads
   - Processes images
   - Displays results

2. **detector.py** - Contains the object detection logic. If ML models aren't available, it falls back to `demo.py`.

3. **demo.py** - A simplified version that works without heavy ML models. Good for testing!

4. **image_processor.py** - Handles all image operations like:
   - Loading images
   - Drawing bounding boxes
   - Creating heatmaps
   - Converting images to web format

5. **location.py** - Extracts GPS coordinates from image metadata and converts them to location names.

6. **description.py** - Generates human-readable descriptions and tags based on detected objects.

---

## Running the Application

### Method 1: Using app.py (Main Application)

1. Make sure your virtual environment is activated (you should see `(venv)` in your terminal)

2. Run the application:
   ```bash
   python app.py
   ```

3. You should see output like:
   ```
   * Running on http://127.0.0.1:5000
   * Debug mode: on
   ```

4. Open your web browser and go to:
   ```
   http://localhost:5000
   ```

5. You should see the Image Detection System homepage!

### Method 2: Using demo.py (For Testing)

If you want to test without the full web interface:

```bash
python demo.py path/to/your/image.jpg
```

This will process an image and show results in the terminal.

---

## How It Works

### The Flow:

1. **User uploads an image** → Image is saved to `static/uploads/` folder

2. **Image Processing** → `image_processor.py` loads and preprocesses the image

3. **Object Detection** → `detector.py` (or `demo.py`) analyzes the image to find objects:
   - Buildings
   - Vehicles
   - People
   - Roads
   - And more!

4. **Image Classification** → The system determines what type of image it is:
   - Urban area
   - Landscape
   - Satellite image
   - etc.

5. **Location Extraction** → `location.py` tries to find location information:
   - From GPS data in image metadata (EXIF)
   - Or infers from image content

6. **Description Generation** → `description.py` creates:
   - A detailed description
   - Relevant tags

7. **Visualization** → The system creates:
   - Annotated image (with bounding boxes)
   - Heatmap showing object density

8. **Display Results** → Everything is shown on the results page

### Example Workflow:

```
Upload Image (upload.html)
    ↓
Process Image (app.py → process_image())
    ↓
Detect Objects (detector.py → detect_objects())
    ↓
Classify Image (detector.py → classify_image())
    ↓
Extract Location (location.py → extract_location())
    ↓
Generate Description (description.py → generate_description())
    ↓
Create Visualizations (image_processor.py)
    ↓
Display Results (results.html)
```

---

## Troubleshooting

### Problem: "Module not found" error

**Solution:** Make sure you:
1. Activated your virtual environment (`(venv)` should appear)
2. Installed requirements: `pip install -r requirements.txt`

### Problem: "Port 5000 already in use"

**Solution:** Either:
- Close the other application using port 5000
- Or change the port in `app.py`:
  ```python
  app.run(debug=True, port=5001)  # Change 5000 to 5001
  ```

### Problem: Images not uploading

**Solution:** 
1. Check that `static/uploads/` folder exists
2. Make sure the folder has write permissions
3. Check file size (max 16MB)

### Problem: No objects detected

**Solution:** This is normal! The demo version uses simple heuristics. For better results:
- Use images with clear objects
- Try different image types
- The system will still provide classification and location info

### Problem: Location shows "Unknown location"

**Solution:**
- The image might not have GPS metadata
- Try images taken with a phone camera (they usually have GPS data)
- Or set up Google Maps API key for better location detection

---

## Next Steps

Once you have the system running:

1. **Try uploading different images:**
   - Satellite images
   - Regular photos
   - Urban scenes
   - Landscapes

2. **Explore the code:**
   - Start with `app.py` to understand the web interface
   - Look at `demo.py` to see how detection works
   - Modify `description.py` to customize descriptions

3. **Customize the system:**
   - Change colors in `image_processor.py`
   - Modify templates in `templates/` folder
   - Add new object classes in `detector.py`

4. **Learn more:**
   - Flask documentation: https://flask.palletsprojects.com/
   - OpenCV tutorial: https://opencv-python-tutroals.readthedocs.io/
   - Image processing basics: https://pillow.readthedocs.io/

---

## Quick Reference Commands

```bash
# Navigate to project
cd path/to/project

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Run tests
python test.py

# Deactivate virtual environment (when done)
deactivate
```

---

## Need Help?

- Check the `README.md` for more technical details
- Look at the code comments in each file
- Search online for Flask, OpenCV, or Python tutorials
- Check error messages carefully - they often tell you what's wrong

---

**Congratulations!** You've set up your Image Detection System. Now start exploring and have fun! 🎉

