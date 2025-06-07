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

## How to run the Application:
 In the terminal run:
```bash
python app.py
```

- This will start the Flask web server on http://localhost:5000.
- Launch the scheduler for daily blof post generation
- open the web interface so you can generate blog posts manually

Simply enter a keyword into the box and hit "Generate Blog Post" 

## How the Schedular works

- It runs every day at 3am
- Will automatically generate a blog post about "wireless earbuds" 
- Saves the generated post the "generated_posts folder. 
- Each post is saved as a json file with, the content, SEO metrics, timestamp, and keyword used. 

## Testing

I've got a solid test suite that makes sure everything works as expected. Here's what I test:

### What I Test
- The web interface loads correctly and handles different inputs
- Blog post generation works with various keywords
- SEO metrics are fetched and processed correctly
- The daily scheduler runs at the right time (3 AM)
- Error handling for things like missing API keys or failed requests
- Saving and loading generated posts

### Running Tests
To run the tests, make sure you're in your virtual environment and run:
```bash
pytest
```

For a detailed coverage report showing which parts of the code are tested:
```bash
pytest --cov=.
```

### Test Coverage
I maintain high test coverage (over 90%) to ensure the application is reliable. The tests check:
- All main features work correctly
- Edge cases are handled properly
- Error messages are clear and helpful
- The scheduler and automation features run smoothly
