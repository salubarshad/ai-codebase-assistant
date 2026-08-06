import os

from dotenv import load_dotenv
from groq import Groq

from agent import run_agent

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

print("Hi, How can I help you?\n")
while True:
    prompt = input()
    response = run_agent(client, prompt)
    print(response.choices[0].message.content)
