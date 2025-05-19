import streamlit as st
import plotly.graph_objects as go
import networkx as nx
from typing import Dict, List, Any
import httpx
import json

class BaseVisualizer:
    def __init__(self, endpoint: str):
        # Change API URL to include /api prefix
        self.api_url = f"http://localhost:8000/api/visualization/{endpoint}"
        
    async def _make_request(self, payload: Dict) -> Dict:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.api_url,
                    json=payload,
                    timeout=30.0
                )
                # Add debug logging
                st.write(f"API Response: {response.status_code}")
                st.write(f"Response content: {response.text}")
                
                if response.status_code == 404:
                    st.error("API endpoint not found. Make sure the backend server is running.")
                    return None
                response.raise_for_status()
                data = response.json()
                if not data.get("success", False):
                    st.error(f"API Error: {data.get('error', 'Unknown error')}")
                    return None
                return data.get("data", {})
            except httpx.ConnectError:
                st.error("Cannot connect to the API. Is the backend server running?")
                return None
            except Exception as e:
                st.error(f"API Error: {str(e)}")
                return None

class CodeFlowDiagram(BaseVisualizer):
    def __init__(self):
        super().__init__("code-flow")
        
    async def render(self, code: str, title: str = "Code Flow Diagram"):
        with st.spinner("Analyzing code structure..."):
            data = await self._make_request({"code": code})
            if data:
                self._render_graph(data, title)

    def _render_graph(self, graph_data: Dict, title: str):
        G = nx.DiGraph()
        
        # Add nodes and edges from graph_data
        for node in graph_data["nodes"]:
            G.add_node(node["id"], label=node["label"], type=node["type"])
        
        for edge in graph_data["edges"]:
            G.add_edge(edge["source"], edge["target"], label=edge["label"])

        # Create Plotly figure
        pos = nx.spring_layout(G)
        
        # Create edges trace
        edge_trace = go.Scatter(
            x=[], y=[], line=dict(width=1, color="#888"), 
            hoverinfo='none', mode='lines'
        )
        
        # Add edges to trace
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace.x += (x0, x1, None)
            edge_trace.y += (y0, y1, None)

        # Create nodes trace
        node_trace = go.Scatter(
            x=[], y=[], text=[], mode='markers+text',
            hoverinfo='text', textposition="bottom center",
            marker=dict(size=30, color='#1f77b4')
        )

        # Add nodes to trace
        for node in G.nodes():
            x, y = pos[node]
            node_trace.x += (x,)
            node_trace.y += (y,)
            node_trace.text += (G.nodes[node]['label'],)

        # Create figure
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title=title,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                plot_bgcolor='white'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

class AlgorithmVisualizer(BaseVisualizer):
    def __init__(self):
        super().__init__("algorithm-visualization")
    
    async def render(self, code: str, input_data: List[Any]):
        with st.spinner("Generating algorithm visualization..."):
            payload = {
                "code": code,
                "input_data": input_data
            }
            st.write("Sending payload:", payload)  # Debug info
            data = await self._make_request(payload)
            if data:
                try:
                    self._render_animation(data)
                except KeyError as e:
                    st.error(f"Missing required field in response: {e}")
                except Exception as e:
                    st.error(f"Error rendering animation: {e}")

    def _render_animation(self, animation_data: Dict):
        steps = animation_data["steps"]
        complexity = animation_data["complexity"]
        
        # Show complexity information
        st.info(f"Time Complexity: {complexity['time']}")
        st.info(f"Space Complexity: {complexity['space']}")
        
        # Create step-by-step visualization
        for step in steps:
            with st.expander(f"Step {step['step']}: {step['description']}", expanded=False):
                # Show current state
                st.json(step["state"])
                # Show highlighted elements
                if step["highlight"]:
                    st.write("Highlighted elements:", step["highlight"])

class PerformanceComparison(BaseVisualizer):
    def __init__(self):
        super().__init__("performance-comparison")
    
    async def render(self, codes: Dict[str, str], input_sizes: List[int]):
        with st.spinner("Analyzing algorithm performance..."):
            data = await self._make_request({"codes": codes, "input_sizes": input_sizes})
            if data:
                self._render_chart(data, input_sizes)

    def _render_chart(self, performance_data: Dict, input_sizes: List[int]):
        fig = go.Figure()
        
        for algo in performance_data["algorithms"]:
            fig.add_trace(go.Scatter(
                x=input_sizes,
                y=algo["time"],
                mode='lines+markers',
                name=f"{algo['name']} (Time)",
            ))
            
        fig.update_layout(
            title="Algorithm Performance Comparison",
            xaxis_title="Input Size",
            yaxis_title="Time (ms)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)