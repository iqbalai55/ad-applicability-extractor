from agent.extraction_agent import parse_ad

FAA_AD_2025_23_53_PARSED_AD = parse_ad(r"pdf\EASA_AD_US-2025-23-53_1.pdf")
EASA_AD_2025_0254_PARSED_AD = parse_ad(r"pdf\EASA_AD_2025-0254R1_1.pdf")

DATASET = [
    {
        "input": {
            "aircraft_model": "MD-11F",
            "msn": 48400,
            "modifications": "None",
        },
        "expected": {
            "FAA_AD_2025_23_53": "Affected",
            "EASA_AD_2025_0254": "Not affected",
        },
    },
    {
        "input": {
            "aircraft_model": "A320-214",
            "msn": 4500,
            "modifications": "mod 24591 (production)",
        },
        "expected": {
            "FAA_AD_2025_23_53": "Not affected",
            "EASA_AD_2025_0254": "Not affected",
        },
    },
    {
        "input": {
            "aircraft_model": "A320-214",
            "msn": 4500,
            "modifications": "None",
        },
        "expected": {
            "FAA_AD_2025_23_53": "Not affected",
            "EASA_AD_2025_0254": "Affected",
        },
    },
]

def is_aircraft_affected(parsed_ad, aircraft_model: str, msn: int, modifications: str) -> str:
    """Determine if the aircraft is affected by the AD."""
    rules = parsed_ad.applicability_rules

    # Check aircraft model
    if aircraft_model not in rules.aircraft_models:
        return "Not affected"

    # Check serial number constraints
    if rules.msn_constraints and isinstance(rules.msn_constraints, list):
        if str(msn) not in rules.msn_constraints:
            return "Not affected"

    # Check excluded modifications
    for excluded_mod in rules.excluded_if_modifications:
        if excluded_mod.lower() in modifications.lower():
            return "Not affected"

    # Check required modifications
    if rules.required_modifications:
        for required_mod in rules.required_modifications:
            if required_mod.lower() not in modifications.lower():
                return "Not affected"

    return "Affected"

if __name__ == "__main__":

    # Evaluate dataset
    for i, sample in enumerate(DATASET, 1):
        aircraft = sample["input"]
        expected = sample["expected"]

        result_faa = is_aircraft_affected(
            FAA_AD_2025_23_53_PARSED_AD,
            aircraft["aircraft_model"],
            aircraft["msn"],
            aircraft["modifications"]
        )
        result_easa = is_aircraft_affected(
            EASA_AD_2025_0254_PARSED_AD,
            aircraft["aircraft_model"],
            aircraft["msn"],
            aircraft["modifications"]
        )

        print(f"\nTest case #{i}: {aircraft}")
        print(f"FAA_AD_2025_23_53 - Expected: {expected['FAA_AD_2025_23_53']}, Got: {result_faa}")
        print(f"EASA_AD_2025_0254 - Expected: {expected['EASA_AD_2025_0254']}, Got: {result_easa}")

        assert result_faa == expected['FAA_AD_2025_23_53'], "FAA AD test failed!"
        assert result_easa == expected['EASA_AD_2025_0254'], "EASA AD test failed!"

    print("\nAll test cases passed!")


    # Test table
    TEST_TABLE = [
        {"aircraft_model": "MD-11", "msn": 48123, "modifications": "None"},
        {"aircraft_model": "DC-10-30F", "msn": 47890, "modifications": "None"},
        {"aircraft_model": "Boeing 737-800", "msn": 30123, "modifications": "None"},
        {"aircraft_model": "A320-214", "msn": 5234, "modifications": "None"},
        {"aircraft_model": "A320-232", "msn": 6789, "modifications": "mod 24591"},
        {"aircraft_model": "A320-214", "msn": 7456, "modifications": "SB A320-57-1089 Rev 04"},
        {"aircraft_model": "A321-111", "msn": 8123, "modifications": "None"},
        {"aircraft_model": "A321-112", "msn": 364, "modifications": "mod 24977"},
        {"aircraft_model": "A319-100", "msn": 9234, "modifications": "None"},
        {"aircraft_model": "MD-10-10F", "msn": 46234, "modifications": "None"},
    ]

    print("\n--- Aircraft AD Evaluation ---\n")
    for entry in TEST_TABLE:
        result_faa = is_aircraft_affected(
            FAA_AD_2025_23_53_PARSED_AD,
            entry["aircraft_model"],
            entry["msn"],
            entry["modifications"]
        )
        result_easa = is_aircraft_affected(
            EASA_AD_2025_0254_PARSED_AD,
            entry["aircraft_model"],
            entry["msn"],
            entry["modifications"]
        )

        print(f"Aircraft: {entry['aircraft_model']}, MSN: {entry['msn']}, Mod: {entry['modifications']}")
        print(f"  FAA_AD_2025_23_53 -> {result_faa}")
        print(f"  EASA_AD_2025_0254 -> {result_easa}\n")
