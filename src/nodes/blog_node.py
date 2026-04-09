from src.states.blogstate import BlogState, Blog
from langchain_core.messages import HumanMessage


class BlogNode:
    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState):
        """Create or regenerate the blog title, taking feedback into account."""
        topic = state["topic"]
        feedback = state.get("feedback", "")

        if feedback:
            prompt = f"""You are an expert blog content writer. Use Markdown formatting.
The user previously generated a blog on "{topic}" and gave this feedback: "{feedback}"
Generate an improved, creative and SEO-friendly blog title that addresses this feedback."""
        else:
            prompt = f"""You are an expert blog content writer. Use Markdown formatting.
Generate a creative and SEO-friendly blog title for: "{topic}"."""

        response = self.llm.invoke(prompt)
        return {"blog": {"title": response.content, "content": ""}}

    def content_generation(self, state: BlogState):
        """Generate or regenerate blog content, taking feedback into account."""
        topic = state["topic"]
        title = state["blog"]["title"]
        feedback = state.get("feedback", "")

        if feedback:
            prompt = f"""You are an expert blog writer. Use Markdown formatting.
Topic: "{topic}"
Title: "{title}"
Previous feedback from user: "{feedback}"

Write a detailed, well-structured blog post that directly addresses this feedback.
Include: introduction, multiple sections with headers, key insights, and a conclusion."""
        else:
            prompt = f"""You are an expert blog writer. Use Markdown formatting.
Topic: "{topic}"
Title: "{title}"

Write a detailed, well-structured blog post.
Include: introduction, multiple sections with headers, key insights, and a conclusion."""

        response = self.llm.invoke(prompt)
        return {"blog": {"title": title, "content": response.content}}

    def translation(self, state: BlogState):
        """Translate the blog to the target language."""
        current_language = state.get("current_language", "english")

        translation_prompt = """Translate the following blog into {current_language}.

CRITICAL INSTRUCTIONS:
1. Return a JSON object with exactly two keys: "title" and "content".
2. The "content" value MUST be a single string in Markdown format.
3. Do NOT create nested objects or lists inside "content".
4. Ensure proper JSON escaping.

ORIGINAL TITLE: {title}
ORIGINAL CONTENT:
{blog_content}"""

        messages = [
            HumanMessage(content=translation_prompt.format(
                current_language=current_language,
                title=state["blog"]["title"],
                blog_content=state["blog"]["content"]
            ))
        ]

        result = self.llm.with_structured_output(Blog, method="json_mode").invoke(messages)
        return {"blog": {"title": result.title, "content": result.content}}