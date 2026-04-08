import streamlit as st
from src.ui.streamlitui.loadui import LoadStreamlitUI
from src.llms.groqllm import GroqLLM
from src.graphs.graph_builder import GraphBuilder
from src.ui.streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while
    implementing exception handling for robustness.
    """
    
    ## Load UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    
    # Check if user input loaded successfully
    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
        
    # Chat input box for the user to message the agent
    user_message = st.chat_input("Enter your message:")    
    
    

    if user_message:
        try:
            print(user_input)
            ## Configure The LLM's
            obj_llm_config = GroqLLM(user_controls=user_input)
            model = obj_llm_config.get_llm()
            
            if not model:
                st.error("Error: LLM model could not be initialized")
                return
                
            usecase = user_input.get("selected_language")
            
            ## graph builder

            graph_builder= GraphBuilder(model)
            print(usecase)
            try:
                graph=graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Graph setup fialed - {e}")    
        except Exception as e:
            st.error(f"Error: Graph setup fialed - {e}")  
            return
   