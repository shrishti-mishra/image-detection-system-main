"""
Simplified Image Processor
Handles image loading, annotation, and visualization
"""

import cv2
import numpy as np
import base64
from PIL import Image
import io


class ImageProcessor:
    """Simple image processing utilities"""
    
    def __init__(self):
        """Initialize the image processor"""
        # Colors for different confidence levels
        self.colors = {
            'high': (0, 255, 0),      # Green for high confidence
            'medium': (255, 255, 0),  # Yellow for medium confidence
            'low': (0, 165, 255),     # Orange for low confidence
        }
    
    def load_image(self, image_path):
        """
        Load image from file
        
        Args:
            image_path: Path to image file
            
        Returns:
            Image as numpy array (RGB format)
        """
        try:
            # Read image using OpenCV
            image = cv2.imread(image_path)
            
            if image is None:
                print(f"Error: Could not load image from {image_path}")
                return None
            
            # Convert from BGR to RGB (OpenCV uses BGR by default)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            return image
            
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def draw_boxes(self, image, detected_objects):
        """
        Draw bounding boxes and labels on image
        
        Args:
            image: Image as numpy array (RGB)
            detected_objects: List of detected objects
            
        Returns:
            Annotated image
        """
        # Create a copy of the image
        annotated = image.copy()
        
        # Convert RGB to BGR for OpenCV drawing functions
        annotated = cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR)
        
        for obj in detected_objects:
            if 'bbox' not in obj:
                continue
            
            # Get bounding box coordinates
            x1, y1, x2, y2 = obj['bbox']
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Get object info
            class_name = obj.get('class_name', 'Unknown')
            confidence = obj.get('confidence', 0.0)
            
            # Choose color based on confidence
            if confidence > 0.7:
                color = self.colors['high']
            elif confidence > 0.4:
                color = self.colors['medium']
            else:
                color = self.colors['low']
            
            # Draw bounding box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            
            # Prepare label text
            label = f"{class_name}: {confidence:.2f}"
            
            # Get text size for background
            (text_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
            )
            
            # Draw label background
            cv2.rectangle(
                annotated,
                (x1, y1 - text_height - 10),
                (x1 + text_width, y1),
                color,
                -1
            )
            
            # Draw label text
            cv2.putText(
                annotated,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),  # White text
                2
            )
        
        # Convert back to RGB
        annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        
        return annotated
    
    def create_heatmap(self, image, detected_objects):
        """
        Create a heatmap visualization showing object density
        
        Args:
            image: Original image
            detected_objects: List of detected objects
            
        Returns:
            Heatmap image
        """
        # Create a blank heatmap
        heatmap = np.zeros((image.shape[0], image.shape[1]), dtype=np.float32)
        
        # Add heat for each detected object
        for obj in detected_objects:
            if 'bbox' not in obj:
                continue
            
            x1, y1, x2, y2 = obj['bbox']
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Get confidence as heat intensity
            confidence = obj.get('confidence', 0.5)
            
            # Add heat to the bounding box area
            heatmap[y1:y2, x1:x2] += confidence
        
        # Normalize heatmap
        if np.max(heatmap) > 0:
            heatmap = heatmap / np.max(heatmap)
        
        # Convert to color map (JET colormap: blue -> green -> yellow -> red)
        heatmap_colored = cv2.applyColorMap(
            (heatmap * 255).astype(np.uint8),
            cv2.COLORMAP_JET
        )
        
        # Convert BGR to RGB
        heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
        
        # Blend with original image (70% original, 30% heatmap)
        alpha = 0.7
        blended = cv2.addWeighted(image, alpha, heatmap_colored, 1 - alpha, 0)
        
        return blended
    
    def image_to_base64(self, image):
        """
        Convert image to base64 string for web display
        
        Args:
            image: Image as numpy array (RGB)
            
        Returns:
            Base64 encoded string with data URI
        """
        try:
            # Convert RGB to BGR for OpenCV
            if len(image.shape) == 3 and image.shape[2] == 3:
                image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            else:
                image_bgr = image
            
            # Encode image as JPEG
            _, buffer = cv2.imencode('.jpg', image_bgr, [cv2.IMWRITE_JPEG_QUALITY, 85])
            
            # Convert to base64
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # Return as data URI
            return f"data:image/jpeg;base64,{img_base64}"
            
        except Exception as e:
            print(f"Error converting image to base64: {e}")
            return ""

