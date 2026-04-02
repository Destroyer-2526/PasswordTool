import argparse
from generator import generate
from analyzer import analyze_password
from improver import process_password

parser = argparse.ArgumentParser(description="Advanced Password Generator & Improver (2026 Edition)")
parser.add_argument("-l", "--length", type=int, default=16, help="Password length (default: 16)")
parser.add_argument("-c", "--count", type=int, default=1, help="Number of passwords to generate")
parser.add_argument("-w", "--words", type=int, default=5, help="Number of words for passphrase")
parser.add_argument("--passphrase", action="store_true", help="Generate passphrase instead of random password")
parser.add_argument("--no-upper", action="store_true")
parser.add_argument("--no-lower", action="store_true")
parser.add_argument("--no-digits", action="store_true")
parser.add_argument("--no-symbols", action="store_true")
parser.add_argument("--improve", type=str, help="Analyze a weak password")
parser.add_argument("--copy", action="store_true", help="Copy to clipboard")
parser.add_argument("--save", type=str, help="Save to file")

args = parser.parse_args()

try:
    if args.improve:
        # Improve / Analyze mode
        result = process_password(args.improve)
        print("\n=== Password Analysis ===")
        print(f"Original     : {result['original']}")
        print(f"Strength     : {result['strength']}")
        print(f"Crack Time   : {result.get('crack_time', 'N/A')}")
        print("\nSuggestions:")
        for s in result["suggestions"]:
            print(f"  • {s}")
        print(f"\nRecommendation: {result['recommended_action']}")

    else:
        # Generate mode
        results = []
        for _ in range(max(1, min(args.count, 50))):
            res = generate(
                length=args.length,
                upper=not args.no_upper,
                lower=not args.no_lower,
                digits=not args.no_digits,
                symbols=not args.no_symbols,
                use_passphrase=args.passphrase,
                num_words=args.words
            )
            results.append(res)

        print("\n=== Generated Password(s) ===")
        for r in results:
            print(f"Password : {r['password']}")
            print(f"Type     : {r['type'].capitalize()}")
            print(f"Entropy  : {r['entropy']} bits")
            if r['type'] == "passphrase":
                print(f"Words    : {r.get('num_words', '')}")
            print("-" * 60)

    # Copy & Save (same as before)
    if args.copy:
        try:
            import pyperclip
            text = "\n".join([r["password"] for r in results]) if 'results' in locals() else args.improve
            pyperclip.copy(text)
            print("\n✓ Copied to clipboard!")
        except ImportError:
            print("\nInstall pyperclip for copy support: pip install pyperclip")

    if args.save:
        with open(args.save, "w") as f:
            if 'results' in locals():
                f.write("\n".join([r["password"] for r in results]))
            else:
                f.write(args.improve)
        print(f"\n✓ Saved to {args.save}")

except Exception as e:
    print(f"Error: {e}")