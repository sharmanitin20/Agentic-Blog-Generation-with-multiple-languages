import json
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
import streamlit as st
import time
import json



class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        initial_state = {"topic": self.user_message}
        
        title_placeholder = st.empty()
        content_placeholder = st.empty()

        for event in self.graph.stream(initial_state):
            for node_name, state_update in event.items():
                
                blog_data = state_update.get("blog", {})
                
                if "title" in blog_data:
                    title_placeholder.markdown(blog_data["title"])
                
                if "content" in blog_data:
                    full_text = blog_data["content"]
                    
                    def stream_generator():
                        for word in full_text.split(" "):
                            yield word + " "
                            time.sleep(0.01)
                    
                    content_placeholder.write_stream(stream_generator)
        