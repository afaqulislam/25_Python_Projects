import streamlit as st

st.set_page_config(page_title="Mad Libs Generator 🧠")

st.title("📝 Fun Mad Libs Game")
st.write("Fill in the blanks below to generate your custom Mad Libs story!")

# Input fields
adj = st.text_input("Enter an adjective:")
verb1 = st.text_input("Enter a verb:")
verb2 = st.text_input("Enter another verb:")
famous_person = st.text_input("Enter a famous person:")

# Generate button
if st.button("Generate Madlib"):
    if adj and verb1 and verb2 and famous_person:
        madlib = (
            f"Computer programming is so **{adj}**! It makes me so excited all the time because "
            f"I love to **{verb1}**, stay hydrated, and **{verb2}** like I am **{famous_person}**!"
        )

        st.markdown("---")
        st.subheader("🎉 Here's your Madlib:")
        st.markdown(madlib)
    else:
        st.warning("Please fill in all fields before generating your Madlib.")
