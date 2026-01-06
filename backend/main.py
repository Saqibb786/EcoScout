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
            # Use 'avc1' for H.264 which is web-friendly. Fallback to 'mp4v' if needed.
            # Note: OpenCV requires openh264-1.8.0-win64.dll or similar for avc1 on Windows sometimes.
            # If 'avc1' fails, it might fall back or error. 'mp4v' is safer but less compatible with some browsers.
            # Let's try 'mp4v' but ensure the container is .mp4. 
            # Actually, standard browsers support H.264 (avc1). 
            try:
                fourcc = cv2.VideoWriter_fourcc(*'avc1')
            except:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                
            out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
            
            all_detections = []
            frame_count = 0
            process_every_n_frames = 5 # Optimization
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Check if we should process this frame
                if frame_count % process_every_n_frames == 0:
                    detections = run_inference(frame, output_path=None)
                    
                    # If this frame has relevant detections, save it
                    if detections:
                        frame_img_name = f"frame_{file_id}_{frame_count}.jpg"
                        frame_img_path = os.path.join(RESULTS_DIR, frame_img_name)
                        # Save the frame *with annotations*? Or raw?
                        # Usually user wants to see the evidence. 
                        # run_inference returns pure records without modifying the frame in-place (mostly).
                        # Let's verify run_inference side effects.
                        # It draws on 'img' which is a copy in the function, but doesn't return it.
                        # So 'frame' here is clean.
                        # We should draw on a copy for the saved image.
                        
                        evidence_frame = frame.copy()
                        for d in detections:
                            bbox = d['bbox']
                            label = d['violation_type']
                            conf = d['confidence']
                            color = (0, 255, 0)
                            if label.lower() in ['littering', 'smoke']:
                                color = (0, 0, 255)
                            cv2.rectangle(evidence_frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
                            cv2.putText(evidence_frame, f"{label} {conf}", (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                            if d.get('license_plate') != "N/A":
                                 cv2.putText(evidence_frame, f"Plate: {d['license_plate']}", (bbox[0], bbox[3]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                                 
                        cv2.imwrite(frame_img_path, evidence_frame)
                        
                        # Add frame info to detections
                        for d in detections:
                            d['frame'] = frame_count
                            d['timestamp'] = frame_count / fps
                            d['frame_image_url'] = f"http://localhost:8000/results/{frame_img_name}"
                            all_detections.append(d)
                        
                    # Also draw on the video frame (which is used for the video file)
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
    # 1. Get the records to be deleted
    records = history_manager.get_records_by_ids(ids)
    
    # 2. Delete the physical files
    deleted_files_count = 0
    for record in records:
        try:
            # Delete original uploaded file
            original_filename = record.get("original_file")
            if original_filename:
                original_path = os.path.join(UPLOAD_DIR, original_filename)
                if os.path.exists(original_path):
                    os.remove(original_path)
                    deleted_files_count += 1

            # Delete annotated image/video
            annotated_url = record.get("annotated_image_url") or record.get("annotated_video_url")
            if annotated_url:
                # Extract filename from URL (http://localhost:8000/results/filename)
                annotated_filename = annotated_url.split("/")[-1]
                annotated_path = os.path.join(RESULTS_DIR, annotated_filename)
                if os.path.exists(annotated_path):
                    os.remove(annotated_path)
                    deleted_files_count += 1
                    
        except Exception as e:
            print(f"Error deleting files for record {record.get('id')}: {e}")

    # 3. Delete from history JSON
    count = history_manager.delete_records(ids)
    return {"message": f"Deleted {count} records and {deleted_files_count} files"}

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
