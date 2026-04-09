---
title: Blog Generator Agent
emoji: ✍️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# ✍️ AI Blog Generator Agent

An agentic blog generation app built with **LangGraph** and **Groq LLM**.

## Features

- 📝 Generate full blogs from a topic in seconds
- 🔁 Feedback loop — give feedback and the blog regenerates with improvements
- 🌐 Multi-language support — English, German, Spanish, Chinese, Hindi
- 📥 Download blog as Markdown
- 📋 Copy to clipboard
- 🔒 Input validation and rate limiting to prevent API abuse

## Tech Stack

- 🦜 LangChain Core + LangGraph
- 🤖 Groq LLM (Llama 3.3 70B)
- 🖥️ Streamlit UI

## How it works

```
Your Topic
    ↓
Title Creation Node
    ↓
Content Generation Node
    ↓
Translation Node (if non-English)
    ↓
Your Blog ✅
```

Once a blog is generated, give feedback in the chat and the pipeline
reruns with your feedback baked into the prompts.

## Local Setup

```bash
git clone <repo>
cd BlogAgentic
pip install -r requirements.txt
# Add GROQ_API_KEY to .env
streamlit run main.py
```