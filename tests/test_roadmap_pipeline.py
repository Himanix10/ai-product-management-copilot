from backend.workflows.roadmap_pipeline import run_roadmap_pipeline

def test_roadmap_pipeline():
    res = run_roadmap_pipeline()
    assert isinstance(res, list)