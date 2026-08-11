import streamlit as st
# Direct import from backend service instead of making an HTTP request
from backend.services.prd_service import generate_prd_direct

def render_prd_generator():
    st.header("PRD Generator")
    
    workspace_id = st.session_state.get("workspace_id", 1)
    feature_title = st.text_input("Feature Title")
    
    if st.button("Generate PRD"):
        with st.spinner("Generating PRD via Agents..."):
            # Direct python call to backend logic
            response = generate_prd_direct(
                workspace_id=workspace_id, 
                feature_title=feature_title
            )
            
            if response.get("status") == "success":
                st.success("PRD Generated Successfully!")
                st.markdown(response["data"])
            else:
                st.error("Failed to generate PRD.")
