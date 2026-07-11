import streamlit as st
import yaml
from prompt_hub.adapters import get_adapter

st.set_page_config(page_title="Prompt-Hub", layout="wide")

st.title("Prompt-Hub")

with open("prompts/manifest.yaml", "r", encoding="utf-8") as f:
    manifest = yaml.safe_load(f)

provider = st.selectbox("Model provider", ["mock", "openai"], index=0)
adapter = get_adapter(provider)

for item in manifest.get("prompts", []):
    st.header(item.get("id"))
    st.write("Prompt:")
    st.code(item.get("prompt"))
    if st.button(f"Run {item.get('id')}"):
        try:
            resp = adapter.generate(item.get("prompt"), seed=item.get("seed"))
            st.success(resp)
        except Exception as e:
            st.error(str(e))