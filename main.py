from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict

from langgraph.graph import StateGraph, END

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

from langchain.agents.initialize import initialize_agent
from langchain.agents import AgentType


# MAIN LLM


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# SEARCH TOOL


search_tool = TavilySearchResults(
    max_results=5
)


# RESEARCH AGENT


research_agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


# RESEARCH FUNCTION


def research_topic(topic):

    query = f"""
    Conduct detailed research on:

    {topic}

    Include:
    - Introduction
    - Latest Trends
    - Advantages
    - Challenges
    - Future Scope
    """

    result = research_agent.invoke({
        "input": query
    })

    return result["output"]



writer_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)



def write_report(research_data):

    prompt = f"""
    You are an expert technical writer.

    Using the following research data,
    write a detailed professional report.

    Research Data:
    {research_data}

    Include:
    - Title
    - Introduction
    - Key Findings
    - Challenges
    - Future Opportunities
    - Conclusion
    """

    response = writer_llm.invoke(prompt)

    return response.content



class AgentState(TypedDict):
    topic: str
    research: str
    report: str



def research_node(state):

    topic = state["topic"]

    print("\n===================================")
    print("RESEARCH AGENT RUNNING")
    print("===================================\n")

    research_result = research_topic(topic)

    return {
        "research": research_result
    }



def writer_node(state):

    research = state["research"]

    print("\n===================================")
    print("WRITER AGENT RUNNING")
    print("===================================\n")

    report = write_report(research)

    return {
        "report": report
    }



workflow = StateGraph(AgentState)

workflow.add_node("researcher", research_node)
workflow.add_node("writer", writer_node)

workflow.set_entry_point("researcher")

workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", END)

# Compile App
app = workflow.compile()



if __name__ == "__main__":

    print("\n===================================")
    print("MULTI AGENT AI RESEARCH SYSTEM")
    print("===================================\n")

    topic = input("Enter Research Topic: ")

    try:

        result = app.invoke({
            "topic": topic
        })

        final_report = result["report"]

        print("\n===================================")
        print("FINAL REPORT")
        print("===================================\n")

        print(final_report)

        # Save report
        with open("report.txt", "w", encoding="utf-8") as file:
            file.write(final_report)

        print("\nReport saved as report.txt\n")

    except Exception as e:

        print("\nERROR:")
        print(e)