# Claude Chatbot

A web chatbot built from scratch with Python, Flask and the Anthropic Claude API.

## Features
- Multi-turn conversation memory (full history sent on each request)
- Configurable system prompt for personality and rules
- Error handling for invalid keys, network failures and API errors
- Secure architecture: the API key stays on the server, never in the browser

## Tech stack
Python · Flask · Anthropic SDK · HTML/CSS/JavaScript

## Run it locally
1. Clone the repo and create a virtual environment:
```
   python -m venv venv
   venv\Scripts\Activate.ps1
```
2. Install dependencies:
```
   pip install -r requirements.txt
```
3. Copy `.env.example` to `.env` and add your Anthropic API key.
4. Start the server and open http://127.0.0.1:5000:
```
   python app.py
```