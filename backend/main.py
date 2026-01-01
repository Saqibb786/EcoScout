from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import shutil
import os
import uuid
from datetime import datetime
from detection import run_inference
import history_manager

app = FastAPI(title="EcoScout API", description="Smart Vehicle Littering & Smoke Emission Detection System")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory Setup
UPLOAD_DIR = "uploads"
RESULTS_DIR = "results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Mount static files for serving annotated images
app.mount("/results", StaticFiles(directory=RESULTS_DIR), name="results")

@app.get("/")
async def root():
    return {"message": "EcoScout API is running"}

@app.post("/upload")
async def upload_media(file: UploadFile = File(...)):
    try:
        # Generate unique filename
        file_ext = file.filename.split(".")[-1]
        file_id = str(uuid.uuid4())
        filename = f"{file_id}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Determine output path
        output_filename = f"annotated_{filename}"
        output_path = os.path.join(RESULTS_DIR, output_filename)
        
        if file_ext.lower() in ['jpg', 'jpeg', 'png', 'bmp']:
            detections = run_inference(file_path, output_path)
            
            result = {
                "id": file_id,
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "original_file": filename,
                "annotated_image_url": f"http://localhost:8000/results/{output_filename}",
                "detections": detections
            }
            
            # Save to history
            history_manager.add_record(result)
            
            return JSONResponse(content=result)
            
        elif file_ext.lower() in ['mp4', 'avi', 'mov']:
            import cv2
            cap = cv2.VideoCapture(file_path)
            if not cap.isOpened():
                 raise HTTPException(status_code=400, detail="Could not open video file")
            
            # Video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Output video writer
            output_video_filename = f"annotated_{filename}"
            output_video_path = os.path.join(RESULTS_DIR, output_video_filename)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v') # or 'avc1'
            out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
            
            all_detections = []
            frame_count = 0
            process_every_n_frames = 5 # Optimization
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process specific frames
                if frame_count % process_every_n_frames == 0:
                    # Run inference on the frame (pass frame directly)
                    # We don't save individual frame images to disk to save space/time
                    # unless debugging is needed.
                    detections = run_inference(frame, output_path=None)
                    
                    # Add timestamp/frame info to detections
                    for d in detections:
                        d['frame'] = frame_count
                        d['timestamp'] = frame_count / fps
                        all_detections.append(d)
                        
                    # Draw annotations on the frame for the video
                    # Note: run_inference draws on the image passed to it if we modified it to do so inplace
                    # or returned the annotated image.
                    # Our modified run_inference draws on 'img' which is a copy or the original.
                    # Let's adjust run_inference to return the annotated image or we just re-draw here?
                    # Actually, the modified run_inference draws on the input image if it's an array?
                    # Wait, "img = image_input.copy()" in my proposed change.
                    # So we need to get that annotated image back if we want to write it to video.
                    
                    # Let's slightly adjust the logic.
                    # Since run_inference returns records, we can re-draw or better yet, 
                    # let's just use the detections to draw on the current frame for the video output.
                    
                    for d in detections:
                        bbox = d['bbox']
                        label = d['violation_type']
                        conf = d['confidence']
                        color = (0, 255, 0)
                        if label.lower() in ['littering', 'smoke']:
                            color = (0, 0, 255)
                        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
                        cv2.putText(frame, f"{label} {conf}", (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                        if d.get('license_plate') != "N/A":
                             cv2.putText(frame, f"Plate: {d['license_plate']}", (bbox[0], bbox[3]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

                out.write(frame)
                frame_count += 1
                
            cap.release()
            out.release()
            
            result = {
                "id": file_id,
                "status": "success",
                "message": "Video processed successfully",
                "timestamp": datetime.now().isoformat(),
                "original_file": filename,
                "annotated_video_url": f"http://localhost:8000/results/{output_video_filename}",
                "detections": all_detections,
                "frame_count": frame_count
            }
            
            # Save to history
            history_manager.add_record(result)
            
            return JSONResponse(content=result)

        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history():
    return history_manager.get_all_records()

@app.delete("/history")
async def delete_history(ids: list[str] = Body(...)):
    count = history_manager.delete_records(ids)
    return {"message": f"Deleted {count} records"}

@app.get("/report/{id}")
async def get_report(id: str):
    # Find record
    records = history_manager.get_all_records()
    record = next((r for r in records if r['id'] == id), None)
    
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
        
    # Generate PDF
    report_filename = f"report_{id}.pdf"
    report_path = os.path.join(RESULTS_DIR, report_filename)
    
    try:
        from report_generator import generate_pdf_report
        generate_pdf_report(record, report_path)
        
        return FileResponse(report_path, media_type='application/pdf', filename=report_filename, content_disposition_type='inline')
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
