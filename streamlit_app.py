# streamlit_app.py
import os
from dotenv import load_dotenv
import pycountry
import streamlit as st
from openai import OpenAI

load_dotenv()  

st.set_page_config(page_title=" 🍽️ Restaurant Name And Menu Generator", layout="wide")
st.title(" 🍽️ Restaurant Name And Menu Generator")

KEY = os.getenv("OPENROUTER_API_KEY") 

MODEL = os.getenv("OPENROUTER_MODEL", "gpt-3.5-turbo")

client = OpenAI(api_key=KEY, base_url="https://openrouter.ai/api/v1")

# --- Countries (sidebar) ---
COUNTRIES = sorted([c.name for c in pycountry.countries])
st.sidebar.header("Pick a cuisine")
country = st.sidebar.selectbox(
    "Country (searchable)",
    COUNTRIES,
    index=COUNTRIES.index("India") if "India" in COUNTRIES else 0,
)

MENU_ITEMS_COUNT = 5

st.sidebar.markdown("Click **Generate** to make a name + menu.")

if st.button("Generate"):
    # Prompt for name
    name_prompt = f"Give  memorable restaurant name and a one-line tagline for a restaurant serving {country} cuisine."
    resp_name = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": "You are a creative restaurant-naming assistant."},
                  {"role": "user", "content": name_prompt}],
        max_tokens=150,
    )
    name_text = (resp_name.choices[0].message.content or "").strip()


    if not name_text:
        st.warning("Model returned no name. Showing default.")
        name_line = "Sample Restaurant"
        st.subheader("Restaurant name + tagline")
        st.write("Sample Restaurant\nA tasty place")
    else:
        st.subheader("Restaurant name + tagline")
        st.write(name_text)
        lines = [l.strip() for l in name_text.splitlines() if l.strip()]
        name_line = lines[0] if lines else "Sample Restaurant"

    # Prompt for menu (plain text)
    menu_prompt = (
        f"List {MENU_ITEMS_COUNT} attractive menu items for a {country} restaurant named \"{name_line}\". "
        "Return them as a short numbered or bulleted plain-text list, each item a title and one-line description."
    )
    resp_menu = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": "You are an expert menu writer."},
                  {"role": "user", "content": menu_prompt}],
        max_tokens=600,
    )
    menu_text = (resp_menu.choices[0].message.content or "").strip()

    if not menu_text:
        st.warning("Model returned no menu. Showing example.")
        st.subheader(f"Menu for {name_line}")
        st.write("- Example Dish — A tasty example description.")
    else:
        st.subheader(f"Menu for {name_line}")
        # display each non-empty line
        for line in menu_text.splitlines():
            if line.strip():
                st.write(line.strip())

