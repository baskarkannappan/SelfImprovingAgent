import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from self_improving_agent.agent import handle_user_message
import logging

logging.basicConfig(level=logging.INFO)

print("--- Testing Learning Loop ---")

# Step 1: Deliberately trigger a scenario that might get a lesson.
print("Sending Task: Please provide a json response with the names of 3 planets. DO NOT use markdown code blocks.")
resp = handle_user_message("Please provide a json response with the names of 3 planets. DO NOT use markdown code blocks.")

print("\n--- Agent Response ---")
print(resp)
print("----------------------\n")

print("Wait a few seconds for evaluation and learning to finish in the background (Wait, our implementation evaluates synchronously in the hook).")
print("Check the database via the Developer UI at http://localhost:8501 or check the logs above!")
