import streamlit as st
import os
from dotenv import load_dotenv
from src.ui.streamlitui.uiconfig import Config


class LoadStreamlitUI:
    def __init__(self):
        load_dotenv()
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())

        # Check if blog has already been generated
        blog_generated = st.session_state.get("blog_generated", False)

        with st.sidebar:

            # ── LOCKED STATE: blog already generated ─────────────────
            if blog_generated:
                st.success("✅ Blog generated!")
                st.info(
                    f"📌 **Topic:** {st.session_state.get('blog_topic', '')}\n\n"
                    f"🌐 **Language:** {st.session_state.get('locked_language', 'English')}\n\n"
                    f"🤖 **Model:** {st.session_state.get('locked_model', '')}"
                )
                st.caption("Settings are locked. Click **🔄 New Chat** to start over.")

                # Still return the locked values so app works
                self.user_controls["selected_llm"] = "Groq"
                self.user_controls["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY")
                self.user_controls["selected_groq_model"] = st.session_state.get("locked_model", "llama-3.3-70b-versatile")
                self.user_controls["selected_language"] = st.session_state.get("locked_language", "English")

            # ── UNLOCKED STATE: show full controls ───────────────────
            else:
                llm_options = self.config.get_llm_options()
                language_options = self.config.get_usecase_options()

                self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

                if self.user_controls["selected_llm"] == "Groq":
                    self.user_controls["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY")

                    model_options = self.config.get_groq_model_options()
                    self.user_controls["selected_groq_model"] = st.selectbox(
                        "Select Model", model_options, index=0
                    )

                try:
                    default_index = language_options.index("English")
                except ValueError:
                    default_index = 0

                self.user_controls["selected_language"] = st.selectbox(
                    "Select Language", language_options, index=default_index
                )

                # Lock values into session state so they persist after generation
                st.session_state["locked_language"] = self.user_controls["selected_language"]
                st.session_state["locked_model"] = self.user_controls.get("selected_groq_model", "llama-3.3-70b-versatile")

            # ── ABOUT expander (always visible) ──────────────────────
            st.divider()
            with st.expander("ℹ️ About this app"):
                st.markdown("""
### How it works

This app uses **LangGraph** to build a stateful agentic blog generation pipeline.

**Flow:**
```
Your Topic
    ↓
Title Creation Node
    ↓
Content Generation Node
    ↓
Translation Node (if non-English)
    ↓
Your Blog ✅
```

**Feedback Loop:**
Once a blog is generated, give feedback in the chat and the entire pipeline reruns with your feedback baked into the prompts.

**Tech Stack:**
- 🦜 LangChain + LangGraph
- 🤖 Groq LLM (Llama 3.3 70B)
- 🖥️ Streamlit UI
                """)

        return self.user_controls