# AI Blog Post Generator

Author: Hunter Savarese

This is an AI-powered blog post generator that creates SEO-optimized content. It uses OpenAI's GPT model to generate blog posts and includes a daily automation feature that creates a blog post for a predefined keyword "wireless earbuds" at 3 AM every day.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ai-blog-generator-interview-HunterSavarese.git
cd ai-blog-generator-interview-HunterSavarese
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

3. Install all the required packages (this will set up everything you need):
```bash
pip install -r requirements.txt
```

## Environment Setup

You'll need an OpenAI API key to make this work. Here's how to set it up:

1. Create a new file called `.env` in the project's main directory
2. Add your OpenAI API key to the file like this:
```
OPENAI_API_KEY=your_api_key_here
```

You can get an API key by signing up at [OpenAI's website](https://platform.openai.com/).
