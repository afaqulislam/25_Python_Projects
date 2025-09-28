import streamlit as st
from pint import UnitRegistry
import json
import os

# **SET PAGE CONFIG FIRST**
st.set_page_config(page_title="Unit Converter", page_icon="🔄", layout="centered")

# Initialize unit registry
ureg = UnitRegistry()
ureg.define("degC = kelvin; offset: 273.15")
ureg.define("degF = kelvin; offset: 255.372222")

# Define unit categories
unit_categories = {
    "Length": [
        "millimeter",
        "centimeter",
        "meter",
        "kilometer",
        "inch",
        "foot",
        "yard",
        "mile",
    ],
    "Weight": ["kilogram", "gram", "milligram", "pound", "ounce"],
    "Volume": ["liter", "milliliter", "gallon", "quart", "pint"],
    "Temperature": ["degC", "degF", "kelvin"],
    "Speed": ["meter/second", "kilometer/hour", "mile/hour", "foot/second"],
    "Time": ["second", "minute", "hour", "day"],
}

# Load or initialize conversion history
history_file = "conversion_history.json"
if os.path.exists(history_file):
    try:
        with open(history_file, "r") as file:
            conversion_history = json.load(file)
    except json.JSONDecodeError:
        conversion_history = {category: [] for category in unit_categories}
else:
    conversion_history = {category: [] for category in unit_categories}

# **Apply Dark Theme Only**
st.markdown(
    """
    <style>
        body, .stApp {background-color: #121212 !important; color: white !important;}
        h1, h3 {color: white !important;}
        label, .stSelectbox label, .stNumberInput label {color: inherit !important;}
        div.stButton > button {
            background-color: gray !important; color: white !important;
            border-radius: 10px;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: darkgray !important;
        }
        .result-box {
            padding: 10px; 
            border-radius: 10px; 
            text-align: center; 
            font-size: 18px; 
            font-weight: bold;
            background-color: #333333;
            color: white;
        }
        .stSidebar { background-color: #1c1c1c !important; }
        .stSidebar * { color: white !important; }
    </style>
""",
    unsafe_allow_html=True,
)

# Streamlit UI
st.markdown(
    """
    <h1 style='text-align: center;'>🌟 Universal Unit Converter</h1>
    <h3 style='text-align: center;'>Convert values between different units.</h3>
""",
    unsafe_allow_html=True,
)

# Category selection
category = st.selectbox("Select a category", list(unit_categories.keys()))
units = unit_categories[category]

# Unit selection
from_unit = st.selectbox("From", units)
to_unit = st.selectbox("To", units)

# User input
value = st.number_input("Enter value", min_value=0.0, format="%.2f")

# Conversion logic
if st.button("Convert"):
    try:
        if category == "Temperature":
            if from_unit == "degC" and to_unit == "degF":
                result = value * 9 / 5 + 32
            elif from_unit == "degF" and to_unit == "degC":
                result = (value - 32) * 5 / 9
            elif from_unit == "degC" and to_unit == "kelvin":
                result = value + 273.15
            elif from_unit == "kelvin" and to_unit == "degC":
                result = value - 273.15
            elif from_unit == "degF" and to_unit == "kelvin":
                result = (value - 32) * 5 / 9 + 273.15
            elif from_unit == "kelvin" and to_unit == "degF":
                result = (value - 273.15) * 9 / 5 + 32
            else:
                result = value
        else:
            result = (value * ureg(from_unit)).to(to_unit).magnitude

        st.markdown(
            f"""
            <div class='result-box'>
                {value} {from_unit} = {result:.4f} {to_unit}
            </div>
        """,
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.error(f"Conversion error: {e}")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center;'>© 2025 Afaq Ul Islam | Crafted with passion and precision 🚀</p>",
    unsafe_allow_html=True,
)
