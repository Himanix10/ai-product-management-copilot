from backend.workflows.end_to_end_pipeline import run_end_to_end_pipeline

def test_end_to_end_pipeline():
    res = run_end_to_end_pipeline(
        source="Zendesk",
        user_type="PM",
        text="Export PRDs to PDF",
        category="Feature Request",
        feature_title="Export PRDs",
        reach=1000,
        impact=2.0,
        conf=0.8,
        effort=1.0
    )
    assert "feedback_stage" in res
    assert "prd_stage" in res
    assert "roadmap_stage" in res