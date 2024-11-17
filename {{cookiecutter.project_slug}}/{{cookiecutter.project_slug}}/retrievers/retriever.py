class Retriever(BaseRetriever):
    embedding_function: Embeddings
    collection_name: str = "LangChainCollection"
    connection_args: Optional[Dict[str, Any]] = None
    search_params: Optional[dict] = None
    retriever: BaseRetriever

    def create_client(cls, values: dict) -> Any:
        return values

    def add_texts(
        self, texts: List[str], metadatas: Optional[List[dict]] = None
    ) -> None:
        self.store.add_texts(texts, metadatas)

    def _get_relevant_documents(
        self,query: str, 
        run_manager: CallbackManagerForRetrieverRun) -> List[Document]:
        
        return self.retriever.invoke(
            query, run_manager=run_manager.get_child(), **kwargs
        )