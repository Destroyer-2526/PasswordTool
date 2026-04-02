"""
Modern Password Generator & Improver - Main Test File
Demonstrates all features of the upgraded tool
"""

from generator import generate
from analyzer import analyze_password
from improver import process_password

def main():
    print("=" * 60)
    print("   ADVANCED PASSWORD TOOL (2026 Edition)")
    print("=" * 60)

    # ==================== 1. RANDOM PASSWORD ====================
    print("\n1. Generating Strong Random Password (Default Settings):")
    result1 = generate(length=18, upper=True, lower=True, digits=True, symbols=True)
    
    print(f"   Password : {result1['password']}")
    print(f"   Type     : {result1['type'].capitalize()}")
    print(f"   Length   : {result1['length']} characters")
    print(f"   Entropy  : {result1['entropy']} bits")
    print("-" * 50)

    # ==================== 2. PASSPHRASE ====================
    print("\n2. Generating Strong Passphrase (Recommended):")
    result2 = generate(use_passphrase=True, num_words=6)
    
    print(f"   Passphrase : {result2['password']}")
    print(f"   Type       : {result2['type'].capitalize()}")
    print(f"   Words      : {result2.get('num_words', 6)}")
    print(f"   Entropy    : {result2['entropy']} bits")
    print("-" * 50)

    # ==================== 3. PASSWORD ANALYSIS ====================
    print("\n3. Analyzing a Weak Password ('testpass123'):")
    weak_password = "testpass123"
    analysis = analyze_password(weak_password)
    
    print(f"   Password   : {weak_password}")
    print(f"   Strength   : {analysis['strength']}")
    print(f"   Entropy    : {analysis['entropy']} bits")
    print(f"   Crack Time : {analysis.get('crack_time', 'N/A')}")
    
    print("\n   Suggestions:")
    for suggestion in analysis.get("suggestions", ["No suggestions available"]):
        print(f"     • {suggestion}")

    print("-" * 50)

    # ==================== 4. IMPROVER DEMO ====================
    print("\n4. Using Improver on Weak Password:")
    improver_result = process_password(weak_password)
    
    print(f"   Original   : {improver_result['original']}")
    print(f"   Strength   : {improver_result['strength']}")
    print(f"   Crack Time : {improver_result.get('crack_time', 'N/A')}")
    
    print("\n   Recommendations:")
    for s in improver_result["suggestions"]:
        print(f"     • {s}")
    
    print(f"\n   Final Advice:\n   {improver_result['recommended_action']}")

    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print("Run 'python ui.py' for GUI or 'python cli.py --help' for CLI options.")
    print("=" * 60)


if __name__ == "__main__":
    main()