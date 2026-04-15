import os
import logging
import numpy as np
from ultralytics import YOLO

# Ensure the log directory exists
os.makedirs('./data', exist_ok=True)

# Configure logger
logging.basicConfig(
    filename='./data/log_file.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class My_LicensePlate_Model:
    """
    Class for detecting license plates using a trained YOLO model.
    """
    
    def __init__(self, model_path: str):
        """
        Initialize the model.
        
        :param model_path: Path to the model weights file (e.g., 'best.pt')
        """
        try:
            # Load the trained YOLO model
            self.model = YOLO(model_path)
            logger.info(f"Model successfully loaded from {model_path}")
        except Exception as e:
            logger.error(f"Critical error loading model from {model_path}: {e}")
            raise

    def detect_plates(self, frame: np.ndarray) -> list[dict]:
        """
        Processes a single image frame and returns a list of detected license plates.
        
        :param frame: Frame in numpy array format (e.g., from cv2.VideoCapture)
        :return: List of dictionaries like [{"bbox": [x1, y1, x2, y2], "confidence": 0.95}, ...]
        """
        results_list = []
        try:
            results = self.model(frame, verbose=False)
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    
                    conf = float(box.conf[0])
                    
                    results_list.append({
                        "bbox": [int(x1), int(y1), int(x2), int(y2)],
                        "confidence": conf
                    })
                    
            logger.info(f"Frame processed. License plates found: {len(results_list)}")
            
        except Exception as e:
            logger.error(f"Error during detection on frame: {e}")
            raise
        return results_list