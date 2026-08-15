from backend.workflows.prd_pipeline import run_prd_pipeline

def test_prd_pipeline():
    res = run_prd_pipeline("Dark Mode", "PMs", "Eye strain", "Toggle in header", 2000, 1.5, 0.9, 1.0)
    assert res["rice_score"] == 2700.0
    assert "Dark Mode" in res["prd_markdown"]