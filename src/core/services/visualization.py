"""
Visualization service for generating lecture analysis charts.
"""

from __future__ import annotations

from typing import Sequence

import plotly.graph_objects as go

from .metrics import Utterance


class ChartGenerator:
    """
    Generates interactive visualizations for lecture analysis.
    """
    
    ENGAGING_COLOR = "green"
    NON_ENGAGING_COLOR = "red"
    
    def create_engagement_timeline(self, utterances: Sequence[Utterance]) -> str:
        """Create an engagement timeline chart."""
        if not utterances:
            return ""
        
        engaging_periods: list[tuple[float, float]] = []
        non_engaging_periods: list[tuple[float, float]] = []
        
        for utterance in utterances:
            start_min = utterance.start_time_ms / 60000
            end_min = utterance.end_time_ms / 60000
            
            if utterance.emotion.is_engaging:
                engaging_periods.append((start_min, end_min))
            else:
                non_engaging_periods.append((start_min, end_min))
        
        min_time = utterances[0].start_time_ms / 60000
        max_time = utterances[-1].end_time_ms / 60000
        
        fig = go.Figure()
        
        for start, end in non_engaging_periods:
            fig.add_shape(
                type="rect",
                x0=start, x1=end, y0=4, y1=16,
                line=dict(color=self.NON_ENGAGING_COLOR),
                fillcolor=self.NON_ENGAGING_COLOR,
            )
        
        for start, end in engaging_periods:
            fig.add_shape(
                type="rect",
                x0=start, x1=end, y0=4, y1=16,
                line=dict(color=self.ENGAGING_COLOR),
                fillcolor=self.ENGAGING_COLOR,
            )
        
        # Legend traces
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode="markers",
            marker=dict(size=10, color=self.ENGAGING_COLOR),
            name="Engaging", showlegend=True,
        ))
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode="markers",
            marker=dict(size=10, color=self.NON_ENGAGING_COLOR),
            name="Non-Engaging", showlegend=True,
        ))
        
        fig.update_layout(
            xaxis=dict(title="Time (minutes)", range=[min_time, max_time], tickmode="auto", nticks=10),
            yaxis=dict(tickvals=[10], ticktext=["Engagement"], range=[0, 25]),
            showlegend=True,
            height=300,
            width=800,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40, r=40, t=20, b=40),
        )
        
        return fig.to_html(full_html=False)

