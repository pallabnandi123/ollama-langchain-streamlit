import os
import uuid
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Import routes blueprint
from routes import register_blueprints

# Load environment variables
load_dotenv(".env.dev")

app = Flask(__name__)

# Register all blueprints
register_blueprints(app)

# Global variables for admin-ingested RAG data
global_rag_data = None
persist_directory = "/app/chroma_db/global"

overwrite_embeddings = False  # Set to False to use existing embeddings

# Access the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ORGANIZATION_ID = os.getenv("ORGANIZATION_ID")


class ChatPDF:
    def __init__(self):
        # Initialize the OpenAI Chat model
        self.model = ChatOpenAI(
            model="gpt-4o-mini",
            openai_api_key=OPENAI_API_KEY,
            organization=ORGANIZATION_ID,
            temperature=0.1,
            max_tokens=100,
        )
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
        self.embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.prompt_template = PromptTemplate.from_template(
            """
            <s>[INST] You are an expert assistant and agent for a Low-Code/No-Code (LCNC) platform. 
            Use the context provided to guide users in developing applications. 
            Keep your response concise and max two sentences. If the context is insufficient, state that clearly. 
            [/INST] Question: {question} Context: {context} Answer: [/INST]
            """
        )

    def ingest(self, pdf_file_path: str, session_id: str, overwrite_embeddings: bool = False):
        try:
            if os.path.exists(persist_directory) and os.listdir(persist_directory) and not overwrite_embeddings:
                print(f"Embedding already exists in {persist_directory}. Loading existing data...")
                db = Chroma(persist_directory=persist_directory, embedding_function=self.embedding)
            else:
                docs = PyPDFLoader(file_path=pdf_file_path).load()
                chunks = self.text_splitter.split_documents(docs)
                print(f"New embedding chunks created: {len(chunks)}")

                os.makedirs(persist_directory, exist_ok=True)
                db = Chroma.from_documents(chunks, self.embedding, persist_directory=persist_directory)
                print(f"FAQ RAG data created and persisted in {persist_directory}.")

            global global_rag_data
            global_rag_data = db  # Update the global RAG data

            return jsonify({"session_id": session_id, "message": "PDF ingested successfully and FAQ data created."})
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return jsonify({"error": f"Error processing PDF: {str(e)}"}), 500

    def ask(self, session_id: str, query: str, prompt_template_name: str = "default_template"):
        try:
            db = global_rag_data
            if db is None:
                return jsonify({"error": "FAQ data is not available. Please contact the admin to upload the FAQ document."}), 404

            matching_docs = db.similarity_search(query)
            print(f"Matched documents: {len(matching_docs)}")

            if not matching_docs:
                return jsonify({"response": "No relevant documents/result found."})

            # Define prompt templates
            prompt_templates = {
                "primary_field_template": PromptTemplate.from_template(
                    "Given the user's business description, return only the business category and subcategory. Question: {question} Context: {context} Answer:"
                ),
                "target_customer_template": PromptTemplate.from_template(
                    "Given the user's target customers, return only the application flow within two sentences. Question: {question} Context: {context} Answer:"
                ),
                "app_template_choice": PromptTemplate.from_template(
                    "Given the selected template, thank the user for choosing it for their business type. Question: {question} Context: {context} Answer:"
                ),
                "default_template": self.prompt_template,
            }

            selected_prompt_template = prompt_templates.get(prompt_template_name, self.prompt_template)

            chain = RetrievalQA.from_chain_type(
                llm=self.model,
                retriever=db.as_retriever(),
                chain_type="stuff",
                chain_type_kwargs={"prompt": selected_prompt_template},
                return_source_documents=True,
                verbose=True,
            )
            result = chain.invoke({"input_documents": matching_docs, "query": query})
            response_text = result.get("result", "No answer found.")

            return jsonify({"response": response_text})
        except Exception as e:
            print(f"Error during query processing: {str(e)}")
            return jsonify({"error": f"Error during query processing: {str(e)}"}), 500


@app.route("/ingest", methods=["POST"])
def admin_ingest():
    try:
        pdf_file = request.files["file"]
        session_id = request.form.get("session_id", str(uuid.uuid4()))
        temp_file_path = f"/tmp/{pdf_file.filename}"
        pdf_file.save(temp_file_path)

        chat_pdf = ChatPDF()
        return chat_pdf.ingest(temp_file_path, session_id, overwrite_embeddings)
    except Exception as e:
        print(f"Error during PDF ingestion: {str(e)}")
        return jsonify({"error": f"Error during PDF ingestion: {str(e)}"}), 500


@app.route("/ask", methods=["POST"])
def user_query():
    try:
        data = request.json
        session_id = data.get("session_id", str(uuid.uuid4()))
        query = data.get("query")
        prompt_template_name = data.get("prompt_template_name", "default_template")

        chat_pdf = ChatPDF()
        return chat_pdf.ask(session_id, query, prompt_template_name)
    except Exception as e:
        print(f"Error during query handling: {str(e)}")
        return jsonify({"error": f"Error during query handling: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
