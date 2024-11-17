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
        self.agent_manager = Agent(self.config)
        self.prompt_handler = PromptTemplate(self.config)
        self.llm_integration = LLM(self.config)
        self.embedding_handler = embedder(self.config)
        self.vector_database = VectorStores(self.config)
        self.tool_manager = Tools(self.config)
        self.memory_manager = ChatMemory(self.config)
        self.callback_manager = CallbackHandler(self.config)
        self.telemetry_logger = Telemetry(self.config)
        self.data_loader = DataLoader(self.config)
        self.retriever = Retriever(self.config)
        self.reranker = Reranker(self.config)

        # Log initialization
        self.telemetry_logger.log("All components initialized successfully.")

    def run(self):
        """Main method to execute the project."""
        self.telemetry_logger.log("Starting main workflow...")
        # Example workflow
        query = "What is the capital of France?"
        context = self.memory_manager.retrieve_context(query)
        
        prompt = self.prompt_handler.create_prompt(query, context)
        response = self.llm_integration.generate_response(prompt)
        
        embeddings = self.embedding_handler.generate_embeddings([response])
        self.vector_database.store_embeddings(embeddings)
        
        candidates = self.retriever.retrieve(query)
        reranked_results = self.reranker.rerank(query, candidates)
        
        self.callback_manager.execute_callbacks("on_complete", response)
        return reranked_results

if __name__ == "__main__":
    project = AIProject()
    results = project.run()
    print("Final Results:", results)
