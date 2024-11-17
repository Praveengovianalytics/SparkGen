from {{ cookiecutter.project_slug }}.agents.agent import Agent
from {{ cookiecutter.project_slug }}.prompt.prompt_template import PromptTemplate
from {{ cookiecutter.project_slug }}.llms.base_llm import BaseLLM
from {{ cookiecutter.project_slug }}.embeddings.embedder import Embedder
from {{ cookiecutter.project_slug }}.vectordatabase.vector_store import VectorStore
from {{ cookiecutter.project_slug }}.tools.tools import Tools
from {{ cookiecutter.project_slug }}.memory.memory import ChatMemory
from {{ cookiecutter.project_slug }}.callbacks.callback_handler import CallbackHandler
from {{ cookiecutter.project_slug }}.telemetry.telemetry import Telemetry
from {{ cookiecutter.project_slug }}.config.config_loader import ConfigLoader
from {{ cookiecutter.project_slug }}.data_loaders.data_loader import DataLoader
from {{ cookiecutter.project_slug }}.retrievers.retriever import Retriever
from {{ cookiecutter.project_slug }}.reranker.reranker import Reranker

class AIProject:
    def __init__(self):
        # Initialize configuration
        self.config = ConfigLoader().load_config()

        # Initialize various components
        self.agent_manager = Agent()
        self.prompt_handler = PromptTemplate()
        self.llm_integration = BaseLLM(self.config)
        self.embedding_handler = Embedder(self.config)
        self.vector_database = VectorStore(self.config)
        self.tool_manager = Tools()
        self.memory_manager = ChatMemory()
        self.callback_manager = CallbackHandler()
        self.telemetry_logger = Telemetry("https://your-telemetry-endpoint.com")
        self.data_loader = DataLoader()
        self.retriever = Retriever()
        self.reranker = Reranker()

        # Log initialization
        self.telemetry_logger.log_event("Initialization", "All components initialized successfully.")

    def run(self):
        """Main method to execute the project."""
        self.telemetry_logger.log_event("Run", "Starting main workflow...")
        # Example workflow
        query = "What is the capital of France?"
        context = self.memory_manager.get_history()

        prompt_data = {
            "user_nickname": "User",
            "user_is_in_a_hurry": False,
            "query": query,
            "context": context
        }

        prompt = self.prompt_handler.render(prompt_data)
        response = self.llm_integration.predict(prompt, self.callback_manager)

        embeddings = self.embedding_handler.embed_query(response)
        self.vector_database.add_embeddings(embeddings)

        candidates = self.retriever.retrieve(query)
        reranked_results = self.reranker.rerank(query, candidates)

        self.callback_manager.on_complete(response)
        return reranked_results

if __name__ == "__main__":
    project = AIProject()
    results = project.run()
    print("Final Results:", results)
