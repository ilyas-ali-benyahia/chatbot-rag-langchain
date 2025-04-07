🏋️‍♂️ Gym Chatbot with RAG (Retrieval-Augmented Generation)
This Python implementation creates an intelligent gym assistant chatbot using:

Google Gemini for response generation

Cohere for text embeddings

Supabase as a vector database

LangChain for text processing

Key Features
Knowledge Base Integration:

Processes text files to create a searchable knowledge base

Splits content into optimal chunks using LangChain's CharacterTextSplitter

Stores embeddings in Supabase for efficient retrieval

Conversational AI:

Uses Gemini Pro 1.5 for natural language understanding

Maintains conversation history context

Provides expert-level fitness advice

Advanced Search:

Implements semantic search with Cohere embeddings

Retrieves most relevant context using Supabase vector similarity

Customizable match threshold and result count

Technical Components
Component	Purpose	Technology
Text Processing	Chunking and document handling	LangChain
Embeddings	Text vectorization	Cohere multilingual-light-v3.0
Vector Database	Storage and similarity search	Supabase
LLM	Response generation	Gemini 1.5 Pro
CLI Interface	User interaction	Python built-in
Setup Instructions
Install dependencies:

bash
Copy
pip install cohere langchain supabase google-generativeai python-dotenv
Configure environment variables:

env
Copy
GEMINI_API_KEY=your_key
COHERE_API_KEY=your_key
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
Prepare your knowledge base:

Add gym/fitness information to info.txt

The system will automatically process this file

Run the chatbot:

bash
Copy
python chatbot.py
Usage Example
plaintext
Copy
💪 Gym Chatbot - Type 'exit' to stop the chat.

You: How do I properly do a deadlift?
Bot: Here are the key steps for a proper deadlift:
1. Stand with feet hip-width apart...
2. Keep your back straight as you hinge at the hips...
3. Grip the bar with hands just outside your legs...
[Detailed instructions continue]
