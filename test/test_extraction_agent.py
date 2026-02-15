import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.extraction_agent import parse_ad
from schema.ad_schema import ApplicabilityRules, ADModel

def compare_ad_models(parsed_ad: ADModel, expected_ad: ADModel):
    """
    Compare the applicability_rules of two ADModel objects.
    Prints detailed differences if they do not match.
    """
    parsed = parsed_ad.applicability_rules
    expected = expected_ad.applicability_rules

    # Compare fields
    aircraft_ok = set(parsed.aircraft_models) == set(expected.aircraft_models)
    msn_ok = parsed.msn_constraints == expected.msn_constraints
    excluded_ok = set(parsed.excluded_if_modifications) == set(expected.excluded_if_modifications)
    required_ok = set(parsed.required_modifications) == set(expected.required_modifications)

    if aircraft_ok and msn_ok and excluded_ok and required_ok:
        print("Test passed!")
    else:
        print("Test failed!")
        print("\nExpected ADModel:")
        print(expected_ad)
        print("\nParsed ADModel:")
        print(parsed_ad)

        # Detailed differences for aircraft models
        missing_models = set(expected.aircraft_models) - set(parsed.aircraft_models)
        extra_models = set(parsed.aircraft_models) - set(expected.aircraft_models)
        if missing_models:
            print("Missing aircraft models:", missing_models)
        if extra_models:
            print("Unexpected extra aircraft models:", extra_models)

EASA_AD_2025_0254_EXPECTED_RULES = ApplicabilityRules(
    aircraft_models=[
        "MD-11",
        "MD-11F",
        "MD-10-10F",
        "MD-10-30F",
        "DC-10-10",
        "DC-10-10F",
        "KC-10A",
        "KDC-10",
        "DC-10-15",
        "DC-10-30",
        "DC-10-30F",
        "DC-10-40",
        "DC-10-40F"
    ],
    msn_constraints=None,
    excluded_if_modifications=[],
    required_modifications=[]
)

EASA_AD_2025_0254_EXPECTED_AD = ADModel(
    ad_id="EASA_AD_US-2025-23-53_1",
    applicability_rules=EASA_AD_2025_0254_EXPECTED_RULES
)

EASA_AD_2025_0254_PARSED_AD = parse_ad(r"pdf\EASA_AD_US-2025-23-53_1.pdf")

print(EASA_AD_2025_0254_PARSED_AD)
print("EASA_AD_2025_0254", compare_ad_models(
    parsed_ad=EASA_AD_2025_0254_PARSED_AD,
    expected_ad=EASA_AD_2025_0254_EXPECTED_AD
))

FAA_AD_AIRBUS_EXPECTED_RULES = ApplicabilityRules(
    aircraft_models=[
        "A320-211",
        "A320-212",
        "A320-214",
        "A320-215",
        "A320-216",
        "A320-231",
        "A320-232",
        "A320-233",
        "A321-111",
        "A321-112",
        "A321-131"
    ],
    msn_constraints=None, 
    excluded_if_modifications=["mod 24591", "SB A320-57-1089 Rev 04", "mod 24977"],  
    required_modifications=[]  
)

FAA_AD_AIRBUS_EXPECTED_RULES_AD = ADModel(
    ad_id="EASA_AD_2025-0254R1_1",
    applicability_rules=FAA_AD_AIRBUS_EXPECTED_RULES
)

FAA_AD_AIRBUS_PARSED_AD = parse_ad(r"pdf\EASA_AD_2025-0254R1_1.pdf")


print(FAA_AD_AIRBUS_PARSED_AD)
print("EASA_AD_2025_0254", compare_ad_models(
    parsed_ad=FAA_AD_AIRBUS_PARSED_AD,
    expected_ad=FAA_AD_AIRBUS_EXPECTED_RULES_AD
))