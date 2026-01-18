"""
Simplified Description Generator
Creates descriptions and tags from detected objects
"""

from collections import Counter


class DescriptionGenerator:
    """Simple description and tag generator"""
    
    def __init__(self):
        """Initialize description generator"""
        pass
    
    def generate_description(self, detected_objects, image_class, location_info):
        """
        Generate a description of the image
        
        Args:
            detected_objects: List of detected objects
            image_class: Image classification
            location_info: Location information
            
        Returns:
            Description string
        """
        # Start with image classification
        class_name = image_class.get('class', 'Unknown') if image_class else 'Unknown'
        confidence = image_class.get('confidence', 0.5) if image_class else 0.5
        
        # Build description
        description = f"This image shows a {class_name.lower()}"
        
        # Add location if available
        location_name = location_info.get('name', '') if location_info else ''
        if location_name and location_name != 'Unknown Location':
            description += f" located in {location_name}"
        
        description += ". "
        
        # Add object information
        if detected_objects and len(detected_objects) > 0:
            # Count objects by type
            object_counts = Counter([obj['class_name'] for obj in detected_objects])
            
            description += f"The image contains {len(detected_objects)} detected object(s): "
            
            # List top objects
            top_objects = object_counts.most_common(5)
            object_list = []
            for obj_name, count in top_objects:
                if count > 1:
                    object_list.append(f"{count} {obj_name}s")
                else:
                    object_list.append(f"1 {obj_name}")
            
            description += ", ".join(object_list) + ". "
            
            # Add confidence info
            avg_confidence = sum(obj.get('confidence', 0) for obj in detected_objects) / len(detected_objects)
            description += f"Average detection confidence: {avg_confidence:.1%}. "
        else:
            description += "No specific objects were detected in this image. "
        
        # Add classification confidence
        if confidence > 0.7:
            description += f"The image classification has high confidence ({confidence:.1%})."
        elif confidence > 0.5:
            description += f"The image classification has moderate confidence ({confidence:.1%})."
        
        return description
    
    def generate_tags(self, detected_objects, image_class, location_info):
        """
        Generate tags for the image
        
        Args:
            detected_objects: List of detected objects
            image_class: Image classification
            location_info: Location information
            
        Returns:
            List of tags
        """
        tags = []
        
        # Add image class as tag
        if image_class and 'class' in image_class:
            tags.append(image_class['class'])
        
        # Add location tags
        if location_info and 'name' in location_info:
            location_name = location_info['name']
            if location_name and location_name != 'Unknown Location':
                # Extract location components
                parts = location_name.split(', ')
                tags.extend(parts[-2:])  # Add city and country
        
        # Add object tags
        if detected_objects:
            object_names = [obj['class_name'] for obj in detected_objects]
            unique_objects = list(set(object_names))
            tags.extend(unique_objects[:10])  # Limit to 10 object tags
        
        # Add confidence-based tags
        if detected_objects:
            avg_confidence = sum(obj.get('confidence', 0) for obj in detected_objects) / len(detected_objects)
            if avg_confidence > 0.7:
                tags.append('high-confidence')
            elif avg_confidence > 0.4:
                tags.append('medium-confidence')
        
        # Remove duplicates and return
        return list(dict.fromkeys(tags))[:15]  # Limit to 15 tags total

