# ⚡ Quick Start Guide

Get your Image Detection System running in **3 simple steps**!

## 🎯 What You Need

- Python 3.8 or higher
- Internet connection (for downloading packages)
- A web browser

## 📦 Step 1: Install Dependencies

Open terminal/command prompt in the project folder:

```bash
pip install -r requirements.txt
```

**What this installs:**
- Flask (web framework)
- YOLOv8 (object detection)
- OpenCV (image processing)
- Pillow (image handling)
- And a few other libraries

**Time:** ~3-5 minutes

## 🚀 Step 2: Run the Application

```bash
python app.py
```

You should see:
```
============================================================
Image Detection System
============================================================

✓ Server starting...
✓ Open your browser: http://localhost:5000
✓ Press Ctrl+C to stop the server
============================================================
```

## 🌐 Step 3: Open in Browser

Open your web browser and go to:
```
http://localhost:5000
```

**That's it!** You should see the Image Detection System homepage.

## 📸 Step 4: Test It!

1. Click "Upload" or use the quick upload on homepage
2. Select an image (JPG, PNG, etc.)
3. Click "Analyze Image"
4. Wait a few seconds...
5. See results with:
   - ✅ Detected objects
   - ✅ Bounding boxes with labels
   - ✅ Location information
   - ✅ Description
   - ✅ Heatmap visualization

## 🎓 How It Works

```
You Upload Image
    ↓
YOLOv8 Detects Objects (automatically!)
    ↓
System Draws Boxes & Labels
    ↓
Extracts Location (if available)
    ↓
Generates Description
    ↓
Shows Results on Web Page
```

## 🔧 Troubleshooting

### "Module not found" error
**Solution:** Make sure you installed requirements:
```bash
pip install -r requirements.txt
```

### Port 5000 already in use
**Solution:** Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### YOLOv8 downloading model
**First time only:** YOLOv8 downloads a small model file (~6MB). This is normal!

### No objects detected
**Try:**
- Images with clear objects (people, cars, animals, etc.)
- Different image types
- System will still show classification and location info

## 📚 Next Steps

- Read `docs/GETTING_STARTED.md` for detailed setup
- Read `docs/PROJECT_CREATION_GUIDE.md` to understand how it was built
- Read `docs/TECHNOLOGIES.md` to learn about the tools used
- Explore the code to see how it works!

## 🎉 You're Done!

Your Image Detection System is now running! 🚀

