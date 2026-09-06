from typing import Dict, Any
from agents.base_agent import BaseAgent
from backend.memory.conversation_memory import ConversationMemory
from backend.tools.retrieval_tools import RetrievalTools


class ChatAgent(BaseAgent):
    def __init__(self):
        super().__init__("ChatAgent")
        self.retrieval_tools = RetrievalTools()

    def execute(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        inputs = inputs or {}
        prompt = (inputs.get("prompt") or "").strip()
        prompt_clean = prompt.lower().strip("!.,? ")
        greetings = {"hey", "hi", "hello", "hey there", "hi there", "good morning", "good afternoon", "good evening", "greetings", "help"}
        if prompt_clean in greetings or (any(prompt_clean.startswith(g + " ") for g in ["hi", "hello", "hey"]) and len(prompt_clean) < 15):
            return {
                "agent": self.agent_name,
                "response": (
                    "Hello! 👋 **I am your AI Product Manager Copilot.**\n\n"
                    "I'm here to help you analyze customer feedback, track pain points, prioritize feature initiatives, write PRDs, and manage roadmap milestones.\n\n"
                    "**Here are a few questions you can ask me:**\n"
                    "- 🔴 *\"Explain the top customer pain points\"*\n"
                    "- 💬 *\"Show recent customer VOC feedback\"*\n"
                    "- 🚀 *\"What are our prioritized initiatives and RICE scores?\"*\n"
                    "- 📄 *\"Show active PRDs and problem statements\"*\n"
                    "- 🗓️ *\"What is planned on the roadmap?\"*\n\n"
                    "How can I assist your product workflow today?"
                ),
            }

        context = self.retrieval_tools.search_documents(prompt)
        history = ConversationMemory.get_history()
        recent_history = "\n".join(
            f"{message['role'].title()}: {message['content']}"
            for message in history[-6:]
        )
        llm_reply = self.invoke_llm(
            "You are an AI Product Manager Copilot. Answer using only the workspace "
            "context below. Do not invent records, metrics, names, or recommendations "
            "that are not supported by that context. If the context does not answer the "
            "question, say so clearly and ask a focused follow-up. Keep the answer concise.\n\n"
            f"Recent conversation:\n{recent_history}\n\n"
            f"Workspace context:\n{context}",
            prompt
        )
        if llm_reply:
            reply = llm_reply
        else:
            reply = (
                f"### 🤖 AI PM Copilot Analysis for: *\"{prompt}\"*\n\n"
                f"Here are the relevant workspace insights and records retrieved from your database:\n\n"
                f"{context}\n\n"
                f"---\n"
                f"💡 **Product Manager Recommendations:**\n"
                f"1. **Address Top Pain Points:** Review high-frequency customer feedback clusters to minimize user friction.\n"
                f"2. **Prioritize Initiatives via RICE:** Focus engineering velocity on features with high RICE scores.\n"
                f"3. **Draft PRDs:** Use the **PRD Generator** tab in the sidebar to define specifications.\n"
                f"4. **Track Milestones:** Monitor progress percentages in the **Roadmap Planner**."
            )

        return {
            "agent": self.agent_name,
            "response": reply
        }