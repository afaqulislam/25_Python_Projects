import streamlit as st
import random
from words import words


# Helper to pick a valid word
def get_valid_word(words):
    word = random.choice(words)
    while "_" in word or " " in word:
        word = random.choice(words)
    return word.lower()


# Initialize session state variables
if "word" not in st.session_state:
    st.session_state.word = get_valid_word(words)
    st.session_state.word_letters = set(st.session_state.word)
    st.session_state.used_letters = set()
    st.session_state.lives = 6
    st.session_state.game_over = False
    st.session_state.message = ""

# Title
st.title("🎮 Hangman Game with Streamlit")
st.markdown("Guess the word by choosing letters below. You have 6 lives!")

# Show game status
display_word = [
    letter if letter in st.session_state.used_letters else "_"
    for letter in st.session_state.word
]
st.write("### Word: ", " ".join(display_word))
st.write(f"**Lives left:** {st.session_state.lives}")
st.write("**Used letters:** ", " ".join(sorted(st.session_state.used_letters)))
st.markdown("---")

# Letter input
cols = st.columns(13)
alphabet = "abcdefghijklmnopqrstuvwxyz"
for idx, letter in enumerate(alphabet):
    with cols[idx % 13]:
        if st.button(
            letter.upper(),
            key=letter,
            disabled=st.session_state.game_over
            or letter in st.session_state.used_letters,
        ):
            st.session_state.used_letters.add(letter)

            if letter in st.session_state.word_letters:
                st.session_state.word_letters.remove(letter)
                st.session_state.message = f"✅ Good job! '{letter}' is in the word."
            else:
                st.session_state.lives -= 1
                st.session_state.message = f"❌ Oops! '{letter}' is not in the word."

# Check for game over
if st.session_state.lives <= 0:
    st.session_state.game_over = True
    st.error(f"💀 Game Over! You lost. The word was: `{st.session_state.word}`.")
elif len(st.session_state.word_letters) == 0:
    st.session_state.game_over = True
    st.success(f"🎉 You won! The word was: `{st.session_state.word}`.")

# Show feedback message
if st.session_state.message:
    st.info(st.session_state.message)

# Reset button
if st.session_state.game_over:
    if st.button("🔁 Play Again"):
        st.session_state.word = get_valid_word(words)
        st.session_state.word_letters = set(st.session_state.word)
        st.session_state.used_letters = set()
        st.session_state.lives = 6
        st.session_state.game_over = False
        st.session_state.message = ""
