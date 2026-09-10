# frontend/dashboard_sections/__init__.py

from .Dashboard_Overview import render_dashboard_overview
from .Customer_Feedback import render_customer_feedback
from .Feedback_Explorer import render_feedback_explorer
from .Customer_Pain_Points import render_customer_pain_points
from .Feature_Requests import render_feature_requests
from .Prioritized_Initiatives import render_prioritized_initiatives
from .PRD_Generator import render_prd_generator
from .Roadmap import render_roadmap
from .Product_Analytics import render_product_analytics
from .Chat_Assistant import render_chat_assistant


__all__ = [
    "render_dashboard_overview",
    "render_customer_feedback",
    "render_feedback_explorer",
    "render_customer_pain_points",
    "render_feature_requests",
    "render_prioritized_initiatives",
    "render_prd_generator",
    "render_roadmap",
    "render_product_analytics",
    "render_chat_assistant",
]