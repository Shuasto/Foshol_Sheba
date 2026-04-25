try:
    import reportlab
    print(f"ReportLab version: {reportlab.Version}")
    from reportlab.pdfgen import canvas
    print("Canvas import successful")
except ImportError as e:
    print(f"ImportError: {e}")
import sys
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path}")
