import streamlit as st

def render_roadmap():
    st.title("Roadmap Planner")
    st.caption("Plan quarters and drag-and-drop initiatives.")

    col_hdr1, col_hdr2, col_hdr3 = st.columns([4, 1.5, 1.5])
    with col_hdr2:
        if st.button("AI Suggest Order", use_container_width=True):
            st.toast("AI Agent re-ordered initiatives by RICE priority score.")
    with col_hdr3:
        if st.button("+ Add Milestone", type="primary", use_container_width=True):
            st.session_state.show_add_modal = True

    st.divider()

    initiatives_data = [
        {"id": 1, "quarter": "Q1", "title": "Excel Export", "status": "In Progress", "order": 1, "progress": 65},
        {"id": 2, "quarter": "Q1", "title": "Performance & Speed", "status": "Planned", "order": 2, "progress": 0},
        {"id": 3, "quarter": "Q1", "title": "Offline Mode", "status": "In Progress", "order": 3, "progress": 65},
        {"id": 4, "quarter": "Q1", "title": "Custom Notifications", "status": "Completed", "order": 4, "progress": 100},
        
        {"id": 5, "quarter": "Q2", "title": "Offline Mode", "status": "Completed", "order": 1, "progress": 100},
        {"id": 6, "quarter": "Q2", "title": "Excel Export", "status": "Backlog", "order": 2, "progress": 0},
        {"id": 7, "quarter": "Q2", "title": "Bulk Upload", "status": "In Progress", "order": 3, "progress": 65},
        
        {"id": 8, "quarter": "Q3", "title": "Offline Mode", "status": "In Progress", "order": 1, "progress": 65},
        {"id": 9, "quarter": "Q3", "title": "Custom Notifications", "status": "In Progress", "order": 2, "progress": 65},
        {"id": 10, "quarter": "Q3", "title": "Mobile App", "status": "Backlog", "order": 3, "progress": 0},
        
        {"id": 11, "quarter": "Q4", "title": "Advanced Filters", "status": "In Progress", "order": 1, "progress": 65},
        {"id": 12, "quarter": "Q4", "title": "Dark Mode", "status": "In Progress", "order": 2, "progress": 65},
        {"id": 13, "quarter": "Q4", "title": "Bulk Upload", "status": "Planned", "order": 3, "progress": 0},
    ]

    q_cols = st.columns(4)
    quarters = [("Q1", "194"), ("Q2", "184"), ("Q3", "144"), ("Q4", "178")]
    statuses = ["Planned", "In Progress", "Completed", "Backlog"]

    for idx, (q_name, count) in enumerate(quarters):
        with q_cols[idx]:
            st.markdown(f"#### {q_name} <span style='float:right; color:gray; font-size:14px;'>{count}</span>", unsafe_allow_html=True)
            q_items = [item for item in initiatives_data if item["quarter"] == q_name]
            
            for item in q_items:
                with st.container(border=True):
                    st.markdown(f"**{item['title']}**")
                    c_status, c_order = st.columns([2, 1])
                    with c_status:
                        st.selectbox(
                            "Status",
                            options=statuses,
                            index=statuses.index(item["status"]),
                            key=f"status_{q_name}_{item['id']}",
                            label_visibility="collapsed"
                        )
                    with c_order:
                        st.caption(f"Order: {item['order']}")
                    
                    st.progress(item["progress"] / 100)
                    st.caption(f"{item['progress']}% completed")

    if getattr(st.session_state, "show_add_modal", False):
        with st.form("add_milestone_form"):
            st.subheader("Add New Roadmap Milestone")
            new_title = st.text_input("Initiative Title", value="New Analytics Endpoint")
            new_q = st.selectbox("Quarter", ["Q1", "Q2", "Q3", "Q4"])
            new_status = st.selectbox("Status", statuses)
            
            if st.form_submit_button("Save Milestone", type="primary"):
                st.session_state.show_show_add_modal = False
                st.success(f"Added **{new_title}** to **{new_q}** roadmap.")
                st.rerun()