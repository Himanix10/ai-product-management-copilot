# Architecture Documentation

The AI Product Manager Copilot is implemented as a multi-agent system built directly over Streamlit and Google Gemini.

## Decoupled Architecture
- **Framework Independency**: Standard Python + SQLite with connection pooling.
- **LLM Engine**: Google Gemini Developer API integration via `google-genai`.
- **No Vector DB Overhead**: Direct structured SQLite operations for feedback, pain points, initiatives, and PRDs.
- **Dynamic NLP Pipeline**: Dynamic VADER sentiment scoring and adaptive Silhouette KMeans clustering.