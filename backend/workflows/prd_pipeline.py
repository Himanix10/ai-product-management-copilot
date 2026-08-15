from agents.prioritization_agent import PrioritizationAgent
from agents.prd_agent import PRDAgent

def run_prd_pipeline(feature_name: str, persona: str, problem: str, reqs: str, reach: float, impact: float, conf: float, effort: float):
    p_agent = PrioritizationAgent()
    prd_agent = PRDAgent()

    p_res = p_agent.execute({"title": feature_name, "reach": reach, "impact": impact, "confidence": conf, "effort": effort})
    prd_res = prd_agent.execute({"feature_name": feature_name, "target_user": persona, "problem": problem, "requirements": reqs})

    return {
        "rice_score": p_res["score"],
        "prd_markdown": prd_res["prd_markdown"]
    }