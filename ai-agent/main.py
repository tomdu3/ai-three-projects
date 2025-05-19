from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

@tool  # the agent will decide whether to use this tool or not
def calculator(a: float, b: float) -> float:
    """Useful for when you need to answer questions about math, but
    don't want to set up a calculator. Here is a simple calculator tool
    that can be used to answer questions about math, like in this case where
    you need to know the sum of two numbers.
    """
    print("Tool called")
    return f"The sum of {a} and {b} is {a + b}."

def main():
    model = ChatOpenAI(temperature=0)  # temperature=0 means deterministic
    tools = [calculator]
    agent_executor = create_react_agent(model, tools)

    print("Hello, I'm your faitful AI agent! Type 'exit' to exit.")
    print("You can ask me anything about the world!")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            break
        
        print("AI: ", end="")

        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()

if __name__ == "__main__":
    main()

