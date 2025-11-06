# handoff.py
import time

class AgentHandoff:
    def __init__(self):
        self.log = []

    def delegate(self, from_agent, to_agent, task):
        entry = {
            "from": from_agent,
            "to": to_agent,
            "task": task,
            "timestamp": time.time()
        }
        self.log.append(entry)
        print(f"Handoff: {from_agent} → {to_agent} | Task: {task}")

if __name__ == "__main__":
    handoff = AgentHandoff()
    handoff.delegate("argus-prime", "bridgebuilder", "follow up with nonprofit")
