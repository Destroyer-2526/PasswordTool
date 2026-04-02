import string
import secrets
from entropy import calculate_entropy

# Good wordlist for passphrases (expand if needed)
WORDLIST = [
    "apple", "banana", "correct", "dragon", "elephant", "frozen", "guitar", "happy",
    "island", "jungle", "kite", "lemon", "mountain", "notebook", "ocean", "purple",
    "quiet", "river", "storm", "thunder", "umbrella", "violet", "whisper", "yellow",
    "zebra", "bracket", "lantern", "market", "needle", "orange", "piano", "quilt",
    "rocket", "shadow", "tiger", "unity", "victory", "window", "forest", "garden",
    "harbor", "kingdom", "lighthouse", "mystic", "oasis", "planet", "quest", "rainbow",
    "sunrise", "twilight", "voyage", "waterfall", "zenith"
]

def build_charset(upper=True, lower=True, digits=True, symbols=True):
    chars = ""
    if upper: chars += string.ascii_uppercase
    if lower: chars += string.ascii_lowercase
    if digits: chars += string.digits
    if symbols: chars += "!@#$%^&*()_+-=[]{}|;:,.<>/?~"
    return chars

def generate_random_password(length=16, upper=True, lower=True, digits=True, symbols=True):
    """Generate cryptographically strong random password"""
    chars = build_charset(upper, lower, digits, symbols)
    if not chars:
        raise ValueError("Select at least one character type")

    length = max(12, length)
    password_list = []

    # Guarantee at least one of each selected type
    if upper: password_list.append(secrets.choice(string.ascii_uppercase))
    if lower: password_list.append(secrets.choice(string.ascii_lowercase))
    if digits: password_list.append(secrets.choice(string.digits))
    if symbols: password_list.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>/?~"))

    remaining = length - len(password_list)
    if remaining > 0:
        password_list += [secrets.choice(chars) for _ in range(remaining)]

    secrets.SystemRandom().shuffle(password_list)
    final_password = ''.join(password_list)

    charset_size = len(chars)
    entropy = calculate_entropy(length, charset_size)

    return {
        "password": final_password,
        "length": length,
        "entropy": entropy,
        "type": "random"
    }

def generate_passphrase(num_words=5, separator="-"):
    """Generate strong memorable passphrase (NIST recommended)"""
    num_words = max(4, num_words)
    words = [secrets.choice(WORDLIST) for _ in range(num_words)]
    passphrase = separator.join(words)
    estimated_entropy = round(num_words * 13.0, 2)  # ~13 bits per word

    return {
        "password": passphrase,
        "length": len(passphrase),
        "entropy": estimated_entropy,
        "type": "passphrase",
        "num_words": num_words
    }

# Unified generator
def generate(length=16, upper=True, lower=True, digits=True, symbols=True,
             use_passphrase=False, num_words=5):
    if use_passphrase:
        return generate_passphrase(num_words)
    return generate_random_password(length, upper, lower, digits, symbols)