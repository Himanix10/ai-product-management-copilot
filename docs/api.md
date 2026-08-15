# API Specifications

- `IngestionAgent.execute(inputs)`: Sanitizes VOC narrative and applies VADER sentiment analysis.
- `ClusteringAgent.execute(inputs)`: TF-IDF + Adaptive Silhouette KMeans feedback grouping.
- `PrioritizationAgent.execute(inputs)`: Calculates RICE score (`(Reach * Impact * Confidence) / Effort`).
- `PRDAgent.execute(inputs)`: Generates Markdown PRD specifications via Google Gemini.
- `ChatAgent.execute(inputs)`: Contextual product management queries powered by Google Gemini.