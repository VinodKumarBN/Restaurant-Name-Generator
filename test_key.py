import os
k = os.getenv("OPENROUTER_API_KEY") 
print("Has key?", bool(k))
if k:
    print("Masked:", k[:4] + "..." + k[-4:])
