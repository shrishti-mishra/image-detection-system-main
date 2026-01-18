"""
Simplified Location Extractor
Extracts location information from image metadata
"""

import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim
from dotenv import load_dotenv

load_dotenv()


class LocationExtractor:
    """Simple location extractor from image EXIF data"""
    
    def __init__(self):
        """Initialize location extractor"""
        try:
            self.geolocator = Nominatim(user_agent="image_detection_app")
            print("✓ Location extractor initialized")
        except Exception as e:
            print(f"⚠ Warning: Could not initialize geocoder: {e}")
            self.geolocator = None
    
    def extract_location(self, image_path):
        """
        Extract location from image EXIF metadata
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with location information
        """
        # Try to extract GPS coordinates from EXIF
        gps_data = self._extract_gps_from_exif(image_path)
        
        if gps_data:
            # Convert coordinates to address
            address = self._reverse_geocode(gps_data['latitude'], gps_data['longitude'])
            
            return {
                'latitude': gps_data['latitude'],
                'longitude': gps_data['longitude'],
                'name': address,
                'confidence': 0.9
            }
        
        # If no GPS data, return unknown
        return {
            'name': 'Unknown Location',
            'confidence': 0.5
        }
    
    def _extract_gps_from_exif(self, image_path):
        """
        Extract GPS coordinates from image EXIF data
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with latitude and longitude, or None
        """
        try:
            image = Image.open(image_path)
            
            # Try to get EXIF data
            exif_data = None
            if hasattr(image, '_getexif') and image._getexif():
                exif_data = image._getexif()
            elif hasattr(image, 'getexif'):
                exif_data = image.getexif()
            
            if not exif_data:
                return None
            
            # Find GPS info
            gps_info = None
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == "GPSInfo":
                    gps_info = {}
                    for gps_tag_id, gps_value in value.items():
                        gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                        gps_info[gps_tag] = gps_value
                    break
            
            if not gps_info:
                return None
            
            # Extract latitude and longitude
            if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
                lat = self._convert_to_degrees(gps_info["GPSLatitude"])
                lon = self._convert_to_degrees(gps_info["GPSLongitude"])
                
                # Apply reference direction
                if gps_info.get("GPSLatitudeRef", "N") == "S":
                    lat = -lat
                if gps_info.get("GPSLongitudeRef", "E") == "W":
                    lon = -lon
                
                return {
                    'latitude': lat,
                    'longitude': lon
                }
            
        except Exception as e:
            print(f"Error extracting GPS: {e}")
        
        return None
    
    def _convert_to_degrees(self, value):
        """Convert GPS coordinates to decimal degrees"""
        def to_float(x):
            try:
                if isinstance(x, tuple) and len(x) == 2:
                    return float(x[0]) / float(x[1]) if x[1] != 0 else 0.0
                return float(x)
            except:
                return 0.0
        
        d = to_float(value[0])
        m = to_float(value[1])
        s = to_float(value[2])
        
        return d + (m / 60.0) + (s / 3600.0)
    
    def _reverse_geocode(self, latitude, longitude):
        """
        Convert GPS coordinates to address
        
        Args:
            latitude: Latitude in decimal degrees
            longitude: Longitude in decimal degrees
            
        Returns:
            Address string
        """
        if self.geolocator is None:
            return "Unknown Location"
        
        try:
            location = self.geolocator.reverse((latitude, longitude), timeout=10)
            if location and location.address:
                return location.address
        except Exception as e:
            print(f"Error in reverse geocoding: {e}")
        
        return f"Location: {latitude:.4f}, {longitude:.4f}"
    
    def generate_maps_url(self, latitude, longitude, zoom=15):
        """
        Generate Google Maps URL
        
        Args:
            latitude: Latitude
            longitude: Longitude
            zoom: Zoom level
            
        Returns:
            Google Maps URL
        """
        return f"https://www.google.com/maps?q={latitude},{longitude}&z={zoom}"

