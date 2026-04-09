from langgraph.graph import StateGraph, START, END
from src.states.blogstate import BlogState
from src.nodes.blog_node import BlogNode


class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm

    def _base_nodes(self, graph, blog_node):
        """Add shared nodes and edges for topic graph."""
        graph.add_node("title_creation", blog_node.title_creation)
        graph.add_node("content_generation", blog_node.content_generation)
        graph.add_edge(START, "title_creation")
        graph.add_edge("title_creation", "content_generation")
        return graph

    def build_topic_graph(self):
        graph = StateGraph(BlogState)
        blog_node = BlogNode(self.llm)
        graph = self._base_nodes(graph, blog_node)
        graph.add_edge("content_generation", END)
        return graph

    def build_language_graph(self, target_lang):
        graph = StateGraph(BlogState)
        blog_node = BlogNode(self.llm)
        graph = self._base_nodes(graph, blog_node)
        graph.add_node(
            "language_translation",
            lambda state: blog_node.translation({**state, "current_language": target_lang})
        )
        graph.add_edge("content_generation", "language_translation")
        graph.add_edge("language_translation", END)
        return graph

    def setup_graph(self, usecase: str):
        usecase = usecase.strip().lower()
        if usecase == "english":
            graph = self.build_topic_graph()
        else:
            graph = self.build_language_graph(usecase)
        return graph.compile()

## Below code is for the langsmith langgraph studio
"""llm=GroqLLM().get_llm()

## get the graph
graph_builder=GraphBuilder(llm)
graph=graph_builder.build_language_graph().compile()"""

