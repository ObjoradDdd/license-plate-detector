import argparse
import cv2
import logging
from model_impl import My_LicensePlate_Model

# Setup logging
logging.basicConfig(
    filename='./data/log_file.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def draw_boxes(frame, detections):
    """
    Draws bounding boxes and confidence scores on the frame.
    """
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        conf = det['confidence']
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        label = f"Plate {conf:.2f}"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
    return frame

def process_video(model: My_LicensePlate_Model, input_path: str, output_path: str):
    """
    Processes an existing video file and saves the result.
    """
    logger.info(f"Starting video processing: {input_path}")
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        logger.error(f"Cannot open video file: {input_path}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        detections = model.detect_plates(frame)
        
        frame_with_boxes = draw_boxes(frame, detections)
        
        out.write(frame_with_boxes)

    cap.release()
    out.release()
    logger.info(f"Video processing finished. Saved to: {output_path}")

def process_stream(model: My_LicensePlate_Model):
    """
    Processes the webcam stream in real-time.
    """
    logger.info("Starting live stream processing")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        logger.error("Cannot open webcam")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            logger.error("Failed to grab frame from webcam")
            break
            
        # Detect plates
        detections = model.detect_plates(frame)
        
        # Draw results
        frame_with_boxes = draw_boxes(frame, detections)
        
        # Display the resulting frame
        cv2.imshow('License Plate Detection (Press "q" to exit)', frame_with_boxes)
        
        # Press 'q' on keyboard to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    logger.info("Live stream processing finished")

def main():
    
    parser = argparse.ArgumentParser(description="License Plate Detection CLI")
    parser.add_argument('--mode', type=str, required=True, choices=['video', 'stream'], 
                        help="Operating mode: 'video' for file, 'stream' for webcam")
    parser.add_argument('--weights', type=str, default='best.pt', 
                        help="Path to YOLO weights file")
    parser.add_argument('--input', type=str, 
                        help="Path to input video file (required for 'video' mode)")
    parser.add_argument('--output', type=str, default='./data/output.mp4', 
                        help="Path to save output video (for 'video' mode)")

    args = parser.parse_args()

    # Initialize model
    try:
        model = My_LicensePlate_Model(model_path=args.weights)
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    # Run the selected mode
    if args.mode == 'stream':
        process_stream(model)
    elif args.mode == 'video':
        if not args.input:
            print("Error: --input argument is required for 'video' mode")
            return
        process_video(model, args.input, args.output)

if __name__ == "__main__":
    main()