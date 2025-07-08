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

mock_restaurants = [
    {
        "name": "La Bella Napoli",
        "cuisine": "Italian",
        "location": "Rome, Italy",
        "menu": [
            {
                "item": "Margherita Pizza",
                "price": 12.5,
                "description": "Classic wood-fired pizza topped with San Marzano tomatoes, fresh mozzarella, and basil."
            },
            {
                "item": "Fettuccine Alfredo",
                "price": 15.0,
                "description": "Creamy parmesan sauce over hand-cut fettuccine pasta, finished with cracked black pepper."
            },
            {
                "item": "Tiramisu",
                "price": 7.0,
                "description": "Traditional Italian dessert layered with mascarpone, espresso-soaked ladyfingers, and cocoa powder."
            }
        ]
    },
    {
        "name": "Spice Symphony",
        "cuisine": "Indian Fusion",
        "location": "New York, USA",
        "menu": [
            {
                "item": "Butter Chicken Bao",
                "price": 10.0,
                "description": "Soft bao buns filled with creamy North Indian butter chicken, topped with pickled onions."
            },
            {
                "item": "Lamb Biryani",
                "price": 18.0,
                "description": "Fragrant basmati rice cooked with spiced lamb and saffron, served with cooling raita."
            },
            {
                "item": "Masala Chai Crème Brûlée",
                "price": 9.0,
                "description": "A spiced twist on the French classic, infused with cardamom, cinnamon, and Assam tea."
            }
        ]
    },
    {
        "name": "Tokyo Zen",
        "cuisine": "Japanese",
        "location": "Tokyo, Japan",
        "menu": [
            {
                "item": "Salmon Sashimi",
                "price": 14.0,
                "description": "Delicate slices of premium salmon served with wasabi, soy sauce, and daikon."
            },
            {
                "item": "Ramen Tonkotsu",
                "price": 13.5,
                "description": "Rich pork bone broth ramen with chashu, ajitama egg, bamboo shoots, and scallions."
            },
            {
                "item": "Matcha Mochi Ice Cream",
                "price": 6.5,
                "description": "Soft mochi balls filled with creamy green tea ice cream — a refreshing dessert."
            }
        ]
    },
    {
        "name": "El Asador Mexicano",
        "cuisine": "Mexican",
        "location": "Mexico City, Mexico",
        "menu": [
            {
                "item": "Tacos al Pastor",
                "price": 9.5,
                "description": "Spit-grilled marinated pork tacos topped with pineapple, onions, and cilantro."
            },
            {
                "item": "Carne Asada",
                "price": 17.0,
                "description": "Grilled skirt steak served with guacamole, charro beans, and handmade corn tortillas."
            },
            {
                "item": "Churros con Chocolate",
                "price": 7.0,
                "description": "Golden-fried dough sticks dusted with cinnamon sugar and served with rich chocolate sauce."
            }
        ]
    },
    {
        "name": "Sultan's Table",
        "cuisine": "Turkish",
        "location": "Istanbul, Turkey",
        "menu": [
            {
                "item": "Iskender Kebab",
                "price": 16.0,
                "description": "Slices of doner meat over pita bread, soaked in tomato butter sauce and served with yogurt."
            },
            {
                "item": "Meze Platter",
                "price": 12.0,
                "description": "A selection of traditional small plates including hummus, baba ganoush, and stuffed grape leaves."
            },
            {
                "item": "Baklava",
                "price": 6.0,
                "description": "Flaky pastry layered with pistachios and sweetened with honey syrup."
            }
        ]
    }
]


async def main():
    restaurant_agent = Agent(
        name="Restaurant_Assistant",
        instructions=
            f"""
            You are a restaurant booking assistant.
            You will help users find their desired dishes based on their preferences.
            You will use the mock_restaurants data to find suitable restaurant.
            You will respond with the best restaurant option that matches the user's criteria.
            If no restaurant matches, you will say "No Restaurants have food that matches your criteria.
            here is your mock data {mock_restaurants}.""",
        model="llama-3.3-70b-versatile",

    )
    result = await Runner.run(
        restaurant_agent,
        input="Suggest me something Indian to eat in USA",
        max_turns=20,
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
