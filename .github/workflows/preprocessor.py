import os
import subprocess

os.chdir(os.getenv("GITHUB_WORKSPACE") + "\\.git")

def set_env(name, value):
    env_file = os.getenv("GITHUB_ENV")
    with open(env_file, "a") as f:
        f.write(f"{name}=\"{value}\"")

tag = os.getenv("GITHUB_REF").replace("refs/tags/", "")
print(f"Found tag '{tag}'")

subprocess.run(["git", "config", "user.name", "GithubActions"])
raw_commits = subprocess.run(["git", "log", f"{tag}..HEAD", "--oneline", "--no-decorate", "--format=\"%s\""], capture_output=True, text=True).stdout

commits = { "fix": [], "feature": [], "tweak": [] }

for line in raw_commits.split():
    lowered = line.lower().strip()

    if lowered.startswith("[fix]"):
        commits["fix"] = line[len("[fix]"):].strip()
    elif lowered.startswith("[feature]"):
        commits["feature"] = line[len("[feature]"):].strip()
    elif lowered.startswith("[tweak]"):
        commits["tweak"] = line[len("[tweak]"):].strip()

result_markdown = ""

result_markdown += "Features:\n"
for commit in commits["feature"]:
    result_markdown += f"*) {commit}\n"
result_markdown += "\n"

result_markdown += "Tweaks:\n"
for commit in commits["tweak"]:
    result_markdown += f"*) {commit}\n"
result_markdown += "\n"

result_markdown += "Fixes:\n"
for commit in commits["fix"]:
    result_markdown += f"*) {commit}\n"
result_markdown += "\n"

print(result_markdown)
