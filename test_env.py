import os
from dotenv import load_dotenv

load_dotenv()

print("VISION_ENDPOINT:", os.getenv("VISION_ENDPOINT"))
print("VISION_KEY:", "FOUND" if os.getenv("VISION_KEY") else "NOT FOUND")

