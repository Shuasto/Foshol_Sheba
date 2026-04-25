from weasyprint import HTML
import sys

try:
    HTML(string='<h1>Hello World - টেস্ট</h1>').write_pdf('/tmp/test.pdf')
    print("Success")
except Exception as e:
    print(f"Error: {e}")
