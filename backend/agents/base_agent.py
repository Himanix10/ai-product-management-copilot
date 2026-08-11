import time
import logging
from typing import Any, Dict, Optional
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BaseAgent")

class AgentOutput(BaseModel):
    agent_name: str
    status: str
    execution_time: float
    confidence_score: float
    data: Dict[str, Any]
    error: Optional[str] = None

class BaseAgent:
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.tools: Dict[str, Any] = {}

    def register_tool(self, tool_name: str, tool_func: Any) -> None:
        self.tools[tool_name] = tool_func

    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not registered in {self.name}")
        return self.tools[tool_name](**kwargs)

    def run(self, input_data: Dict[str, Any]) -> AgentOutput:
        start_time = time.time()
        try:
            result = self._process(input_data)
            exec_time = time.time() - start_time
            return AgentOutput(
                agent_name=self.name,
                status="success",
                execution_time=round(exec_time, 3),
                confidence_score=0.95,
                data=result
            )
        except Exception as e:
            exec_time = time.time() - start_time
            logger.error(f"[{self.name}] Error: {str(e)}")
            return AgentOutput(
                agent_name=self.name,
                status="failed",
                execution_time=round(exec_time, 3),
                confidence_score=0.0,
                data={},
                error=str(e)
            )

    def _process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement _process()")