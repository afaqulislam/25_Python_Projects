import streamlit as st
import random

st.set_page_config(page_title="Rock Paper Scissors ✊✋✌️")

st.title("✊ Rock - 📄 Paper - ✌️ Scissors Game")
st.write("Choose Rock, Paper, or Scissors and try to beat the computer!")

choices = {"r": "Rock", "p": "Paper", "s": "Scissors"}
choice_keys = list(choices.keys())

# Initialize session state
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0
if "result" not in st.session_state:
    st.session_state.result = ""
if "user_choice" not in st.session_state:
    st.session_state.user_choice = ""
if "computer_choice" not in st.session_state:
    st.session_state.computer_choice = ""

# User makes a choice
user_input = st.radio("Make your choice:", list(choices.values()))

# Map back to 'r', 'p', or 's'
reverse_choices = {v: k for k, v in choices.items()}
user_choice = reverse_choices[user_input]

if st.button("Play"):
    computer_choice = random.choice(choice_keys)

    st.session_state.user_choice = choices[user_choice]
    st.session_state.computer_choice = choices[computer_choice]

    if user_choice == computer_choice:
        st.session_state.result = "🤝 It's a tie!"
    elif (
        (user_choice == "r" and computer_choice == "s")
        or (user_choice == "s" and computer_choice == "p")
        or (user_choice == "p" and computer_choice == "r")
    ):
        st.session_state.result = "🎉 You won!"
        st.session_state.user_score += 1
    else:
        st.session_state.result = "😞 You lost!"
        st.session_state.computer_score += 1

# Display choices and results
if st.session_state.result:
    st.write(f"You chose: **{st.session_state.user_choice}**")
    st.write(f"Computer chose: **{st.session_state.computer_choice}**")
    st.subheader(st.session_state.result)

# Display scores
st.markdown("---")
st.metric("Your Score", st.session_state.user_score)
st.metric("Computer Score", st.session_state.computer_score)

# Reset button
if st.button("Reset Game"):
    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.session_state.result = ""
    st.session_state.user_choice = ""
    st.session_state.computer_choice = ""
    st.success("Game has been reset!")
