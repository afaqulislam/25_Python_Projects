import streamlit as st
import re
import random
import string

st.set_page_config(
    page_title="Password Strength Meter", page_icon="🔒", layout="centered"
)

COMMON_PASSWORDS = {
    "password",
    "123456",
    "qwerty",
    "admin",
    "welcome",
    "password123",
    "abc123",
    "letmein",
    "monkey",
    "1234567890",
}

# Precompile regexes
re_upper = re.compile(r"[A-Z]")
re_lower = re.compile(r"[a-z]")
re_digit = re.compile(r"\d")
re_special = re.compile(
    r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]"
)  # expanded special chars
re_repeat = re.compile(r"(.)\1{2,}")


def has_sequential_chars(password, seq_len=3):
    """Check for ascending sequential letters or digits of length seq_len"""
    password = password.lower()
    for i in range(len(password) - seq_len + 1):
        segment = password[i : i + seq_len]
        # Check if segment is sequential letters
        if all(
            ord(segment[j]) + 1 == ord(segment[j + 1]) for j in range(len(segment) - 1)
        ):
            return True
        # Check if segment is sequential digits
        if segment.isdigit() and all(
            int(segment[j]) + 1 == int(segment[j + 1]) for j in range(len(segment) - 1)
        ):
            return True
    return False


def check_password_strength(password):
    score = 0
    feedback = []

    if password.lower() in COMMON_PASSWORDS:
        feedback.append(
            "❌ This is a commonly used password and can be easily guessed."
        )
        return 0, feedback

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    if len(password) >= 12:
        score += 1

    if re_upper.search(password) and re_lower.search(password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    if re_digit.search(password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    if re_special.search(password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (e.g. !@#$%^&*).")

    if has_sequential_chars(password):
        score -= 1
        feedback.append("❌ Avoid sequential letters or numbers (like 'abc' or '123').")

    if re_repeat.search(password):
        score -= 1
        feedback.append("❌ Avoid repeating characters (like 'aaa').")

    score = max(0, score)
    return score, feedback


def generate_password(
    length=12,
    include_upper=True,
    include_lower=True,
    include_digits=True,
    include_special=True,
):
    """Generate a strong random password ensuring at least one char from each selected category"""
    categories = []
    if include_upper:
        categories.append(string.ascii_uppercase)
    if include_lower:
        categories.append(string.ascii_lowercase)
    if include_digits:
        categories.append(string.digits)
    if include_special:
        categories.append("!@#$%^&*()_+-=[]{}|;:',.<>?")

    if not categories:
        categories = [string.ascii_letters + string.digits]

    # Ensure at least one from each category
    password_chars = [random.choice(cat) for cat in categories]

    all_chars = "".join(categories)
    remaining_length = length - len(password_chars)
    password_chars += [random.choice(all_chars) for _ in range(remaining_length)]

    random.shuffle(password_chars)
    return "".join(password_chars)


# --- Streamlit UI ---

st.title("🔒 Password Strength Meter")
st.markdown("Check how strong your password is and get suggestions to improve it.")

# Show/hide password toggle
show_password = st.checkbox("Show Password")

password = st.text_input(
    "Enter your password:",
    value="",
    type="default" if show_password else "password",
    key="hidden_password",
)

if password:
    score, feedback = check_password_strength(password)
    strength_labels = ["Weak", "Moderate", "Strong"]
    if score >= 5:
        strength = strength_labels[2]
        color = "#16a34a"  # green
        emoji = "✅"
    elif score >= 3:
        strength = strength_labels[1]
        color = "#f59e0b"  # orange
        emoji = "⚠️"
    else:
        strength = strength_labels[0]
        color = "#dc2626"  # red
        emoji = "❌"

    st.markdown(
        f"### Password Strength: <span style='color:{color}; font-weight:bold;'>{emoji} {strength}</span>",
        unsafe_allow_html=True,
    )

    # Colorful progress bar
    progress = score / 5
    st.markdown(
        f"""
        <div style="background-color:#e5e7eb; border-radius:8px; height:20px; width:100%;">
            <div style="background-color:{color}; height:20px; border-radius:8px; width:{progress*100}%; transition: width 0.5s;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Feedback
    if feedback:
        st.subheader("Feedback:")
        for item in feedback:
            st.markdown(f"- {item}")
    else:
        st.success("✅ Excellent! Your password meets all security criteria.")

    # Stats
    st.subheader("Password Statistics:")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Length: {len(password)} characters")
        st.info(f"Uppercase letters: {len(re_upper.findall(password))}")
    with col2:
        st.info(f"Lowercase letters: {len(re_lower.findall(password))}")
        st.info(f"Special characters: {len(re_special.findall(password))}")

    # Estimated time to crack (simple heuristic)
    complexity = 0
    if re_lower.search(password):
        complexity += 26
    if re_upper.search(password):
        complexity += 26
    if re_digit.search(password):
        complexity += 10
    if re_special.search(password):
        complexity += len("!@#$%^&*()_+-=[]{}|;:',.<>?")

    if complexity > 0:
        combos = complexity ** len(password)
        if combos < 1e6:
            crack_time = "Seconds to minutes"
        elif combos < 1e10:
            crack_time = "Hours to days"
        elif combos < 1e13:
            crack_time = "Months"
        else:
            crack_time = "Years to centuries"

        st.warning(f"Estimated time to crack: **{crack_time}**")

# Password generator section
st.markdown("---")
st.subheader("🔄 Password Generator")
st.markdown("Need a strong password? Generate one below:")

col1, col2 = st.columns(2)
with col1:
    length = st.slider("Password Length", min_value=8, max_value=30, value=12)
    include_upper = st.checkbox("Include Uppercase Letters", value=True)
    include_lower = st.checkbox("Include Lowercase Letters", value=True)
with col2:
    include_digits = st.checkbox("Include Numbers", value=True)
    include_special = st.checkbox("Include Special Characters", value=True)

if st.button("Generate Strong Password"):
    generated_password = generate_password(
        length, include_upper, include_lower, include_digits, include_special
    )
    st.code(generated_password, language="plaintext")

    gen_score, gen_feedback = check_password_strength(generated_password)
    progress = gen_score / 5
    color = "#16a34a" if gen_score >= 5 else "#f59e0b" if gen_score >= 3 else "#dc2626"
    st.markdown(
        f"""
        <div style="background-color:#e5e7eb; border-radius:8px; height:20px; width:100%; margin-top:10px;">
            <div style="background-color:{color}; height:20px; border-radius:8px; width:{progress*100}%; transition: width 0.5s;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if gen_score >= 5:
        st.success("✅ Generated a strong password!")
    else:
        st.warning("⚠️ Try adjusting the options to generate a stronger password.")
