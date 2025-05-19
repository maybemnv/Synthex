import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
import streamlit as st
from components.visualizations import CodeFlowDiagram, AlgorithmVisualizer, PerformanceComparison
import asyncio

st.set_page_config(page_title="Code Visualization", layout="wide")

def main():
    st.title("Code Visualization Tools")
    
    tab1, tab2, tab3 = st.tabs(["Code Flow", "Algorithm Steps", "Performance"])
    
    with tab1:
        st.header("Code Flow Diagram")
        code = st.text_area("Enter your code:", height=200)
        if st.button("Generate Flow Diagram"):
            if code:
                flow_diagram = CodeFlowDiagram()
                asyncio.run(flow_diagram.render(code))
            else:
                st.warning("Please enter some code.")
    
    with tab2:
        st.header("Algorithm Visualization")
        algo_code = st.text_area("Enter algorithm code:", height=200, key="algo")
        input_data = st.text_input("Input data (comma-separated):", "5,2,9,1,7")
        if st.button("Visualize Algorithm"):
            if algo_code:
                try:
                    input_list = [int(x.strip()) for x in input_data.split(",")]
                    visualizer = AlgorithmVisualizer()
                    asyncio.run(visualizer.render(algo_code, input_list))
                except ValueError:
                    st.error("Invalid input data format.")
            else:
                st.warning("Please enter algorithm code.")
    
    with tab3:
        st.header("Performance Comparison")
        algo1 = st.text_area("Algorithm 1:", height=150, key="algo1")
        algo2 = st.text_area("Algorithm 2:", height=150, key="algo2")
        sizes = st.text_input("Input sizes (comma-separated):", "10,100,1000")
        
        if st.button("Compare Performance"):
            if algo1 and algo2:
                try:
                    size_list = [int(x.strip()) for x in sizes.split(",")]
                    codes = {"Algorithm 1": algo1, "Algorithm 2": algo2}
                    comparison = PerformanceComparison()
                    asyncio.run(comparison.render(codes, size_list))
                except ValueError:
                    st.error("Invalid input sizes format.")
            else:
                st.warning("Please enter both algorithms.")

if __name__ == "__main__":
    main()