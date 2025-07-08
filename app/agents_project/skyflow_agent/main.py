from agents import Agent, Runner, set_tracing_disabled, set_default_openai_api,  set_default_openai_client
from dotenv import load_dotenv
from openai import AsyncOpenAI
import asyncio
import os

load_dotenv()

# Load API keys
groq_api_key = os.getenv("GROQ_API_KEY")

client = AsyncOpenAI(
    api_key=groq_api_key,
    base_url="https://api.groq.com/openai/v1"
)

# Agent setup
set_tracing_disabled(True)
set_default_openai_api("chat_completions")
set_default_openai_client(client)

# Mock flights
mock_flights = [
    {
        "airline": "Air Canada",
        "price": 580,
        "layovers": 0,
        "departure": "2025-07-08T14:30",
        "arrival": "2025-07-08T19:45",
        "destination": "Canada",
        "class": "economy"
    },
    {
        "airline": "British Airways",
        "price": 650,
        "layovers": 1,
        "departure": "2025-07-08T10:00",
        "arrival": "2025-07-08T18:00",
        "destination": "Paris",
        "class": "business"
    },
    {
        "airline": "Lufthansa",
        "price": 400,
        "layovers": 2,
        "departure": "2025-07-09T12:00",
        "arrival": "2025-07-09T20:00",
        "destination": "Germany",
        "class": "economy"
    },
    {
        "airline": "PIA",
        "price": 300,
        "layovers": 1,
        "departure": "2025-07-10T09:00",
        "arrival": "2025-07-10T17:00",
        "destination": "Dubai",
        "class": "economy"
    },
    {
        "airline": "Air Canada",
        "price": 800,
        "layovers": 0,
        "departure": "2025-07-08T14:30",
        "arrival": "2025-07-08T19:45",
        "destination": "Russia",
        "class": "business"
    }

]



async def main():
    flight_agent = Agent(
        name="Flight_Assistant",
        instructions=
            f"""
            You are a flight booking assistant.
            You will help users find flights based on their preferences.
            You will use the mock_flights data to find suitable flights.
            You will respond with the best flight option that matches the user's criteria.
            If no flight matches, you will say "No flights found matching your criteria
            here is your mock data {mock_flights}.""",
        model="llama-3.3-70b-versatile",

    )
    result = await Runner.run(
        flight_agent,
        input="I need a flight to Russia under 900, business class, preferably direct, next week",
        max_turns=20,
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
