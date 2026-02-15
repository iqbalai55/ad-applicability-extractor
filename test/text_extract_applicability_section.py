import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.file_processor import process_uploaded_file
from agent.extraction_agent import extract_applicability_section

print("=== EASA_AD_2025-0254R1_1 ===\n")
file_name, content = process_uploaded_file(r"pdf\EASA_AD_2025-0254R1_1.pdf")
section = extract_applicability_section(content)
print(section)
print("\n")

print("=== EASA_AD_US-2025-23-53_1 ===\n")
file_name, content = process_uploaded_file(r"pdf\EASA_AD_US-2025-23-53_1.pdf")
section = extract_applicability_section(content)
print(section)
