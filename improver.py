from analyzer import analyze_password
from generator import generate

def process_password(weak_password: str):
    """Professional Improver - Honest analysis + strong recommendation"""
    if not weak_password or len(weak_password.strip()) == 0:
        return {
            "strength": "Very Weak",
            "suggestions": ["Please enter a password to analyze"],
            "recommended_action": "Enter a weak password above to see detailed analysis.",
            "suggested_strong": ""
        }

    # Get realistic analysis
    analysis = analyze_password(weak_password)

    # Generate a fresh strong password (completely new, not based on weak one)
    strong_result = generate(length=18, upper=True, lower=True, digits=True, symbols=True)
    
    # Generate a passphrase option as well
    passphrase_result = generate(use_passphrase=True, num_words=5)

    suggestions = analysis.get("suggestions", [])
    if not suggestions:
        suggestions = ["This password is too simple or common"]

    return {
        "strength": analysis["strength"],
        "suggestions": suggestions,
        "recommended_action": "⚠️ Best Security Practice:\n"
                              "Do NOT try to modify or 'improve' weak passwords.\n"
                              "Always generate a completely new strong password or memorable passphrase.",
        "suggested_strong": strong_result["password"],
        "suggested_passphrase": passphrase_result["password"]
    }