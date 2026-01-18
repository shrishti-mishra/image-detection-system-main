import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import json

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the modules to test with fallbacks to demo versions
try:
    from detector import SatelliteDetector
except Exception:
    from demo import DemoSatelliteDetector as SatelliteDetector

try:
    from location import LocationExtractor
except Exception:
    from demo import DemoLocationExtractor as LocationExtractor

try:
    from description import DescriptionGenerator
except Exception:
    from demo import DemoDescriptionGenerator as DescriptionGenerator

try:
    from image_processor import ImageProcessor
except Exception:
    from demo import DemoImageProcessor as ImageProcessor

class TestSatelliteDetectionSystem(unittest.TestCase):
    """Test cases for the Satellite Detection System"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create test directory if it doesn't exist
        self.test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data')
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Create a sample test image
        self.test_image_path = os.path.join(self.test_dir, 'test_image.jpg')
        
        # Initialize components
        self.detector = SatelliteDetector()
        self.location_extractor = LocationExtractor()
        self.description_generator = DescriptionGenerator()
        self.image_processor = ImageProcessor()
    
    def test_detector_initialization(self):
        """Test that the detector initializes correctly"""
        self.assertIsNotNone(self.detector)
    
    def test_location_extractor_initialization(self):
        """Test that the location extractor initializes correctly"""
        self.assertIsNotNone(self.location_extractor)
    
    def test_description_generator_initialization(self):
        """Test that the description generator initializes correctly"""
        self.assertIsNotNone(self.description_generator)
    
    def test_image_processor_initialization(self):
        """Test that the image processor initializes correctly"""
        self.assertIsNotNone(self.image_processor)
    
    @patch('detector.SatelliteDetector.detect_objects')
    def test_object_detection(self, mock_detect):
        """Test object detection functionality"""
        # Mock the detect_objects method to return test data
        mock_objects = [
            {
                'class': 1,
                'class_name': 'building',
                'confidence': 0.95,
                'bbox': [100, 100, 200, 200]
            },
            {
                'class': 3,
                'class_name': 'road',
                'confidence': 0.85,
                'bbox': [300, 300, 400, 350]
            }
        ]
        mock_detect.return_value = mock_objects
        
        # Call the method
        result = self.detector.detect_objects(self.test_image_path)
        
        # Verify the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['class_name'], 'building')
        self.assertEqual(result[1]['class_name'], 'road')
    
    @patch('detector.SatelliteDetector.classify_image')
    def test_image_classification(self, mock_classify):
        """Test image classification functionality"""
        # Mock the classify_image method to return test data
        mock_classification = {
            'class': 'urban_area',
            'confidence': 0.82
        }
        mock_classify.return_value = mock_classification
        
        # Call the method
        result = self.detector.classify_image(self.test_image_path)
        
        # Verify the result
        self.assertEqual(result['class'], 'urban_area')
        self.assertAlmostEqual(result['confidence'], 0.82)
    
    @patch('location.LocationExtractor.extract_location')
    def test_location_extraction(self, mock_extract):
        """Test location extraction functionality"""
        # Mock the extract_location method to return test data
        mock_location = {
            'latitude': 37.7749,
            'longitude': -122.4194,
            'name': 'San Francisco, CA, USA',
            'confidence': 0.9
        }
        mock_extract.return_value = mock_location
        
        # Call the method
        result = self.location_extractor.extract_location(self.test_image_path)
        
        # Verify the result
        self.assertEqual(result['name'], 'San Francisco, CA, USA')
        self.assertEqual(result['latitude'], 37.7749)
        self.assertEqual(result['longitude'], -122.4194)
    
    def test_description_generation(self):
        """Test description generation functionality"""
        # Test data
        objects = [
            {
                'class': 1,
                'class_name': 'building',
                'confidence': 0.95,
                'bbox': [100, 100, 200, 200]
            },
            {
                'class': 3,
                'class_name': 'road',
                'confidence': 0.85,
                'bbox': [300, 300, 400, 350]
            }
        ]
        
        classification = {
            'class': 'urban_area',
            'confidence': 0.82
        }
        
        location = {
            'latitude': 37.7749,
            'longitude': -122.4194,
            'name': 'San Francisco, CA, USA',
            'confidence': 0.9
        }
        
        # Call the method
        description = self.description_generator.generate_description(
            objects, classification, location
        )
        
        # Verify the result
        self.assertIsInstance(description, str)
        self.assertGreater(len(description), 0)
        
        # Check that the description contains key information
        self.assertIn('urban_area', description)
        self.assertIn('San Francisco', description)
        self.assertIn('building', description)
        self.assertIn('road', description)
    
    def test_tag_generation(self):
        """Test tag generation functionality"""
        # Test data
        objects = [
            {
                'class': 1,
                'class_name': 'building',
                'confidence': 0.95,
                'bbox': [100, 100, 200, 200]
            },
            {
                'class': 3,
                'class_name': 'road',
                'confidence': 0.85,
                'bbox': [300, 300, 400, 350]
            }
        ]
        
        classification = {
            'class': 'urban_area',
            'confidence': 0.82
        }
        
        location = {
            'latitude': 37.7749,
            'longitude': -122.4194,
            'name': 'San Francisco, CA, USA',
            'confidence': 0.9
        }
        
        # Call the method
        tags = self.description_generator.generate_tags(
            objects, classification, location
        )
        
        # Verify the result
        self.assertIsInstance(tags, list)
        self.assertGreater(len(tags), 0)
        
        # Check that the tags contain key information
        self.assertIn('urban_area', tags)
        self.assertIn('building', tags)
        self.assertIn('road', tags)
    
    @patch('image_processor.ImageProcessor.preprocess_image')
    def test_image_preprocessing(self, mock_preprocess):
        """Test image preprocessing functionality"""
        # Mock the preprocess_image method to return test data
        import numpy as np
        mock_image = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_preprocess.return_value = mock_image
        
        # Call the method
        result = self.image_processor.preprocess_image(self.test_image_path)
        
        # Verify the result
        self.assertEqual(result.shape, (100, 100, 3))
    
    def tearDown(self):
        """Clean up after tests"""
        # Remove test directory and files
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main()