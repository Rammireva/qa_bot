import chromadb
from chromadb.utils import embedding_functions
from read_file import load_pdf
import openai
import os

os.environ['OPENAI_API_KEY']='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'
openai.api_key='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'

client = chromadb.PersistentClient(path="/Users/apple/Documents/chromadb")

sentence_transformer = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_or_create_collection(name="docs", metadata={"hnsw:space":"cosine"}, embedding_function=sentence_transformer)

def add_document_cache():
    data_embeddings = sentence_transformer([doc_content])
    collection.add(
        embeddings=data_embeddings,
        documents=[doc_content]
    )


def add_text_to_collection(file: str, word: int = 1000) -> None:
    docs = load_pdf(file, word)
    docs_strings = []
    ids = []
    metadatas = []
    id = 0
    for page_no in docs.keys():
        for doc in docs[page_no]:
            data_embeddings = sentence_transformer([doc])
            collection.add(
                ids = [file+str(page_no)],
                documents = doc,
                embeddings=data_embeddings,
                metadatas = [{"source":file+str(page_no)}],
            )

    return "PDF embeddings successfully added to collection"


def get_chroma():
    print(collection.get())
    return "success"


def getFromEmbeddings(query: str):
    embedded_query = sentence_transformer([query])
    results = collection.query(
        query_texts=query,
        # query_embeddings=embedded_query,
        include=["documents"],
        n_results=1
    )
    print(results)
    return results


def get_answer(query: str):
    cache_response = getFromEmbeddings(query)
    if len(cache_response['documents']) > 0:
        print(cache_response)
        content = cache_response['documents'][0]
        print(content)
        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Q&A system that is trusted around the world. Always answer the query using the provided context information, and not prior knowledge. \\n Some rules to follow: \\n1. Never directly reference the given contect in your answer. \\n2. Avoid statements like 'Based on the context, ...' or 'The context information, ...' or anything along those lines."
                },
                {
                    "role": "user",
                    "content": f"Context information is below. \\n----------\\n{content}\\nQuery: {query}\\nAnswer:"
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        print("having content", gpt_response['choices'][0]['message']['content'])
        return gpt_response['choices'][0]['message']['content']
    else:
        print('no content')


def delete_collection():
    client.delete_collection(name="docs")