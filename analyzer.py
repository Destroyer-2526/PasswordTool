try:
    from zxcvbn import zxcvbn
    ZXCvBN_AVAILABLE = True
except ImportError:
    ZXCvBN_AVAILABLE = False

from entropy import calculate_entropy

def analyze_password(password: str):
    if not password or len(password.strip()) == 0:
        return {
            "strength": "Very Weak",
            "score": 0,
            "entropy": 0.0,
            "warnings": "Password is empty",
            "suggestions": ["Generate a new strong password or passphrase"],
            "zxcvbn_used": False
        }

    if ZXCvBN_AVAILABLE:
        result = zxcvbn(password)
        score = result["score"]
        strength_map = {0: "Very Weak", 1: "Weak", 2: "Medium", 3: "Strong", 4: "Very Strong"}

        entropy = result.get("entropy", 0.0)
        if entropy == 0.0:
            entropy = calculate_entropy(len(password), 95)

        return {
            "strength": strength_map.get(score, "Unknown"),
            "score": score,
            "entropy": round(entropy, 2),
            "warnings": result.get("feedback", {}).get("warning", ""),
            "suggestions": result.get("feedback", {}).get("suggestions", []),
            "zxcvbn_used": True
        }

    # Fallback
    else:
        entropy = calculate_entropy(len(password), 95)
        score = min(6, len(password) // 3)

        strength = "Very Weak" if score <= 3 else "Weak" if score <= 5 else "Strong"

        return {
            "strength": strength,
            "score": score,
            "entropy": round(entropy, 2),
            "warnings": "",
            "suggestions": ["Use longer passwords or passphrases"],
            "zxcvbn_used": False
        }