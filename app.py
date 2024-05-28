import google.generativeai as gemini_client
from qdrant_client import QdrantClient, UpdateResult
from qdrant_client.http.models import Distance, PointStruct, VectorParams
from enum import Enum
from qdrant_client import QdrantClient
from qdrant_client.http.models import UpdateResult

# Rest of your code...


class UpdateStatus(Enum):
    COMPLETED = 'completed'
    # Add more status values as needed

collection_name = "example_collection"
GEMINI_API_KEY = "AIzaSyDaMnbTaTk-qoVqFWC3VrUDPZdbV6blXQg"
gemini_client.configure(api_key=GEMINI_API_KEY)
search_client = QdrantClient(":memory:")
texts = [
    "Qdrant is a vector database that is compatible with Gemini.",
    "Gemini is a new family of Google PaLM models, released in December 2023.",
]
results = [
    gemini_client.embed_content(
        model="models/embedding-001",
        content=sentence,
        task_type="retrieval_document",
        title="Qdrant x Gemini",
    )
    for sentence in texts
]
len(results[0]['embedding'])
768
points = [
    PointStruct(
        id=idx,
        vector=response['embedding'],
        payload={"text": text},
    )
    for idx, (response, text) in enumerate(zip(results, texts))
]
search_client.create_collection(collection_name, vectors_config=
    VectorParams(
        size=768,
        distance=Distance.COSINE,
    )
)
search_client.upsert(collection_name, points)
UpdateResult(operation_id=0, status=UpdateStatus.COMPLETED)

# search_result =  # Add this line to capture the search results
search_client.search(
    collection_name=collection_name,
    query_vector=gemini_client.embed_content(
        model="models/embedding-001",
        content="Is Qdrant compatible with Gemini?",
        task_type="retrieval_query",
    )["embedding"],
)

