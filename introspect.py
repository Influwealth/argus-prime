# introspect.py
import os

class CapsuleIntrospector:
    def __init__(self, base_path="capsules"):
        self.base_path = base_path

    def list_capsules(self):
        return [f for f in os.listdir(self.base_path) if f.endswith(".yaml")]

    def check_health(self, capsule_name):
        path = os.path.join(self.base_path, capsule_name + ".yaml")
        return os.path.exists(path)

if __name__ == "__main__":
    introspector = CapsuleIntrospector()
    print("Available Capsules:", introspector.list_capsules())
    print("Argus Health:", introspector.check_health("argus-prime"))
