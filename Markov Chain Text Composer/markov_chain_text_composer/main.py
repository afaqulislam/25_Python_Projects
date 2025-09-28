import markovify
import os

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Read the input lyrics
try:
    with open("data/lyrics.txt", "r", encoding="utf-8") as file:
        text = file.read()
except FileNotFoundError:
    print("❌ lyrics.txt not found in /data folder.")
    exit()

# Build Markov model
model = markovify.Text(text)

# Number of lines to generate
num_lines = 5

# Prepare output file
output_path = "output/generated.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("🎶 Generated Lyrics:\n\n")

print("🎤 Generated Lyrics:\n")

# Generate sentences
for i in range(num_lines):
    sentence = model.make_sentence()

    # Fallback if no full sentence can be generated
    if sentence is None:
        sentence = model.make_short_sentence(100)

    # Final fallback
    if sentence is None:
        sentence = "[Could not generate a sentence]"

    print(f"{i+1}. {sentence}")

    # Write to file
    with open(output_path, "a", encoding="utf-8") as f:
        f.write(f"{i+1}. {sentence}\n")
