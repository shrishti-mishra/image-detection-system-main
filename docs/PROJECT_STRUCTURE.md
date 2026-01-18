# Project Structure Guide

This document explains the organization and purpose of every file and folder in the Image Detection System.

## 📁 Directory Structure

```
project/
│
├── 📄 Core Application Files
│   ├── app.py                 # Main Flask web application
│   ├── api.py                 # REST API endpoints
│   └── requirements.txt       # Python package dependencies
│
├── 📄 Core Logic Modules
│   ├── detector.py            # Object detection using ML models
│   ├── demo.py                # Demo/fallback detection (no ML required)
│   ├── image_processor.py     # Image processing and visualization
│   ├── location.py            # Location extraction from metadata
│   └── description.py         # Description and tag generation
│
├── 📄 Documentation
│   ├── README.md              # Technical documentation
│   ├── GETTING_STARTED.md     # Beginner setup guide
│   └── PROJECT_STRUCTURE.md   # This file
│
├── 📁 Web Interface
│   ├── templates/             # HTML templates
│   │   ├── index.html         # Home page
│   │   ├── upload.html        # Image upload interface
│   │   └── results.html       # Results display page
│   │
│   └── static/                # Static web assets
│       ├── css/
│       │   └── style.css      # Website styling
│       ├── js/
│       │   └── main.js        # Client-side JavaScript
│       └── uploads/           # User-uploaded images storage
│
├── 📁 Utilities
│   ├── scripts/
│   │   └── create_ppt.py      # PowerPoint presentation generator
│   ├── uploads/               # Additional upload storage
│   └── test.py                # Unit tests
│
└── 📁 Generated/Runtime (not in repo)
    ├── __pycache__/           # Python bytecode cache (auto-generated)
    └── venv/                  # Virtual environment (create locally)
```

---

## 📄 File Descriptions

### Core Application Files

#### `app.py`
**Purpose:** Main Flask web application entry point  
**What it does:**
- Initializes Flask web server
- Defines web routes (home, upload, results)
- Handles image uploads
- Orchestrates image processing pipeline
- Renders HTML templates

**Key Functions:**
- `index()` - Home page route
- `upload()` - Image upload handler
- `process_image()` - Main image processing function

**Dependencies:** Flask, all core modules

---

#### `api.py`
**Purpose:** REST API endpoints for programmatic access  
**What it does:**
- Provides `/api/detect` endpoint
- Accepts image uploads via POST
- Returns JSON responses with detection results
- Can be used by other applications/services

**Key Endpoints:**
- `POST /api/detect` - Detect objects in uploaded image
- `POST /api/location` - Extract location only
- `POST /api/describe` - Generate description from data
- `POST /api/export` - Export labeled dataset

**Dependencies:** Flask Blueprint, all core modules

---

#### `requirements.txt`
**Purpose:** Lists all Python packages needed  
**What it contains:**
- Package names and versions
- Used by `pip install -r requirements.txt`

**Key Packages:**
- Flask (web framework)
- OpenCV (image processing)
- Pillow (image handling)
- NumPy (numerical operations)
- TensorFlow/PyTorch (ML models, optional)

---

### Core Logic Modules

#### `detector.py`
**Purpose:** Object detection using machine learning models  
**What it does:**
- Loads TensorFlow/PyTorch models
- Detects objects in images
- Classifies image types
- Returns bounding boxes and confidence scores

**Key Classes:**
- `SatelliteDetector` - Main detector class

**Key Methods:**
- `detect_objects(image)` - Find objects in image
- `classify_image(image_path)` - Classify image type
- `annotate_image(image, objects)` - Draw bounding boxes

**Fallback:** If models fail to load, falls back to `demo.py`

---

#### `demo.py`
**Purpose:** Demo/fallback detection without heavy ML models  
**What it does:**
- Provides simplified object detection
- Works without TensorFlow/PyTorch
- Uses image analysis heuristics
- Perfect for testing and development

**Key Classes:**
- `DemoSatelliteDetector` - Demo detector
- `DemoLocationExtractor` - Demo location finder
- `DemoDescriptionGenerator` - Demo description generator
- `DemoImageProcessor` - Demo image processor

**When to use:** 
- Testing the system
- When ML models aren't available
- For development/debugging

---

#### `image_processor.py`
**Purpose:** Image processing and visualization  
**What it does:**
- Loads and preprocesses images
- Draws bounding boxes on images
- Creates heatmap visualizations
- Converts images to web formats (base64)
- Handles image format conversions

**Key Classes:**
- `ImageProcessor` - Main processor class

**Key Methods:**
- `preprocess_image(image_path)` - Load and prepare image
- `annotate_image(image, objects)` - Draw detection boxes
- `create_heatmap(image, objects)` - Generate heatmap
- `image_to_base64(image)` - Convert for web display

---

#### `location.py`
**Purpose:** Extract location information from images  
**What it does:**
- Reads GPS data from image EXIF metadata
- Performs reverse geocoding (coordinates → address)
- Detects famous landmarks
- Generates Google Maps URLs

**Key Classes:**
- `LocationExtractor` - Main location extractor

**Key Methods:**
- `extract_location(image_path)` - Get location from image
- `_extract_from_exif(image_path)` - Read GPS from metadata
- `_reverse_geocode(lat, lon)` - Convert coordinates to address
- `generate_maps_url(lat, lon)` - Create maps link

**Dependencies:** Pillow (EXIF), geopy (geocoding)

---

#### `description.py`
**Purpose:** Generate descriptions and tags  
**What it does:**
- Creates human-readable image descriptions
- Generates relevant tags
- Analyzes object relationships
- Provides contextual information

**Key Classes:**
- `DescriptionGenerator` - Main generator class

**Key Methods:**
- `generate_description(objects, class, location)` - Create description
- `generate_tags(objects, class, location)` - Create tags
- `_add_context()` - Add contextual information

---

### Web Interface Files

#### `templates/index.html`
**Purpose:** Home page of the web application  
**What it shows:**
- Welcome message
- Project description
- Navigation links
- Instructions for use

---

#### `templates/upload.html`
**Purpose:** Image upload interface  
**What it does:**
- Provides file upload form
- Shows image preview
- Validates file types
- Submits to processing endpoint

---

#### `templates/results.html`
**Purpose:** Display analysis results  
**What it shows:**
- Original image
- Annotated image (with bounding boxes)
- Heatmap visualization
- Detected objects list
- Image classification
- Location information
- Generated description
- Tags

---

#### `static/css/style.css`
**Purpose:** Website styling  
**What it contains:**
- Color schemes
- Layout styles
- Responsive design rules
- Component styling

---

#### `static/js/main.js`
**Purpose:** Client-side JavaScript  
**What it does:**
- Handles form submissions
- Image preview functionality
- AJAX requests
- Dynamic UI updates

---

### Utility Files

#### `scripts/create_ppt.py`
**Purpose:** Generate PowerPoint presentations from results  
**What it does:**
- Creates PowerPoint files
- Adds images and results
- Formats slides
- Exports analysis results

**Usage:** Run separately to create presentations from detection results

---

#### `test.py`
**Purpose:** Unit tests for the system  
**What it tests:**
- Component initialization
- Object detection
- Image classification
- Location extraction
- Description generation

**Run with:** `python test.py`

---

## 🔄 Data Flow

### Image Upload Flow:
```
User uploads image
    ↓
app.py receives file
    ↓
Saves to static/uploads/
    ↓
Calls process_image()
    ↓
image_processor.preprocess_image()
    ↓
detector.detect_objects()
    ↓
detector.classify_image()
    ↓
location_extractor.extract_location()
    ↓
description_generator.generate_description()
    ↓
image_processor.annotate_image()
    ↓
image_processor.create_heatmap()
    ↓
Render results.html with all data
```

### API Request Flow:
```
POST /api/detect
    ↓
api.py receives request
    ↓
Saves uploaded file
    ↓
Calls same processing pipeline
    ↓
Returns JSON response
```

---

## 📦 Dependencies Between Files

```
app.py
  ├── imports from api.py (API blueprint)
  ├── imports from detector.py (or demo.py)
  ├── imports from image_processor.py
  ├── imports from location.py
  ├── imports from description.py
  └── uses templates/ folder

api.py
  ├── imports from detector.py (or demo.py)
  ├── imports from image_processor.py
  ├── imports from location.py
  └── imports from description.py

detector.py
  └── uses TensorFlow/PyTorch (optional)

demo.py
  └── standalone (no external ML dependencies)

image_processor.py
  ├── uses OpenCV
  └── uses Pillow

location.py
  ├── uses Pillow (EXIF)
  └── uses geopy (geocoding)
```

---

## 🎯 Where to Start

1. **New to the project?** → Read `GETTING_STARTED.md`
2. **Want to understand the code?** → Start with `app.py`
3. **Want to modify detection?** → Look at `detector.py` or `demo.py`
4. **Want to change the UI?** → Edit files in `templates/` and `static/`
5. **Want to add features?** → Check `api.py` for API structure

---

## 📝 Notes

- **Upload folders:** Both `static/uploads/` and `uploads/` are used. The app creates them automatically.
- **Demo mode:** If ML models fail, the system automatically uses `demo.py` for basic functionality.
- **Cache files:** `__pycache__/` folders are auto-generated by Python and can be safely ignored/deleted.
- **Virtual environment:** The `venv/` folder should NOT be committed to version control.

---

## 🔧 Maintenance

### Files to Clean Regularly:
- `static/uploads/*` - Old uploaded images
- `uploads/*` - Old uploaded images
- `__pycache__/` - Python cache (can delete anytime)

### Files to Update:
- `requirements.txt` - When adding new packages
- `README.md` - When adding features
- `GETTING_STARTED.md` - When setup process changes

---

This structure is designed to be:
- **Modular:** Each file has a clear, single purpose
- **Maintainable:** Easy to find and modify code
- **Extensible:** Easy to add new features
- **Beginner-friendly:** Clear organization and documentation

