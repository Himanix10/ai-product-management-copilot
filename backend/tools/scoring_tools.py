class ScoringTools:
    @staticmethod
    def calculate_rice(reach: float, impact: float, confidence: float, effort: float) -> float:
        if effort <= 0:
            raise ValueError("Effort must be greater than zero.")
        return round((reach * impact * confidence) / effort, 2)

    @staticmethod
    def calculate_ice(impact: float, confidence: float, ease: float) -> float:
        return round(impact * confidence * ease, 2)