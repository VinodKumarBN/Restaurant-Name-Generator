# streamlit_app.py (minimal)
import os
import streamlit as st
import pycountry
from openai import OpenAI

st.set_page_config(page_title="Restaurant Name And Menu Generator", layout="wide")
st.title("🍽️ Restaurant Name And Menu Generator")

KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "gpt-3.5-turbo")

client = OpenAI(api_key=KEY, base_url="https://openrouter.ai/api/v1")

COUNTRIES = sorted([c.name for c in pycountry.countries])
country = st.sidebar.selectbox("Pick a cuisine (country)", COUNTRIES, index=COUNTRIES.index("India") if "India" in COUNTRIES else 0)

MENU_ITEMS_COUNT = 5

if st.button("Generate"):
    # name + tagline
    name_prompt = f"Give 1 memorable restaurant name and a one-line tagline for a restaurant serving {country} cuisine."
    resp_name = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": name_prompt}],
        max_tokens=150,
    )
    name_text = resp_name.choices[0].message.content
    #st.sidebar("Restaurant name + tagline")
    st.write(name_text)

    name_line = name_text.splitlines()[0].strip()

    
    menu_prompt = (
        f"List {MENU_ITEMS_COUNT} attractive menu items for a {country} restaurant named \"{name_line}\". "
        "Return them as a short numbered or bulleted plain-text list, each item a title and one-line description."
    )
    resp_menu = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": menu_prompt}],
        max_tokens=600,
    )
    menu_text = resp_menu.choices[0].message.content
    st.subheader(f"🍱 Menu for {name_line}")
    st.write(menu_text)


