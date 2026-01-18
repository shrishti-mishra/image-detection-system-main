# 🖼️ Image Detection System

A web-based application for automatically detecting objects in images, extracting location information, and generating detailed descriptions. Uses YOLOv8 for state-of-the-art object detection.

## ✨ Features

- 📤 **Upload Images** - Support for JPG, PNG, TIFF formats
- 🔍 **Object Detection** - Detects 80+ object types using YOLOv8
- 📦 **Labeled Bounding Boxes** - Visual annotations with confidence scores
- 📍 **Location Extraction** - Reads GPS data from image EXIF metadata
- 📝 **Auto Descriptions** - Generates descriptions and tags
- 🎨 **Visualizations** - Heatmaps and annotated images
- 🌐 **Web Interface** - Beautiful, responsive UI

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open Browser
```
http://localhost:5000
```

**That's it!** Upload an image and see the magic happen! ✨

## 📁 Project Structure

```
project/
├── app.py                 ⭐ Main application (run this!)
├── requirements.txt       📦 Dependencies
│
├── detector.py           🤖 Object detection (YOLOv8)
├── image_processor.py    🖼️ Image processing
├── location.py           📍 Location extraction
├── description.py        📝 Description generation
│
├── templates/            🌐 HTML pages
├── static/               🎨 CSS, JS, uploads
│
└── docs/                 📚 Documentation
    ├── START_HERE.md
    ├── GETTING_STARTED.md
    ├── PROJECT_CREATION_GUIDE.md
    └── TECHNOLOGIES.md
```

## 🛠️ Technologies Used

- **Flask** - Web framework
- **YOLOv8** - Object detection AI
- **OpenCV** - Image processing
- **Pillow** - Image I/O and EXIF
- **NumPy** - Array operations
- **Geopy** - Location geocoding

See `docs/TECHNOLOGIES.md` for detailed explanations.

## 📚 Documentation

- **📖 [GETTING_STARTED.md](docs/GETTING_STARTED.md)** - Complete setup guide
- **🏗️ [PROJECT_CREATION_GUIDE.md](docs/PROJECT_CREATION_GUIDE.md)** - How the project was created
- **🛠️ [TECHNOLOGIES.md](docs/TECHNOLOGIES.md)** - Tools and technologies explained
- **📁 [FINAL_STRUCTURE.md](docs/FINAL_STRUCTURE.md)** - Project structure details

## 🎯 How It Works

```
1. User uploads image
   ↓
2. YOLOv8 detects objects
   ↓
3. System draws bounding boxes
   ↓
4. Extracts location (if available)
   ↓
5. Generates description
   ↓
6. Displays results
```

## 📋 Requirements

- Python 3.8+
- pip (Python package manager)
- Web browser

## 🔧 Configuration

### Optional: Google Maps API Key

For enhanced location features, create a `.env` file:
```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to modify and improve this project!

## 📞 Support

- Check `docs/GETTING_STARTED.md` for setup help
- Check `docs/TECHNOLOGIES.md` to understand the tech stack
- Read the code comments for implementation details

---

**Made with ❤️ using Python, Flask, and YOLOv8**
