import streamlit as st
import time
from src.ui.streamlitui.loadui import LoadStreamlitUI
from src.llms.groqllm import GroqLLM
from src.graphs.graph_builder import GraphBuilder
from src.ui.streamlitui.display_result import DisplayResultStreamlit

MAX_TOPIC_LENGTH = 40
MAX_FEEDBACK_LENGTH = 40
COOLDOWN_SECONDS = 30


def check_cooldown():
    """Returns (can_generate, seconds_remaining)"""
    last_gen = st.session_state.get("last_generation_time", 0)
    elapsed = time.time() - last_gen
    remaining = int(COOLDOWN_SECONDS - elapsed)
    return elapsed >= COOLDOWN_SECONDS, max(0, remaining)


def validate_input(text, max_length, field_name):
    """Returns (is_valid, error_message)"""
    text = text.strip()
    if not text:
        return False, f"{field_name} cannot be empty."
    if len(text) > max_length:
        return False, f"{field_name} is too long ({len(text)}/{max_length} chars). Please shorten it."
    return True, ""


def show_blog_actions():
    """Download and copy buttons."""
    title = st.session_state.get("blog_title", "")
    content = st.session_state.get("blog_content", "")
    if not content:
        return

    full_blog = f"# {title}\n\n{content}"
    filename = f"blog_{st.session_state.get('blog_topic', 'output')[:20].replace(' ', '_')}.md"

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Download as Markdown",
            data=full_blog,
            file_name=filename,
            mime="text/markdown",
            use_container_width=True
        )
    with col2:
        copy_js = f"""
        <script>
        function copyToClipboard() {{
            navigator.clipboard.writeText({repr(full_blog)}).then(() => {{
                document.getElementById('copy-btn').innerText = '✅ Copied!';
                setTimeout(() => {{
                    document.getElementById('copy-btn').innerText = '📋 Copy to Clipboard';
                }}, 2000);
            }});
        }}
        </script>
        <button id="copy-btn" onclick="copyToClipboard()"
            style="width:100%;padding:0.4rem 0.8rem;border-radius:0.5rem;
                   border:1px solid #ccc;background:#fff;cursor:pointer;font-size:0.9rem;">
            📋 Copy to Clipboard
        </button>"""
        st.components.v1.html(copy_js, height=45)


def load_langgraph_agenticai_app():
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Failed to load UI configuration.")
        return

    # Session state defaults
    for key, val in {
        "blog_generated": False,
        "blog_topic": "",
        "iteration": 0,
        "last_generation_time": 0,
    }.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # New Chat button
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🔄 New Chat", use_container_width=True):
            for key in ["blog_generated", "blog_topic", "blog_title",
                        "blog_content", "iteration", "last_generation_time",
                        "locked_language", "locked_model"]:
                st.session_state.pop(key, None)
            st.rerun()

    # LLM setup
    try:
        model = GroqLLM(user_controls=user_input).get_llm()
    except ValueError as e:
        st.error(f"API Key error: {e}. Check your GROQ_API_KEY in .env")
        return
    except Exception as e:
        st.error(f"Could not initialize LLM: {e}")
        return

    usecase = user_input.get("selected_language", "English")

    try:
        graph = GraphBuilder(model).setup_graph(usecase)
    except Exception as e:
        st.error(f"Graph setup failed: {e}")
        return

    # PHASE 1: Topic input
    if not st.session_state["blog_generated"]:
        st.markdown("### 📝 What should the blog be about?")
        st.caption(f"Maximum {MAX_TOPIC_LENGTH} characters")
        user_message = st.chat_input(f"Enter your topic (max {MAX_TOPIC_LENGTH} chars)...")

        if user_message:
            is_valid, error = validate_input(user_message, MAX_TOPIC_LENGTH, "Topic")
            if not is_valid:
                st.warning(f"⚠️ {error}")
                return

            can_generate, remaining = check_cooldown()
            if not can_generate:
                st.warning(f"⏳ Please wait {remaining}s before generating again.")
                return

            st.session_state["blog_topic"] = user_message
            st.session_state["last_generation_time"] = time.time()

            with st.chat_message("user"):
                st.write(f"**Topic:** {user_message}")

            try:
                DisplayResultStreamlit(usecase, graph, user_message, None).display_result_on_ui()
            except Exception as e:
                if "rate limit" in str(e).lower():
                    st.error("Groq rate limit hit. Please wait a minute and try again.")
                elif "api key" in str(e).lower():
                    st.error("Invalid API key. Check your GROQ_API_KEY.")
                else:
                    st.error(f"Generation failed: {e}")
                return
            st.rerun()

    
    else:
        st.markdown(f"## {st.session_state.get('blog_title', '')}")
        st.markdown(st.session_state.get("blog_content", ""))
        st.divider()
        show_blog_actions()
        st.divider()

        iteration = st.session_state.get("iteration", 1)
        if iteration > 1:
            st.caption(f"🔁 Regenerated {iteration - 1} time(s) based on your feedback")

        st.markdown("### 💬 Give feedback to improve the blog")
        st.caption(f"Maximum {MAX_FEEDBACK_LENGTH} characters")
        feedback = st.chat_input(f"e.g. 'Make it shorter', 'Add examples'... (max {MAX_FEEDBACK_LENGTH} chars)")

        if feedback:
            is_valid, error = validate_input(feedback, MAX_FEEDBACK_LENGTH, "Feedback")
            if not is_valid:
                st.warning(f"⚠️ {error}")
                return

            can_generate, remaining = check_cooldown()
            if not can_generate:
                st.warning(f"⏳ Please wait {remaining}s before regenerating.")
                return

            st.session_state["last_generation_time"] = time.time()

            with st.chat_message("user"):
                st.write(f"**Feedback:** {feedback}")

            try:
                DisplayResultStreamlit(
                    usecase, graph,
                    st.session_state["blog_topic"],
                    feedback
                ).display_result_on_ui()
            except Exception as e:
                if "rate limit" in str(e).lower():
                    st.error("Groq rate limit hit. Please wait a minute and try again.")
                elif "api key" in str(e).lower():
                    st.error("Invalid API key. Check your GROQ_API_KEY.")
                else:
                    st.error(f"Regeneration failed: {e}")
                return
            st.rerun()