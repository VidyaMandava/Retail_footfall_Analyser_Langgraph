"""
Retail Footfall Analyzer

This script uses LangGraph to analyze retail footfall patterns and provide
competitive insights for retail businesses. It creates a conversational
AI tool that can process queries about footfall patterns in specific locations.

Requirements:
- langchain_openai
- langchain_core
- langchain_community
- langgraph==0.2.59
"""

import os
import json
import time
from typing import Dict, Any

from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langchain_core.tools import Tool
from langchain_core.messages import SystemMessage, HumanMessage

class RetailFootfallAnalyzer:
    """Main class for retail footfall analysis using LangGraph."""
    
    def __init__(self, openai_api_key=None, model_name="gpt-4o-mini", temperature=0):
        """
        Initialize the RetailFootfallAnalyzer.
        
        Args:
            openai_api_key (str, optional): OpenAI API key. If None, it will be read from environment variable.
            model_name (str, optional): Name of the OpenAI model to use. Defaults to "gpt-4o-mini".
            temperature (float, optional): Temperature for response generation. Defaults to 0.
        """
        # Set up API key
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        
        # Check if API key is available
        if "OPENAI_API_KEY" not in os.environ:
            raise ValueError("OpenAI API key not found. Please provide it or set the OPENAI_API_KEY environment variable.")
        
        # Initialize the model
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        
        # System prompt
        self.system_prompt = """You are a retail analyst specializing in footfall patterns and competitive analysis.
When using the retail_footprint_api tool:
1. Extract key insights about peak hours, customer traffic, and competitor data
2. Present the information in a clear, structured format
3. Only use factual information from the API results
4. If specific data is not available, acknowledge the limitation
5. Focus on actionable insights for business owners and marketers"""
        
        # Create the graph
        self.graph = self._build_graph()
    
    def _query_retail_footprint_api(self, query: str) -> str:
        """
        Queries the retail footprint API for information about store traffic patterns.
        
        Args:
            query: A specific request for retail footprint data
            
        Returns:
            JSON string containing retail footprint data
        """
        print(f"Querying retail footprint API with: {query}")
        
        # This is where you would make the actual API call
        # Replace this mock implementation with your actual API call
        
        # Mock response for demonstration
        if "marathahalli" in query.lower():
            mock_data = {
                "location": "Marathahalli, Bangalore",
                "peak_hours": {
                    "weekdays": ["6PM-8PM"],
                    "weekends": ["11AM-2PM", "5PM-9PM"]
                },
                "footfall_data": {
                    "average_daily": 1250,
                    "highest_hour": "6PM-7PM",
                    "busiest_day": "Saturday"
                },
                "competitor_insights": {
                    "density": "High",
                    "major_players": ["Central", "Lifestyle", "Max"],
                    "comparative_traffic": "25% higher during evening hours"
                }
            }
            return json.dumps(mock_data, indent=2)
        
        # Add more location conditions as needed
        elif "pune" in query.lower():
            mock_data = {
                "location": "Pune, Maharashtra",
                "peak_hours": {
                    "weekdays": ["5PM-7PM"],
                    "weekends": ["12PM-3PM", "6PM-8PM"]
                },
                "footfall_data": {
                    "average_daily": 980,
                    "highest_hour": "6PM-7PM",
                    "busiest_day": "Sunday"
                },
                "competitor_insights": {
                    "density": "Medium",
                    "major_players": ["Westside", "Shoppers Stop", "Pantaloons"],
                    "comparative_traffic": "15% higher during weekend evenings"
                }
            }
            return json.dumps(mock_data, indent=2)
        
        else:
            return json.dumps({"error": "No specific data available for this location"})
    
    def _should_continue(self, state: MessagesState) -> str:
        """
        Determines whether to continue processing with tools or end the conversation.
        
        Args:
            state: Current state containing messages
            
        Returns:
            Next node to process or END
        """
        messages = state['messages']
        last_message = messages[-1]
        print(f"Checking message: {type(last_message).__name__}")
        
        has_tool_calls = hasattr(last_message, 'tool_calls') and last_message.tool_calls
        print(f"Has tool calls: {has_tool_calls}")
        
        if has_tool_calls:
            return 'tools'
        else:
            return END
    
    def _call_model(self, state: MessagesState) -> Dict[str, Any]:
        """
        Calls the language model with the current state.
        
        Args:
            state: Current state containing messages
            
        Returns:
            Updated state with new messages
        """
        print("Calling model...")
        messages = state['messages']
        
        # Add system message if not already present
        if not any(isinstance(msg, SystemMessage) for msg in messages):
            print("Adding system message")
            messages = [SystemMessage(content=self.system_prompt)] + messages
        
        print(f"Sending {len(messages)} messages to LLM")
        try:
            response = self.llm.invoke(messages)
            print("Received response from LLM")
            return {'messages': messages + [response]}
        except Exception as e:
            print(f"Error in LLM call: {e}")
            error_message = f"An error occurred: {str(e)}"
            return {'messages': messages + [HumanMessage(content=error_message)]}
    
    def _build_graph(self) -> StateGraph:
        """
        Builds the LangGraph state graph.
        
        Returns:
            Compiled StateGraph
        """
        print("Creating graph...")
        graph = StateGraph(MessagesState)
        graph.add_node('agent', self._call_model)
        
        # Create the retail footprint tool
        retail_tool = Tool(
            name="retail_footprint_api",
            description="Get retail footprint data including peak hours, footfall patterns, and competitor insights for specific locations",
            func=self._query_retail_footprint_api
        )
        
        # Set up tools
        tools = [retail_tool]
        tool_node = ToolNode(tools)
        graph.add_node('tools', tool_node)
        
        # Connect the nodes
        graph.add_edge(START, "agent")
        graph.add_conditional_edges('agent', self._should_continue)
        graph.add_edge('tools', 'agent')
        
        # Compile the graph
        print("Compiling graph...")
        return graph.compile()
    
    def analyze(self, query: str) -> Dict[str, Any]:
        """
        Analyzes retail footfall based on a specific query.
        
        Args:
            query: Question or request about retail footfall
            
        Returns:
            Dictionary containing the response messages
        """
        print("Starting graph execution...")
        start_time = time.time()
        
        # Execute the graph
        try:
            output = self.graph.invoke({
                'messages': [HumanMessage(content=query)]
            })
            
            print(f"Execution completed in {time.time() - start_time:.2f} seconds")
            
            # Print the final result
            print("\nFinal output:")
            final_message = output['messages'][-1]
            if hasattr(final_message, 'content'):
                print(final_message.content)
            
            return output
        except Exception as e:
            print(f"Error executing graph: {e}")
            return {'error': str(e)}


def main():
    """Main function to demonstrate the RetailFootfallAnalyzer."""
    try:
        # Initialize analyzer
        analyzer = RetailFootfallAnalyzer()
        
        # Example query
        query = "Analyze the footfall patterns for retail stores in Marathahalli, Bangalore. Focus on peak hours and comparison with competitors."
        
        # Run analysis
        result = analyzer.analyze(query)
        
        # Print final message content
        if 'messages' in result:
            final_message = result['messages'][-1]
            if hasattr(final_message, 'content'):
                print("\n--- Analysis Report ---")
                print(final_message.content)
        
    except Exception as e:
        print(f"Error in main execution: {e}")


if __name__ == "__main__":
    main()
