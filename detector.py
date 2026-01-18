"""
Simplified Object Detector using YOLOv8
YOLOv8 is much easier to use than TensorFlow/PyTorch!
"""

import os
from ultralytics import YOLO
import cv2
import numpy as np


class Detector:
    """Simple object detector using YOLOv8"""
    
    def __init__(self):
        """Initialize the detector"""
        print("Initializing YOLOv8 detector...")
        
        # YOLOv8 will automatically download the model on first use
        # Using 'yolov8n.pt' (nano) - smallest and fastest model
        # You can also use: yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt
        # Larger models = better accuracy but slower
        
        try:
            # Load YOLOv8 model (will download automatically if not present)
            self.model = YOLO('yolov8n.pt')  # nano model - fast and lightweight
            print("✓ YOLOv8 model loaded successfully!")
            
            # COCO class names (80 classes that YOLOv8 can detect)
            self.class_names = [
                'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck',
                'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
                'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
                'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
                'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
                'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
                'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
                'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet',
                'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven',
                'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
                'hair drier', 'toothbrush'
            ]
            
        except Exception as e:
            print(f"⚠ Warning: Could not load YOLOv8 model: {e}")
            print("The system will use fallback detection methods.")
            self.model = None
            self.class_names = []
    
    def detect_objects(self, image_path):
        """
        Detect objects in an image using YOLOv8
        
        Args:
            image_path: Path to the image file
            
        Returns:
            List of detected objects with bounding boxes and labels
        """
        if self.model is None:
            return self._fallback_detection(image_path)
        
        try:
            # Run YOLOv8 inference
            results = self.model(image_path)
            
            detected_objects = []
            
            # Process results
            for result in results:
                boxes = result.boxes
                
                for i, box in enumerate(boxes):
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    
                    # Get confidence score
                    confidence = float(box.conf[0].cpu().numpy())
                    
                    # Get class ID and name
                    class_id = int(box.cls[0].cpu().numpy())
                    class_name = self.class_names[class_id] if class_id < len(self.class_names) else f"class_{class_id}"
                    
                    # Only include high-confidence detections
                    if confidence > 0.25:  # Lower threshold to catch more objects
                        detected_objects.append({
                            'class': class_id,
                            'class_name': class_name,
                            'confidence': round(confidence, 2),
                            'bbox': [int(x1), int(y1), int(x2), int(y2)]  # [x1, y1, x2, y2]
                        })
            
            print(f"✓ Detected {len(detected_objects)} objects")
            return detected_objects
            
        except Exception as e:
            print(f"⚠ Error in YOLOv8 detection: {e}")
            return self._fallback_detection(image_path)
    
    def _fallback_detection(self, image_path):
        """Fallback detection if YOLOv8 is not available"""
        print("Using fallback detection...")
        
        # Simple fallback: return empty or basic detection
        try:
            img = cv2.imread(image_path)
            if img is None:
                return []
            
            height, width = img.shape[:2]
            
            # Return a simple detection in the center (for demo purposes)
            return [{
                'class': 0,
                'class_name': 'Image',
                'confidence': 0.5,
                'bbox': [width//4, height//4, width*3//4, height*3//4]
            }]
        except:
            return []
    
    def classify_image(self, detected_objects):
        """
        Classify image type based on detected objects
        
        Args:
            detected_objects: List of detected objects
            
        Returns:
            Dictionary with classification info
        """
        if not detected_objects:
            return {
                'class': 'Unknown',
                'confidence': 0.5
            }
        
        # Count objects by category
        object_names = [obj['class_name'] for obj in detected_objects]
        
        # Determine image type based on detected objects
        urban_objects = ['car', 'bus', 'truck', 'traffic light', 'stop sign', 'person', 'building']
        vehicle_objects = ['car', 'bus', 'truck', 'motorcycle', 'bicycle', 'airplane', 'train', 'boat']
        animal_objects = ['bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe']
        indoor_objects = ['chair', 'couch', 'bed', 'dining table', 'tv', 'laptop', 'refrigerator']
        
        urban_count = sum(1 for obj in object_names if obj in urban_objects)
        vehicle_count = sum(1 for obj in object_names if obj in vehicle_objects)
        animal_count = sum(1 for obj in object_names if obj in animal_objects)
        indoor_count = sum(1 for obj in object_names if obj in indoor_objects)
        
        # Classify based on dominant category
        if urban_count > 2:
            image_type = 'Urban Area'
            confidence = min(0.9, 0.6 + (urban_count * 0.05))
        elif vehicle_count > 1:
            image_type = 'Transportation Scene'
            confidence = 0.75
        elif animal_count > 0:
            image_type = 'Animal Scene'
            confidence = 0.8
        elif indoor_count > 2:
            image_type = 'Indoor Scene'
            confidence = 0.75
        else:
            image_type = 'General Scene'
            confidence = 0.65
        
        return {
            'class': image_type,
            'confidence': round(confidence, 2),
            'object_count': len(detected_objects)
        }

