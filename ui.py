import customtkinter as ctk
from generator import generate
from analyzer import analyze_password
from improver import process_password

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Password Generator & Improver")
app.geometry("820x700")

# Variables
password_var = ctk.StringVar()
strength_var = ctk.StringVar(value="Strength: -")
entropy_var = ctk.StringVar(value="Entropy: -")

length_var = ctk.IntVar(value=16)
num_words_var = ctk.IntVar(value=5)

use_upper = ctk.BooleanVar(value=True)
use_lower = ctk.BooleanVar(value=True)
use_digits = ctk.BooleanVar(value=True)
use_symbols = ctk.BooleanVar(value=True)
use_passphrase = ctk.BooleanVar(value=False)

suggested_strong_var = ctk.StringVar()
suggested_phrase_var = ctk.StringVar()

# Functions
def generate_password_ui():
    try:
        if use_passphrase.get():
            result = generate(use_passphrase=True, num_words=num_words_var.get())
        else:
            result = generate(
                length=length_var.get(),
                upper=use_upper.get(),
                lower=use_lower.get(),
                digits=use_digits.get(),
                symbols=use_symbols.get()
            )
        password_var.set(result["password"])
        update_strength(result["password"])
    except Exception as e:
        password_var.set(f"Error: {e}")

def update_strength(password):
    analysis = analyze_password(password)
    strength_var.set(f"Strength: {analysis['strength']}")
    entropy_var.set(f"Entropy: {analysis['entropy']} bits")

    score = analysis.get("score", 0)
    if score >= 4:
        strength_bar.set(1.0)
        strength_bar.configure(progress_color="green")
    elif score >= 3:
        strength_bar.set(0.85)
        strength_bar.configure(progress_color="#00ff00")
    elif score >= 2:
        strength_bar.set(0.6)
        strength_bar.configure(progress_color="yellow")
    else:
        strength_bar.set(0.3)
        strength_bar.configure(progress_color="red")

def copy_password():
    text = password_var.get().strip()
    if text:
        app.clipboard_clear()
        app.clipboard_append(text)

def analyze_improver():
    weak = input_entry.get().strip()
    if not weak:
        suggestion_text.delete("1.0", "end")
        suggestion_text.insert("1.0", "Please enter a weak password first.")
        return

    result = process_password(weak)

    suggestion_text.delete("1.0", "end")
    suggestion_text.insert("1.0", f"Analyzed Strength: {result['strength']}\n\n")
    suggestion_text.insert("end", "Suggestions:\n")
    for s in result["suggestions"]:
        suggestion_text.insert("end", f"• {s}\n")
    suggestion_text.insert("end", f"\nRecommendation:\n{result['recommended_action']}")

    # Show fresh strong suggestions
    suggested_strong_var.set(result["suggested_strong"])
    suggested_phrase_var.set(result["suggested_passphrase"])

# ===================== GUI =====================
tabs = ctk.CTkTabview(app)
tabs.pack(fill="both", expand=True, padx=20, pady=20)

# Generator Tab
gen = tabs.add("Generator")
ctk.CTkLabel(gen, text="Password Generator", font=("Arial", 24, "bold")).pack(pady=20)

out_frame = ctk.CTkFrame(gen)
out_frame.pack(fill="x", padx=30, pady=10)
output = ctk.CTkTextbox(out_frame, height=80)
output.pack(fill="x", padx=10, pady=5, side="left", expand=True)
ctk.CTkButton(out_frame, text="Copy", command=copy_password).pack(side="right", padx=10)

password_var.trace_add("write", lambda *a: (output.delete("1.0","end"), output.insert("1.0", password_var.get())))

ctk.CTkLabel(gen, textvariable=strength_var).pack(pady=8)
strength_bar = ctk.CTkProgressBar(gen, width=520)
strength_bar.pack(pady=8)
strength_bar.set(0)
ctk.CTkLabel(gen, textvariable=entropy_var).pack(pady=8)

ctk.CTkCheckBox(gen, text="Generate Passphrase (Recommended)", variable=use_passphrase).pack(pady=15)

len_frame = ctk.CTkFrame(gen)
len_frame.pack(fill="x", padx=40, pady=10)
ctk.CTkLabel(len_frame, text="Length:").pack(side="left", padx=10)
ctk.CTkSlider(len_frame, from_=12, to=32, variable=length_var).pack(side="left", fill="x", expand=True, padx=10)
ctk.CTkLabel(len_frame, textvariable=length_var).pack(side="left")

opt = ctk.CTkFrame(gen)
opt.pack(pady=15)
ctk.CTkCheckBox(opt, text="Uppercase", variable=use_upper).grid(row=0, column=0, padx=25)
ctk.CTkCheckBox(opt, text="Lowercase", variable=use_lower).grid(row=0, column=1, padx=25)
ctk.CTkCheckBox(opt, text="Digits", variable=use_digits).grid(row=1, column=0, padx=25)
ctk.CTkCheckBox(opt, text="Symbols", variable=use_symbols).grid(row=1, column=1, padx=25)

ctk.CTkButton(gen, text="Generate", height=55, font=("Arial", 18, "bold"),
              command=generate_password_ui).pack(pady=30, padx=60, fill="x")

# Improvements Tab
imp = tabs.add("Improvements")
ctk.CTkLabel(imp, text="Password Improver", font=("Arial", 24, "bold")).pack(pady=20)

input_entry = ctk.CTkEntry(imp, placeholder_text="Enter weak password here...", height=45)
input_entry.pack(pady=15, padx=40, fill="x")

suggestion_text = ctk.CTkTextbox(imp, height=160)
suggestion_text.pack(pady=15, padx=40, fill="x")

ctk.CTkLabel(imp, text="Suggested Strong Random Password:").pack(anchor="w", padx=40, pady=(15,5))
ctk.CTkEntry(imp, textvariable=suggested_strong_var, height=40).pack(pady=5, padx=40, fill="x")

ctk.CTkLabel(imp, text="Suggested Passphrase:").pack(anchor="w", padx=40, pady=(15,5))
ctk.CTkEntry(imp, textvariable=suggested_phrase_var, height=40).pack(pady=5, padx=40, fill="x")

ctk.CTkButton(imp, text="Analyze & Get Strong Recommendation", 
              height=50, font=("Arial", 15, "bold"),
              command=analyze_improver).pack(pady=30, padx=80, fill="x")

app.mainloop()