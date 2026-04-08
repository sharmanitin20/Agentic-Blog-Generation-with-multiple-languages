from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.states.blogstate import BlogState
from src.nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)

    def build_topic_graph(self):
        self.blog_node_obj = BlogNode(self.llm)
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation", self.blog_node_obj.content_generation)
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", END)
        return self.graph

    def build_language_graph(self, target_lang):
        self.blog_node_obj = BlogNode(self.llm)
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation", self.blog_node_obj.content_generation)
        
        # FIXED: Pass the target_lang directly into the lambda
        self.graph.add_node("language_translation", 
            lambda state: self.blog_node_obj.translation({**state, "current_language": target_lang}))

        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", "language_translation")
        self.graph.add_edge("language_translation", END)
        return self.graph

    def setup_graph(self, usecase):
        # We build the graph based on the dropdown selection
        if usecase.lower() == "english":
            self.build_topic_graph()
        else:
            self.build_language_graph(usecase)
            
        return self.graph.compile()
    

    

            

    

## Below code is for the langsmith langgraph studio
"""llm=GroqLLM().get_llm()

## get the graph
graph_builder=GraphBuilder(llm)
graph=graph_builder.build_language_graph().compile()"""

