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
        
        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                self.user_controls["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY") 
                
                model_options = self.config.get_groq_model_options()
                # Added index=0 to load the first model by default
                self.user_controls["selected_groq_model"] = st.selectbox(
                    "Select Model", 
                    model_options, 
                    index=0
                )
                
            try:
                default_index = usecase_options.index("English")
            except ValueError:
                default_index = 0 

            self.user_controls["selected_language"] = st.selectbox(
                "Select Language", 
                usecase_options, 
                index=default_index
            )
            
            # These will print to your terminal every time the UI re-renders
            print(f"Language: {self.user_controls['selected_language']}")
            print(f"LLM: {self.user_controls['selected_llm']}")
                
        return self.user_controls