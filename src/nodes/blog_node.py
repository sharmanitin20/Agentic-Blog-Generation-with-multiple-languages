from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog

class BlogNode:
    """
    A class to represent the blog node
    """

    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState):
        """
        create the title for the blog
        """
        if "topic" in state and state["topic"]:
            prompt = """
                   You are an expert blog content writer. Use Markdown formatting. Generate
                   a blog title for the {topic}. This title should be creative and SEO friendly
                   """
            
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": response.content}}
        
    def content_generation(self, state: BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state['blog']['title'], "content": response.content}}
        
    def translation(self, state: BlogState):
        """
        Translate the content to the specified language.
        """
        # Reinforced prompt to prevent the LLM from nesting JSON objects inside 'content'
        translation_prompt = """
        Translate the following content into {current_language}.
        
        CRITICAL INSTRUCTIONS:
        1. Return a JSON object with exactly two keys: "title" and "content".
        2. The "content" value MUST be a single string containing the entire translated blog in Markdown format. 
        3. Do NOT create nested objects, dictionaries, or lists inside the "content" field.
        4. Ensure all quotes and newlines are properly escaped so the JSON remains valid.

        ORIGINAL CONTENT:
        {blog_content}
        """
        
        print(f"Translating to: {state['current_language']}")
        blog_content = state["blog"]["content"]
        
        messages = [
            HumanMessage(content=translation_prompt.format(
                current_language=state["current_language"], 
                blog_content=blog_content
            ))
        ]
        
        # Using json_mode to satisfy Groq requirements
        translation_result = self.llm.with_structured_output(Blog, method="json_mode").invoke(messages)
        
        # We return the object to update the 'blog' key in the state
        return {"blog": {"title": translation_result.title, "content": translation_result.content}}

    def route(self, state: BlogState):
        return {"current_language": state['current_language']}
    
    def route_decision(self, state: BlogState):
        """
        Route the content to the respective translation function.
        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "french": 
            return "french"
        else:
        """
        
        return state['current_language']