import streamlit as st
import time


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message, feedback=None):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message
        self.feedback = feedback

    def display_result_on_ui(self):
        topic = st.session_state.get("blog_topic", self.user_message)
        iteration = st.session_state.get("iteration", 0)

        initial_state = {
            "topic": topic,
            "current_language": self.usecase,
            "feedback": self.feedback or "",
            "iteration": iteration,
        }

        title_placeholder = st.empty()
        content_placeholder = st.empty()

        final_title = ""
        final_content = ""

        with st.spinner("✍️ Generating your blog..."):
            for event in self.graph.stream(initial_state):
                for node_name, state_update in event.items():
                    blog_data = state_update.get("blog", {})

                    if blog_data.get("title"):
                        final_title = blog_data["title"]
                        title_placeholder.markdown(
                            f"## {final_title}", unsafe_allow_html=True
                        )

                    if blog_data.get("content"):
                        final_content = blog_data["content"]

        # Stream content word by word after generation
        if final_content:
            def stream_generator():
                for word in final_content.split(" "):
                    yield word + " "
                    time.sleep(0.015)

            content_placeholder.write_stream(stream_generator)

        # Save to session state for feedback loop
        st.session_state["blog_title"] = final_title
        st.session_state["blog_content"] = final_content
        st.session_state["blog_generated"] = True
        st.session_state["iteration"] = iteration + 1