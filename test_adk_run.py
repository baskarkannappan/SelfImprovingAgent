import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from self_improving_agent.agent import self_improving_agent
import logging

logging.basicConfig(level=logging.INFO)

def main():
    res = self_improving_agent.run("what is 12 + 67")
    print(res)

if __name__ == "__main__":
    main()
