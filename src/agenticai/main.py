import streamlit as st
from src.agenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.agenticai.LLMS.groqllm import GroqLLM
from src.agenticai.graph.graph_builder import GraphBuilder
from src.agenticai.ui.streamlitui.display_results import DisplayResultsStreamlit

def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while
    implementing exception handling for robusteness.
    
    """
    
    ## Load UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    
    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    user_message = st.chat_input("Enter your message: ")
    
    if user_message:
        try:
            # Configuration The LLM
            obj_llm_config = GroqLLM(user_controls=user_input)
            model = obj_llm_config.get_llm_model()
            
            
            if not model:
                st.error("Error: LLM model could not be intialized.")
                return
            
            # Initialize and set up the graph based on use case
            usecase = user_input.get('selected_usecase')
            
            if not usecase:
                st.error("Error: Use case not selected.")
                return 
            
            # Graph builder
            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultsStreamlit(usecase,graph,user_message).display_results_on_ui()
            except Exception as e:
                st.error(f"Error occurred while building the graph: {e}")
                return
        except Exception as e:
            st.error(f"Error occurred while configuring LLM: {e}")
            return