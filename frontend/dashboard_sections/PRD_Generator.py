import streamlit as st

def render_prd_generator():
    st.title("PRD Generator")
    st.caption("Automatically draft Product Requirement Documents using AI Agents")

    initiative = st.selectbox(
        "Select Prioritized Initiative", 
        ["Dashboard Performance Optimization", "Jira Webhook Integration", "Dark Mode Theme"]
    )
    
    if st.button("Generate PRD with AI Agent", type="primary"):
        with st.spinner("AI PRD Agent compiling specifications..."):
            st.markdown(f"""
            ---
            # PRD: {initiative}
            
            **Document ID:** `PRD-501` | **Status:** `Approved` | **Target Quarter:** `Q3 2026`  

            ### 1. Executive Summary
            Operational requirements to execute **{initiative}**, resolving key user pain points.

            ### 2. Objectives & Key Results (OKRs)
            * Reduce P95 analytics query latency under **2.0 seconds**.
            * Improve platform CSAT score by **15%**.

            ### 3. Functional Requirements
            * **FR-1:** Implement server-side caching for repeat analytical queries.
            * **FR-2:** The API shall return structured HTTP timeout warnings.

            ### 4. Acceptance Criteria
            * **Given** a logged-in Product Lead, **When** opening dashboard, **Then** all widgets load in **< 2 seconds**.
            ---
            """)
