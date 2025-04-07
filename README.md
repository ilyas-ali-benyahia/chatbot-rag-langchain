# 💪 AI Gym Assistant Chatbot

**A Retrieval-Augmented Generation (RAG) chatbot for fitness advice**  
*Powered by Gemini 1.5, Cohere, and Supabase*

![Demo](https://img.shields.io/badge/Demo-Terminal_Interface-green) 
![RAG](https://img.shields.io/badge/Architecture-RAG-blue)

## 🔍 Overview
An AI-powered gym assistant that:
- Answers fitness questions using your custom knowledge base (`info.txt`)
- Implements semantic search with **Cohere's multilingual embeddings**
- Generates natural responses via **Google Gemini 1.5**
- Stores vectors in **Supabase** for low-latency retrieval

## 🛠️ Tech Stack
| Component          | Technology                          |
|--------------------|-------------------------------------|
| **LLM**            | Google Gemini 1.5 Pro               |
| **Embeddings**     | Cohere `embed-multilingual-light-v3`|
| **Vector Database**| Supabase + pgvector                 |
| **Text Processing**| LangChain                           |

## ⚡ Quick Start

1. **Install dependencies**
   pip install cohere langchain supabase google-generativeai python-dotenv

2. Configure Environment Variables
Create a .env file in the root directory of your project and add the following:

env
Copy
Edit
GEMINI_API_KEY=your_key_here  
COHERE_API_KEY=your_key_here  
SUPABASE_URL=your_project_url  
SUPABASE_KEY=your_anon_key  
3. **Add your fitness content**
    Edit info.txt with exercise instructions, nutrition tips, etc.
4. **Run the chatbot**
    Run the chatbot


**📖 Example Usage**

    💪 You: How do I improve my squat form?
    Bot: Here are 3 key tips:
    1. Keep your chest up and core engaged...
    2. Ensure knees track over toes...
    3. Descend until thighs are parallel to... 


**🎯 Features**
**Context-Aware Responses**: Retrieves relevant snippets before answering

**Multilingual Support**: Handles non-English queries via Cohere

**Conversation History**: Maintains dialogue context

**Easy Knowledge Updates**: Just modify info.txt    




# 🏋️‍♂️ AI-Powered Fitness Chatbot

A smart chatbot powered by Cohere, LangChain, Supabase, and Google Gemini that provides fitness guidance based on your custom content.

---

## 🚀 Setup Instructions

### 1. Install Dependencies

Install all required Python packages using pip:

```bash
pip install cohere langchain supabase google-generativeai python-dotenv

