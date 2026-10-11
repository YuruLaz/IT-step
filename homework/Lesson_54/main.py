from typing import Literal

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()

MODEL_NAME = "claude-haiku-5-5"

SYSTEM_PROMPT = (
    "You are a product review analyst. Analyze the customer review you are given "
    "and extract its sentiment, pros, cons, a short summary, and whether the "
    "reviewer would recommend the product.\n"
    "Only use information from the review itself — do not invent pros or cons.\n\n"
    "{format_instructions}"
)


class ReviewAnalysis(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"] = Field(
        description="Overall mood of the review"
    )
    pros: list[str] = Field(description="Good sides of the product mentioned in the review")
    cons: list[str] = Field(description="Bad sides of the product mentioned in the review")
    summary: str = Field(description="Short summary of the review in one or two sentences")
    recommend: bool = Field(description="True if the reviewer would recommend buying the product")


def build_chain():
    model = ChatAnthropic(model=MODEL_NAME, max_tokens=16000)
    parser = PydanticOutputParser(pydantic_object=ReviewAnalysis)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "Review: {review}"),
    ])
    prompt = prompt.partial(format_instructions=parser.get_format_instructions())

    return prompt | model | parser


def main():
    chain = build_chain()

    review = input("Enter a product review: ")
    result = chain.invoke({"review": review})

    print(result)
    print(type(result))


if __name__ == "__main__":
    main()


# ==================================================
# სატესტო მონაცემები
# ==================================================
#
# ტესტი 1
# This laptop is fast, lightweight, and has an excellent display. However, its battery life could be better.
# Expected: sentiment='positive'
# Output:   sentiment='positive' pros=['Fast performance', 'Lightweight', 'Excellent display'] cons=['Battery life could be better'] summary='The reviewer praises the laptop for its speed, light weight, and excellent display, but notes that battery life falls short of expectations.' recommend=True  ✅
#           <class '__main__.ReviewAnalysis'>
#
# ტესტი 2
# The phone is slow, overheats frequently, and the camera quality is disappointing.
# Expected: sentiment='negative'
# Output:   sentiment='negative' pros=[] cons=['Slow performance', 'Overheats frequently', 'Disappointing camera quality'] summary='The reviewer finds the phone slow, prone to frequent overheating, and its camera quality disappointing.' recommend=False  ✅
#           <class '__main__.ReviewAnalysis'>
#
# ტესტი 3
# The headphones have average sound quality. They are comfortable, but the price is relatively high.
# Expected: sentiment='neutral'
# Output:   sentiment='neutral' pros=['Comfortable'] cons=['Average sound quality', 'Relatively high price'] summary='The reviewer finds the headphones comfortable but rates the sound quality as average and considers the price relatively high. The review does not express a clear endorsement.' recommend=False  ✅
#           <class '__main__.ReviewAnalysis'>
