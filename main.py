import streamlit as st
from utility_functions import load_keys, clean_file, build_prompt, _analyze_with_anthropic

st.title("Contracts...simplified!")
st.markdown(
    """
    Type in a link to a sec.gov contract, press submit, and we will give you a brief summary 
    and some recommended actions items for you and your friends.
    """
)

url = st.text_input("Type in your link here:")

if st.button ("Submit 🎈"): 
    claude_key, workspace_id, headers = load_keys("keys.json")
    cleaned_html = clean_file(url, headers)
    prompt = build_prompt(cleaned_html)
    output_text = _analyze_with_anthropic(prompt, claude_key, workspace_id)
    st.write(output_text)

