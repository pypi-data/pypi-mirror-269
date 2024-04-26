from langchain.document_loaders import CSVLoader, PDFMinerLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import os
import argparse

def initialize_rag(doc_path, persist_directory):
    # Load the document
    if doc_path.endswith(".csv"):
        loader = CSVLoader(doc_path)
    elif doc_path.endswith(".pdf"):
        loader = PDFMinerLoader(doc_path)
    elif doc_path.endswith(".docx"):
        loader = TextLoader(doc_path)
    else:
        raise ValueError("Unsupported file format. Supported formats are CSV, PDF, and DOCX.")

    documents = loader.load()

    # Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=500)
    texts = text_splitter.split_documents(documents)

    # Create embeddings
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create ChromaDB and store document IDs
    db = Chroma.from_documents(texts, embeddings, persist_directory=persist_directory)
    db.persist()

    doc_ids_path = os.path.join(persist_directory, "docids.txt")

    # Store document IDs in a file
    for text_id, _ in enumerate(texts):
        document_id = f"doc_{text_id}"
        with open(doc_ids_path, "a") as f:
            f.write(f"{document_id}\n")

def main():
    persist_directory = "db"
    if not os.path.exists(persist_directory):
        os.mkdir(persist_directory)
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", type=str, help="Path to the document to process")
    args = parser.parse_args()
    if args.doc:
        initialize_rag(args.doc, persist_directory)
        print(f"Database created at {persist_directory}")
    else:
        print("Please provide a document to process using --doc argument")

if __name__ == "__main__":
    main()
