# test_key.py
import os
k = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
print("Has key?", bool(k))
if k:
    print("Masked:", k[:4] + "..." + k[-4:])
