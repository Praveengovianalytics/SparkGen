from openai import OpenAI

class Embedder:
    """
    A class designed to interact with OpenAI's embedding model.
    It takes a query, processes it through the OpenAI API, and returns embeddings for that query.

    Attributes:
        embedder (OpenAI): An instance of OpenAI initialized with the model configuration for embedding.
    """

    def __init__(self, model_config: dict) -> None:
        """
        Initializes the Embedder instance with the provided model configuration.

        Args:
            model_config (dict): A dictionary containing the model's configuration parameters 
                                 such as API key, model ID, etc.
        """
        # Initialize the OpenAI instance with the provided configuration for embeddings
        self.embedder = OpenAI(**model_config)
    
    def embed_query(self, query: str, callback: object = None):
        """
        Sends a query to the embedding model and returns the embedding vector.

        Args:
            query (str): The input query to be embedded by the language model.
            callback (object, optional): A placeholder for a callback function that can process the embedding output. 
                                         Default is None.

        Returns:
            output (list): The embedding vector generated from the input query.
        """
        # Start input capture (expandable for logging or monitoring the input)
        
        # Generate the embedding for the query
        output = self.embedder(query)
        
        # Token utilization capture (expandable for tracking the number of tokens used)
        # End output capture (expandable for logging or monitoring the output)
        # Return the generated embedding vector
        return output