import re
import json
from schema.ad_schema import ApplicabilityRules, ADModel
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from utils.llm_config import get_chat_model
from utils.file_processor import process_uploaded_file

APPLICABILITY_PROMPT = PromptTemplate(
    template="""
You are an expert in Aviation ADs. Extract aircraft models and modifications into structured JSON.

Rules:

1. aircraft_models:
   - Only include **model codes** (e.g., 'MD-11', 'MD-10-10F', 'A320-211').
   - Remove manufacturer names or prefixes (e.g., 'Boeing Model', 'Airbus').
   - If multiple models are in parentheses, split into separate entries:
     Example: 'MODEL-X (MODEL-Y and MODEL-Z)' → ['MODEL-X', 'MODEL-Y', 'MODEL-Z'].

2. msn_constraints:
   - Include only serial number constraints if explicitly listed.
   - Use null if "all MSN" or not limited.

3. excluded_if_modifications:
   - Include only **exact mod/SB codes**, removing extra words:
     - 'manufacturer modification (mod) 12345' → 'mod 12345'
     - 'Service Bulletin (SB) XYZ-01 at Revision 02' → 'SB XYZ-01 Rev 02'
   - Always convert "Revision" → "Rev".

4. required_modifications:
   - Same as excluded_if_modifications.

AD Applicability Section:
{section_text}

{format_instructions}
""",
    input_variables=["section_text"],
    partial_variables={"format_instructions": "{format_instructions}"}
)

class ApplicabilityAgent:
    def __init__(self):
        self.llm = get_chat_model()
        self.parser = JsonOutputParser(pydantic_object=ApplicabilityRules)
        
        self.prompt = APPLICABILITY_PROMPT.partial(
            format_instructions=self.parser.get_format_instructions()
        )
        self.chain = self.prompt | self.llm | self.parser

    def parse_section(self, section_text: str) -> ApplicabilityRules:
        """Parse a raw Applicability section and return structured data."""
        try:
            result = self.chain.invoke({"section_text": section_text})

            # Print structured output for debugging
            #print("\n--- [STRUCTURED APPLICABILITY OUTPUT] ---")
            #print(json.dumps(result, indent=2))

            return result
        except Exception as e:
            raise RuntimeError(f"ApplicabilityAgent failed: {str(e)}") from e

    def process_ad(self, ad_id: str, section_text: str) -> ADModel:
        """Parse Applicability section and return a full ADModel."""
        try:
            rules = self.parse_section(section_text)
            return ADModel(ad_id=ad_id, applicability_rules=rules)
        except Exception as e:
            # Fallback in case LLM fails
            print(f"[WARNING] LLM failed to parse Applicability section: {e}")
            fallback_rules = ApplicabilityRules(
                aircraft_models=[],
                msn_constraints=None,
                excluded_if_modifications=[],
                required_modifications=[]
            )
            return ADModel(ad_id=ad_id, applicability_rules=fallback_rules)
        
def extract_applicability_section(text: str) -> str:
    """
    Extract the raw text of the Applicability section from an AD text,
    only if 'Applicability' appears at the start of a line.
    """
    match = re.search(r"(?:^|\n).{0,5}?Applicability.{0,3}\n(.*?)(?:\n\n|\Z)", text, re.DOTALL | re.IGNORECASE)
    if not match:
        raise ValueError("Applicability section not found")

    section_text = match.group(0).strip()
    return section_text


def parse_ad(file_path: str) -> ADModel:
    """
    Parse an AD file and return an ADModel.
    Extracts the Applicability section and uses the LLM agent.
    """
    # Extract file content
    ad_id, ad_text = process_uploaded_file(file_path)

    # Use ApplicabilityAgent to parse the section and return full ADModel
    agent = ApplicabilityAgent()
    section_text = extract_applicability_section(ad_text)
    return agent.process_ad(ad_id, section_text)
