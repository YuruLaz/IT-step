import sys

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import search_hotel, get_exchange_rate, search_attractions, get_weather

load_dotenv()

#utf-8 for only °C
sys.stdout.reconfigure(encoding="utf-8")


MODEL_NAME = "gemini-3.5-flash-lite"

#define llm and
llm = ChatGoogleGenerativeAI(model=MODEL_NAME)
llm_with_tools = llm.bind_tools(
    tools=[search_hotel, get_exchange_rate, search_attractions, get_weather],
    tool_choice="auto",
)

available_tools = {
    "search_hotel": search_hotel,
    "get_exchange_rate": get_exchange_rate,
    "search_attractions": search_attractions,
    "get_weather": get_weather,
}

if __name__ == "__main__":
    while True:
        question = input("Q / 'exit': ")
        if question == "exit":
            break

        messages = [HumanMessage(content=question)]

        response = llm_with_tools.invoke(messages)
        messages.append(response)

        tools_used = response.tool_calls

        if tools_used:
            print("\nTools used:")
            for tool_call in tools_used:
                # {
                #     'name': 'search_hotel',
                #     'args': {'city': 'Tbilisi'},
                #     'id': 'call_560510',
                #     'type': 'tool_call',
                # }
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]

                print(f"- {tool_name}: {tool_args}")

                if tool_name in available_tools:
                    tool_function = available_tools[tool_name]
                    tool_result = tool_function.invoke(tool_args)
                    #running tool with .invoke()
                else:
                    tool_result = f"Error: Tool {tool_name} not found."

                tool_message = ToolMessage(
                    content=str(tool_result),
                    name=tool_name,
                    tool_call_id=tool_id,
                )
                messages.append(tool_message)

            final_response = llm_with_tools.invoke(messages)
            print(f"\nFinal Answer: {final_response.content[0]['text']}")
        else:
            print("\nNo tools were used.")
            print(f"\nAnswer: {response.content[0]['text']}")
 