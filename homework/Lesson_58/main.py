from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "claude-haiku-5-5"

llm = ChatAnthropic(model=MODEL_NAME, thinking={"type": "disabled"})

#State
class MyStateDict(TypedDict):
    product_text: str
    product_info: str
    marketing_text: str
    final_description: str

#Node 1
def extract(state: MyStateDict):
    p_text = state['product_text']
    prompt = f"divide, clean and format this information about a product: {p_text}"
    response = llm.invoke(prompt)
    return {"product_info": response.content}

#Node 2
def marketing(state: MyStateDict):
    p_info = state["product_info"]
    prompt = f"devise a clean/attractive marketing text about this product: {p_info}. Keep it to 1-2 short paragraphs, no markdown formatting, no asterisks or bold text, plain text only."
    response = llm.invoke(prompt)
    return {"marketing_text": response.content}

#Node 3
def format(state: MyStateDict):
    m_text = state["marketing_text"]
    return {"final_description": f"=== PRODUCT DESCRIPTION ===\n\n{m_text}\n\n=== END ==="}

graph = StateGraph(MyStateDict)
graph.add_node("extraction_node", extract)
graph.add_node("marketing_node", marketing)
graph.add_node("format_node", format)

graph.add_edge(START, "extraction_node")
graph.add_edge("extraction_node", "marketing_node")
graph.add_edge("marketing_node", "format_node")
graph.add_edge("format_node", END)

app = graph.compile()

result = app.invoke({"product_text": "iphone 15, 6.1 inch oled, 128gb, a16 bionic, 48mp camera, usb-c, battery good, available in black and blue"})

print(result["final_description"])