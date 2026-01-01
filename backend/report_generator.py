from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os
from datetime import datetime

def generate_pdf_report(record, output_path):
    """
    Generates a PDF report for a detection record.
    """
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "EcoScout Detection Report")
    
    # Timestamp
    c.setFont("Helvetica", 12)
    timestamp_str = record.get('timestamp', datetime.now().isoformat())
    try:
        dt = datetime.fromisoformat(timestamp_str)
        formatted_date = dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        formatted_date = timestamp_str
        
    c.drawString(50, height - 80, f"Date: {formatted_date}")
    c.drawString(50, height - 100, f"File ID: {record.get('id', 'N/A')}")
    c.drawString(50, height - 120, f"Original File: {record.get('original_file', 'N/A')}")
    
    # Summary
    detections = record.get('detections', [])
    violation_count = len([d for d in detections if d['violation_type'].lower() in ['littering', 'smoke']])
    c.drawString(50, height - 150, f"Total Detections: {len(detections)}")
    c.setFillColor(colors.red if violation_count > 0 else colors.green)
    c.drawString(200, height - 150, f"Violations Found: {violation_count}")
    c.setFillColor(colors.black)
    
    # Image
    # We need the local path to the annotated image.
    # The record has 'annotated_image_url' or 'annotated_video_url'.
    # We need to resolve this to a local path.
    # Assuming the caller passes the record with enough info or we can derive it.
    # For now, let's try to find the image in the 'results' directory based on the URL or filename.
    
    image_drawn = False
    current_y = height - 180
    
    # Try to find the image file
    # If it's a video, we might not have a static image unless we saved a thumbnail or frame.
    # In main.py, for video, we saved 'annotated_frame_...' for the first frame if we did that logic,
    # but for full video processing we might not have a single image easily accessible unless we saved one.
    # Let's assume for video we might skip the image or use a placeholder if not found.
    
    # Logic to find image path:
    # URL: http://localhost:8000/results/annotated_uuid.jpg
    # Local: results/annotated_uuid.jpg
    
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    
    image_filename = None
    if 'annotated_image_url' in record:
        image_filename = record['annotated_image_url'].split('/')[-1]
    elif 'annotated_video_url' in record:
        # For video, maybe we can't show a moving image. 
        # But wait, in main.py for video we didn't explicitly save a "thumbnail" for the report.
        # We could try to find 'annotated_frame_...' if it exists (from the placeholder logic) 
        # OR just skip image for video reports for now.
        pass
        
    if image_filename:
        image_path = os.path.join(results_dir, image_filename)
        if os.path.exists(image_path):
            try:
                # Resize image to fit
                img = ImageReader(image_path)
                img_width, img_height = img.getSize()
                aspect = img_height / float(img_width)
                
                display_width = 400
                display_height = display_width * aspect
                
                if current_y - display_height < 100:
                    c.showPage()
                    current_y = height - 50
                
                c.drawImage(img, 100, current_y - display_height, width=display_width, height=display_height)
                current_y -= (display_height + 30)
                image_drawn = True
            except Exception as e:
                print(f"Error drawing image: {e}")
                c.drawString(50, current_y, "[Error loading image]")
                current_y -= 30
    
    if not image_drawn:
        c.drawString(50, current_y, "[Image not available for this report]")
        current_y -= 30

    # Detections Table
    if detections:
        data = [['Type', 'Confidence', 'License Plate', 'OCR Conf']]
        for d in detections:
            data.append([
                d.get('violation_type', 'N/A'),
                f"{d.get('confidence', 0)}%",
                d.get('license_plate', 'N/A'),
                f"{d.get('ocr_confidence', 0)}%"
            ])
            
        table = Table(data, colWidths=[100, 80, 150, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        if current_y - (len(data) * 20) < 50:
             c.showPage()
             current_y = height - 50
             
        table.wrapOn(c, width, height)
        table.drawOn(c, 50, current_y - (len(data) * 20))
        
    c.save()
    return output_path
