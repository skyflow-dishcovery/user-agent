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
mock_hotels = [
    {
        "name": "The Grand Monarch",
        "location": "Paris, France",
        "stars": 5,
        "price_per_night": 420,
        "rooms": [
            {
                "type": "Deluxe King Room",
                "price": 420,
                "description": "Spacious room with a king-sized bed, Eiffel Tower view, marble bathroom, and complimentary breakfast."
            },
            {
                "type": "Junior Suite",
                "price": 620,
                "description": "Elegant suite with separate living area, rain shower, French balcony, and 24-hour butler service."
            }
        ]
    },
    {
        "name": "Maple Inn",
        "location": "Toronto, Canada",
        "stars": 3,
        "price_per_night": 120,
        "rooms": [
            {
                "type": "Standard Double Room",
                "price": 120,
                "description": "Comfortable room with two double beds, city view, and free high-speed Wi-Fi."
            },
            {
                "type": "King Room with Kitchenette",
                "price": 145,
                "description": "Perfect for extended stays — includes a kitchenette, dining area, and a large workspace."
            }
        ]
    },
    {
        "name": "Sakura Stay",
        "location": "Kyoto, Japan",
        "stars": 4,
        "price_per_night": 180,
        "rooms": [
            {
                "type": "Zen Garden View Room",
                "price": 180,
                "description": "Peaceful room overlooking a traditional Japanese garden, featuring tatami floors and futon bedding."
            },
            {
                "type": "Modern Twin Room",
                "price": 195,
                "description": "Two twin beds with minimalist design, balcony access, and luxury toiletries."
            }
        ]
    },
    {
        "name": "Desert Mirage Resort",
        "location": "Dubai, UAE",
        "stars": 5,
        "price_per_night": 370,
        "rooms": [
            {
                "type": "Executive Suite",
                "price": 450,
                "description": "Opulent suite with desert view, jacuzzi, private lounge access, and personalized concierge service."
            },
            {
                "type": "Deluxe Room",
                "price": 370,
                "description": "Elegant room with skyline view, king-size bed, and a deep soaking tub."
            }
        ]
    },
    {
        "name": "Casa Del Mar",
        "location": "Barcelona, Spain",
        "stars": 4,
        "price_per_night": 210,
        "rooms": [
            {
                "type": "Sea View Room",
                "price": 230,
                "description": "Bright room with floor-to-ceiling windows, beach-facing balcony, and Mediterranean decor."
            },
            {
                "type": "Economy Room",
                "price": 185,
                "description": "Cozy yet modern room with all essentials, ideal for solo travelers or short stays."
            }
        ]
    }
]


async def main():
    hotel_agent = Agent(
        name="Hotel_Assistant",
        instructions=
            f"""
            You are a hotel booking assistant.
            You will help users find hotels based on their preferences.
            You will use the mock_hotels data to find suitable hotels.
            You will respond with the best hotel option that matches the user's criteria.
            If no hotel matches, you will say "No hotels found matching your criteria
            here is your mock data {mock_hotels}.""",
        model="llama-3.3-70b-versatile",

    )
    result = await Runner.run(
        hotel_agent,
        input="I need a cheap hotel to stay in Barcelona. Single bed would work.",
        max_turns=20,
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
