from setuptools import setup

setup(
    name="mindmax",
    version="0.2",
    packages=[
        "agents",
        "agents.mindmax",
        "agents.mindmax.nim",
        "agents.deepagent",
        "agents.argus",
        "agents.vaultgemma",
        "agents.prediction_engine",
        "mcp",
        "mcp.clients",
        "mobile",
        "local_llm",
    ],
    install_requires=[],
)
