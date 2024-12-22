from langchain_community.vectorstores import Qdrant
from langchain.agents import Tool
from qdrant_client import QdrantClient
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from config.environment import get_env_variable

def initialize_qdrant():
    # Set up Qdrant with your existing collection
    client = QdrantClient(
        url=get_env_variable('QDRANT_URL'),
        api_key=get_env_variable('QDRANT_API_KEY'),
    )

    # Get the HuggingFace API key
    huggingface_api_key = get_env_variable('HUGGINGFACE_API_KEY')
    if huggingface_api_key is None:
        raise ValueError("HUGGINGFACE_API_KEY is not set in environment variables or secrets")

    # Initialize remote embeddings
    embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key=huggingface_api_key, model_name="sentence-transformers/all-mpnet-base-v2"
    )

    return client, embeddings

# Initialize the Qdrant retriever tool
qdrant, embeddings = initialize_qdrant()

# Set up Qdrant with your existing collection
qdrant_retriever = Qdrant(
    client=qdrant,
    collection_name="DnD_BasicRules_2018.txt",  # Replace with your collection name
    embeddings=embeddings
)

def get_relevant_document(name: str) -> str:
    results = qdrant_retriever.similarity_search(query=name, k=5)
    
    total_content = "\n\nBelow is content related to the user's query: \n\n"
    chunk_count = 0
    for result in results:
        chunk_count += 1
        if chunk_count > 4:
            break
        total_content += result.page_content + "\n"
    return total_content

dnd_rules_tool = Tool(
    name="Get Relevant document",
    func=get_relevant_document,
    description="Useful for helping answer queries about DND or Dungeon and Dragons."
) 