import streamlit as st
import random

st.set_page_config(page_title="User Guess Game 🎯")

st.title("🎯 Guess the Number Game")
st.write("Try to guess a number between 1 and a maximum value you choose!")

# Initialize session state variables
if "random_number" not in st.session_state:
    st.session_state.random_number = None
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# User selects range
max_value = st.number_input(
    "Choose the maximum number (greater than 1):", min_value=2, value=10
)

# Start or restart game
if st.button("Start New Game"):
    st.session_state.random_number = random.randint(1, max_value)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.success("Game started! Guess a number below 👇")

# Only show input if game is active
if st.session_state.random_number and not st.session_state.game_over:
    guess = st.number_input(
        "Enter your guess:", min_value=1, max_value=max_value, step=1
    )

    if st.button("Submit Guess"):
        st.session_state.attempts += 1

        if guess < st.session_state.random_number:
            st.warning("Too low. Try again!")
        elif guess > st.session_state.random_number:
            st.warning("Too high. Try again!")
        else:
            st.success(
                f"🎉 Correct! You guessed it in {st.session_state.attempts} attempts."
            )
            st.balloons()
            st.session_state.game_over = True

# Show answer if game is over
if st.session_state.game_over:
    st.info(f"The number was: {st.session_state.random_number}")
