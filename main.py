import argparse
from agent.extraction_agent import parse_ad
from evaluate import is_aircraft_affected


def main():
    parser = argparse.ArgumentParser(
        description="AD Extraction & Applicability Checker"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # -------- EXTRACT COMMAND --------
    extract_parser = subparsers.add_parser(
        "extract", help="Extract structured data from AD document"
    )
    extract_parser.add_argument(
        "--ad", required=True, help="Path to AD document"
    )

    # -------- CHECK COMMAND --------
    check_parser = subparsers.add_parser(
        "check", help="Check if an aircraft is affected by an AD"
    )
    check_parser.add_argument("--ad", required=True, help="Path to AD document")
    check_parser.add_argument("--model", required=True, help="Aircraft model")
    check_parser.add_argument("--msn", required=True, help="Manufacturer Serial Number")
    check_parser.add_argument("--mod", default="None", help="Modification status (optional)")

    args = parser.parse_args()

    # EXTRACT MODE
    if args.command == "extract":
        ad_data = parse_ad(args.ad)

        print("\n--- Extracted AD Data ---\n")
        print(ad_data)

    # CHECK MODE
    elif args.command == "check":
        ad_data = parse_ad(args.ad)

        result = is_aircraft_affected(
            ad_data,
            aircraft_model=args.model,
            msn=int(args.msn),
            modifications=args.mod
        )

        print("\n--- Applicability Result ---\n")
        if result == "Affected":
            print("The aircraft IS affected by this AD.")
        else:
            print("The aircraft is NOT affected by this AD.")


if __name__ == "__main__":
    main()
