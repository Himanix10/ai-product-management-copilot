from backend.workflows.prd_pipeline import run_prd_pipeline


def test_prd_pipeline():
    res = run_prd_pipeline(
        feature_name="Dark Mode",
        persona="PMs",
        problem="Eye strain",
        reqs="Toggle in header",
        reach=2000,
        impact=1.5,
        conf=0.9,
        effort=1.0,
        acceptance_criteria="- [ ] Toggle switches theme in < 100ms.\n- [ ] State persists on page refresh."
    )
    assert res["rice_score"] == 2700.0
    assert "Dark Mode" in res["prd_markdown"]
    assert "Acceptance Criteria" in res["prd_markdown"]
    assert "Toggle switches theme" in res["acceptance_criteria"]