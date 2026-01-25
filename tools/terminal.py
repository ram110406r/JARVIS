import subprocess

def handle_terminal(text):
    print("[Terminal tool requested]")

    if "ls" in text:
        print("🔍 Dry run: ls")
        result = subprocess.run(
            ["ls"],
            capture_output=True,
            text=True,
            shell=True
        )
        print(result.stdout)
