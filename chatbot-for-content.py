import os
import sys
import cohere
from dotenv import load_dotenv
from typing import List, Tuple
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from supabase import create_client, Client
import google.generativeai as genai

# Load environment variables
load_dotenv()

class GymChatbot:
    def __init__(self, file_path: str):
        """
        Initialize the chatbot with a vector store from the given file.
        """
        self.setup_gemini_api()
        self.supabase = self.initialize_supabase()
        self.setup_cohere_api()
        self.create_vector_store(file_path)
        self.conversation_history: List[Tuple[str, str]] = []

    def setup_gemini_api(self):
        """
        Set up Google Gemini API configuration.
        """
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        except Exception as e:
            print(f"Error setting up Gemini API: {e}")
            sys.exit(1)

    def initialize_supabase(self) -> Client:
        """
        Initialize the Supabase client.
        """
        try:
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_KEY")
            if not supabase_url or not supabase_key:
                raise ValueError("Missing Supabase credentials")
            return create_client(supabase_url, supabase_key)
        except Exception as e:
            print(f"Error initializing Supabase: {e}")
            sys.exit(1)

    def setup_cohere_api(self):
        """
        Set up Cohere API for embeddings.
        """
        try:
            self.cohere_api_key = os.getenv("COHERE_API_KEY")
            if not self.cohere_api_key:
                raise ValueError("Missing Cohere API key")
            self.client = cohere.Client(self.cohere_api_key)
        except Exception as e:
            print(f"Error setting up Cohere API: {e}")
            sys.exit(1)

    def embed_text(self, text: str, input_type: str = "search_query"):
        """
        Generate embeddings using Cohere's API.
        - input_type can be 'search_query' (for queries) or 'search_document' (for documents).
        """
        try:
            # Use embed-multilingual-light-v3.0 which produces 384-dimensional vectors
            response = self.client.embed(
                texts=[text], 
                model="embed-multilingual-light-v3.0",
                input_type=input_type
            )
            return response.embeddings[0]  # Return the first embedding
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return None

    def delete_all_data(self):
        """
        Delete all records from Supabase.
        """
        try:
            self.supabase.table("chatbotcontent").delete().neq("id", 0).execute()
        except Exception as e:
            print(f"Error deleting data: {e}")

    def create_vector_store(self, file_path: str):
        """
        Create a vector store in Supabase from a text file.
        """
        try:
            self.delete_all_data()
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
            text_splitter = CharacterTextSplitter(chunk_size=1200, chunk_overlap=100)
            split_texts = text_splitter.split_text(text)
            docs = [Document(page_content=chunk) for chunk in split_texts]

            for doc in docs:
                embedding = self.embed_text(doc.page_content, input_type="search_document")
                if embedding:  # Ensure embedding is not None
                    self.supabase.table("chatbotcontent").insert({
                        "content": doc.page_content,
                        "embedding": embedding
                    }).execute()
        except Exception as e:
            print(f"Error creating vector store: {e}")
            sys.exit(1)

    def retrieve_relevant_context(self, query: str, top_k: int = 6) -> List[str]:
        """
        Retrieve relevant context from Supabase.
        """
        try:
            query_embedding = self.embed_text(query)
            if not query_embedding:
                return []

            response = self.supabase.rpc(
                'match_documents', 
                {'query_embedding': query_embedding, 'match_threshold': 0.1, 'match_count': top_k}
            ).execute()

            return [row["content"] for row in response.data]
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return []

    def generate_response(self, query: str) -> str:
        """
        Generate a response using Gemini.
        """
        try:
            context = self.retrieve_relevant_context(query)
            if not context:
                return "I couldn't find specific information. Can you rephrase?"
            
            prompt = f"""
            You are an expert gym assistant. Use the following context to answer the query:

            Context:
            {chr(10).join([f"- {chunk}" for chunk in context])}

            User Query: {query}
            """
            
            response = self.model.generate_content(prompt)
            generated_text = response.text.strip()
            self.conversation_history.append((query, generated_text))
            return generated_text
        
        except Exception as e:
            print(f"Error generating response: {e}")
            return "An error occurred while processing your query."

# Terminal Chat Loop
def start_terminal_chat():
    chatbot = GymChatbot("info.txt")
    
    print("💪 Gym Chatbot - Type 'exit' to stop the chat.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            print("Goodbye! 💪")
            break
        
        response = chatbot.generate_response(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    start_terminal_chat()