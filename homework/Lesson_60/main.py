from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from typing_extensions import TypedDict

MODEL_NAME = "claude-haiku-5-5"
llm = ChatAnthropic(
    model=MODEL_NAME,
    thinking={"type": "disabled"}
)

class TravelState(TypedDict):
    user_input: str
    destination_info: str
    food_info: str
    budget_info: str
    final_plan: str

def destination_agent(state: TravelState) -> dict:
    system_prompt = """
    You are a travel destination specialist.

    Analyze the user's travel request and provide
    recommendations for attractions and activities.

    Consider:
    - The destination
    - Travel duration
    - User interests
    - Popular attractions
    - Cultural and historical sites

    Do not recommend restaurants.
    Do not calculate the travel budget.
    Do not create a complete travel itinerary.

    Return only destination-related information.
    """
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["user_input"]),
    ])
    return {"destination_info": response.content}

def food_agent(state: TravelState) -> dict:
    system_prompt = """
    You are a local food specialist.

    Recommend food and dining options based on
    the user's destination, preferences, and budget.

    Consider:
    - Traditional local dishes
    - Local cuisine
    - Affordable dining options
    - Restaurants and cafes
    - Estimated meal prices

    Do not plan sightseeing activities.
    Do not calculate the overall travel budget.
    Do not create a complete travel itinerary.

    Return only food-related recommendations.

    If you cannot verify current restaurant details
    or prices, clearly state that estimates may vary.
    """
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["user_input"]),
    ])
    return {"food_info": response.content}

def budget_agent(state: TravelState) -> dict:
    system_prompt = """
    You are a travel budget specialist.

    Estimate the expenses for the requested trip.

    Divide the estimated costs into these categories:

    1. Accommodation
    2. Food
    3. Transportation
    4. Activities and attractions

    Consider:
    - Destination
    - Duration
    - Number of travelers, if specified
    - User's budget preference

    Provide estimated costs for each category
    and calculate an estimated total.

    State your currency and assumptions clearly.
    Distinguish per-person costs from group costs.

    If important information is missing, explain
    your assumptions instead of pretending to know
    the exact costs.

    Do not create a travel itinerary.
    Return only budget-related information.
    """
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["user_input"]),
    ])
    return {"budget_info": response.content}

def planner_agent(state: TravelState) -> dict:
    system_prompt = """
    You are the final travel planning specialist.

    Your task is to combine information from three
    specialized agents into one organized travel plan.

    You will receive:
    - Destination recommendations
    - Food recommendations
    - Budget estimates

    Follow these rules:

    1. Use the information provided by the agents.
    2. Do not invent new attractions, restaurants,
       prices, or factual claims.
    3. Organize the itinerary according to the
       requested travel duration.
    4. Incorporate the user's interests.
    5. Include the food recommendations.
    6. Include the estimated budget breakdown.
    7. Clearly communicate assumptions and uncertainty.
    8. If information is missing, acknowledge it.

    Structure your answer as follows:

    - Trip overview
    - Day-by-day itinerary
    - Food recommendations
    - Estimated budget breakdown
    - Practical tips

    Make the final answer clear and useful.

    You are an aggregator, not a fourth independent
    research agent. Base your recommendations on
    the information supplied by the other agents.
    """
    user_message = f"""
    USER REQUEST:
    {state["user_input"]}

    DESTINATION AGENT RESULTS:
    {state["destination_info"]}

    FOOD AGENT RESULTS:
    {state["food_info"]}

    BUDGET AGENT RESULTS:
    {state["budget_info"]}

    Combine these results into one complete travel plan.
    """
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message),
    ])
    return {"final_plan": response.content}

builder = StateGraph(TravelState)
builder.add_node("destination_agent", destination_agent)
builder.add_node("food_agent", food_agent)
builder.add_node("budget_agent", budget_agent)
builder.add_node("planner_agent", planner_agent)

builder.add_edge(START, "destination_agent")
builder.add_edge(START, "food_agent")
builder.add_edge(START, "budget_agent")
builder.add_edge("destination_agent", "planner_agent")
builder.add_edge("food_agent", "planner_agent")
builder.add_edge("budget_agent", "planner_agent")
builder.add_edge("planner_agent", END)

app = builder.compile()

app_result = app.invoke({
    "user_input": "I want to plan a trip to Japan in the spring, focusing on cultural experiences and local cuisine.",
})

print(app_result["final_plan"])
