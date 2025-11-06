# router.py
import json, time

class CapsuleRouter:
    def __init__(self):
        self.routes = {
            "credit": "wealthbridge",
            "simulation": "mindmax",
            "outreach": "bridgebuilder",
            "quantum": "argus-prime"
        }

    def predict_route(self, query: str) -> str:
        for keyword, capsule in self.routes.items():
            if keyword in query.lower():
                return capsule
        return "deepagent"

if __name__ == "__main__":
    router = CapsuleRouter()
    test_query = "run credit analysis for federal worker"
    capsule = router.predict_route(test_query)
    print(f"Routing to capsule: {capsule}")
