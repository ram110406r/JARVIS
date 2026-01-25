import os

BASE_DIR = "sandbox"

os.makedirs(BASE_DIR, exist_ok=True)

def handle_filesystem(text):
    print("[Filesystem tool invoked]")

    if "create file" in text.lower():
        path = os.path.join(BASE_DIR, "example.txt")
        with open(path, "w") as f:
            f.write("Created by JARVIS")
        print(f"✅ File created at {path}")
