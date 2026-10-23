from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from typing_extensions import TypedDict

load_dotenv()

MODEL_NAME = "claude-haiku-5-5"

MAX_ATTEMPTS = 3

llm = ChatAnthropic(model=MODEL_NAME, thinking={"type": "disabled"})
def ask_llm(prompt):
    return llm.invoke(prompt).content

class State(TypedDict):
    ingretients: str
    recepie: str
    feedback: str
    approved: bool
    attempts: int

def generate_recepie(state: State):
    prompt = f"Generate a recepie based on these ingredients: {state['ingretients']}. Keep it short and simple."
    return {"recepie": ask_llm(prompt)}

def check_recepie(state: State):
    prompt = f"Check if this recepie is good: {state['recepie']}. Return 'True' if it's good, 'False' otherwise."
    feedback = ask_llm(prompt)
    approved = feedback.strip().lower() == "true"
    return {"feedback": feedback, "approved": approved}

def improve_recepie(state: State):
    prompt = f"Improve this recepie based on these ingredients: {state['ingretients']}, the current recepie: {state['recepie']}, and the feedback: {state['feedback']}. Keep it short and simple."
    return {"recepie": ask_llm(prompt), "attempts": state["attempts"] + 1}

def routing(state: State):
    if state["approved"] or state["attempts"] >= MAX_ATTEMPTS:
        return END
    return "improve_recepie"

builder = StateGraph(State)
builder.add_node("generate_recepie", generate_recepie)
builder.add_node("check_recepie", check_recepie)
builder.add_node("improve_recepie", improve_recepie)

builder.add_edge(START, "generate_recepie")
builder.add_edge("generate_recepie", "check_recepie")
builder.add_conditional_edges("check_recepie", routing)
builder.add_edge("improve_recepie", "check_recepie")

graph = builder.compile()

result = graph.invoke({
    "ingretients": "chicken, rice, onion, tomato",
    "recepie": "",
    "feedback": "",
    "approved": False,
    "attempts": 0,
})

print(result["recepie"])
print(result["feedback"])