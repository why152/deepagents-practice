from my_agent.agent import agent
from langchain_core.messages import HumanMessage

print("Agent loaded successfully.")
try:
    graph = agent.get_graph()
    print(f"Agent graph type: {type(graph)}")
    # print(graph.draw_ascii()) # Optional: might fail if dependencies missing, keeping it simple
except Exception as e:
    print(f"Could not inspect graph: {e}")


# Optional: Inspect the graph to see if subagents are present
# This depends on how deepagents compiles the graph, but at least loading it confirms no syntax errors.
print("Verification complete: Agent can be imported.")
