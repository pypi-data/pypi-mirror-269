import os

from dotenv import load_dotenv
from openai import OpenAI

from parea import Parea

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

p = Parea(api_key=os.getenv("PAREA_API_KEY"), project_name="testing")
p.wrap_openai_client(client)


tools = [
    {
        "type": "function",
        "function": {
            "name": "solarFarm_potential",
            "description": "Estimate the energy output of a solar farm given its location and panel area for a particular month.",
            "parameters": {
                "type": "object",
                "properties": {
                    "coordinates": {"type": "array", "items": {"type": "number"}, "description": "The geographic coordinates of the location of the solar farm."},
                    "panelArea": {"type": "integer", "description": "The total solar panel area in square feet at the location."},
                    "month": {"type": "string", "description": "The month for which to calculate the potential energy output. Default to January", "optional": True},
                },
                "required": ["coordinates", "panelArea"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "windFarm_potential",
            "description": "Estimate the energy output of a wind farm given its location and turbine count for a particular month.",
            "parameters": {
                "type": "object",
                "properties": {
                    "coordinates": {"type": "array", "items": {"type": "number"}, "description": "The geographic coordinates of the location of the wind farm."},
                    "turbineCount": {"type": "integer", "description": "The total number of wind turbines at the location."},
                    "month": {"type": "string", "description": "The month for which to calculate the potential energy output. Default to January", "optional": True},
                },
                "required": ["coordinates", "turbineCount"],
            },
        },
    },
]
messages = [
    {
        "role": "user",
        "content": """Questions:How much is the potential of the Solar farm at location with coordinates [43.653225, -79.383186] in December, given that it has a total solar panel area of 80000 sq ft?
 Note that the provided function is in Python.""",
    }
]
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    tools=tools,
    tool_choice="auto",
)
# messages.append({k: v for k, v in completion.choices[0].message.model_dump().items() if v is not None})
# # messages.append(completion.choices[0].message)
# messages.append({"role": "tool", "content": "5 Celcius", "tool_call_id": completion.choices[0].message.tool_calls[0].id})
# messages.append(
#     {
#         "role": "user",
#         "content": "What's the weather like in Boston today?",
#     }
# )
#
# final_completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=messages,
#     tools=tools,
#     tool_choice="auto",
# )
#
# print(final_completion)
