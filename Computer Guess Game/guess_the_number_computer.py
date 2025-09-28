import streamlit as st
import random

st.set_page_config(page_title="Computer Guesses Your Number", page_icon="🎯")
st.title("🎯 Computer Guesses Your Number")

# Initialize session state
if "low" not in st.session_state:
    st.session_state.low = 1
if "high" not in st.session_state:
    st.session_state.high = None
if "guess" not in st.session_state:
    st.session_state.guess = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "finished" not in st.session_state:
    st.session_state.finished = False


def start_game():
    st.session_state.low = 1
    st.session_state.high = st.session_state.max_number
    st.session_state.guess = random.randint(st.session_state.low, st.session_state.high)
    st.session_state.feedback = None
    st.session_state.game_started = True
    st.session_state.finished = False


# Input to start the game
if not st.session_state.game_started:
    st.subheader("Set the Maximum Number")
    st.session_state.max_number = st.number_input(
        "Maximum number:", min_value=1, value=100
    )
    if st.button("Start Game"):
        start_game()

# Game loop UI
elif st.session_state.game_started and not st.session_state.finished:
    st.subheader("Think of a number... Don't tell me!")
    st.write(f"My guess is: **{st.session_state.guess}**")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔼 Too High"):
            st.session_state.high = st.session_state.guess - 1
    with col2:
        if st.button("🔽 Too Low"):
            st.session_state.low = st.session_state.guess + 1
    with col3:
        if st.button("✅ Correct!"):
            st.success(f"Yay! I guessed your number: {st.session_state.guess} 🎉")
            st.session_state.finished = True

    # Check if the range is invalid
    if st.session_state.low > st.session_state.high and not st.session_state.finished:
        st.error("⚠️ Hmm, your responses are inconsistent. Let's restart.")
        st.session_state.game_started = False

    # Update guess
    elif not st.session_state.finished:
        st.session_state.guess = random.randint(
            st.session_state.low, st.session_state.high
        )

# Restart game
if st.session_state.game_started or st.session_state.finished:
    if st.button("🔁 Play Again"):
        for key in ["low", "high", "guess", "feedback", "game_started", "finished"]:
            st.session_state.pop(key, None)
        st.rerun()
