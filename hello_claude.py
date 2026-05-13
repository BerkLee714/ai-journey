# Week 4: First API call to Claude
# This is the smallest possible "hello world" with the Anthropic API. 

import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load the .env file so ANTHROPIC_API_KEY becomes available
load_dotenv()

# Create a client - this is the object that talks to Claude
client = Anthropic()

# Send a message
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024, 
    messages=[
        {"role": "user", "content": "Hi, Claude! In two sentences, introduce yourself to someone who has never used you before."} 
    ]
)

# Extract and print the text
message_text = response.content[0].text
print(message_text)

# Bonus: print the cost info
print("")
print("=== Cost info ===")
print(f"Tokens used: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")
