from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

response = client.messages.create(
  model= "claude-haiku-4-5-20251001",
  max_tokens=20,
  messages=[{
    "role":"user",
    "content":"Tell me one fun fact about Hyderabad."
  }],

)

print(response.content[0].text)
print(response)