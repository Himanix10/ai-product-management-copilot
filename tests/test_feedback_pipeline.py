from backend.workflows.feedback_pipeline import run_feedback_pipeline

def test_feedback_pipeline():
    res = run_feedback_pipeline("CRM", "Lead", "Need bulk export", "Feature Request")
    assert "ingestion" in res
    assert "themes" in res
    assert "clusters" in res