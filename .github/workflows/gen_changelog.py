import os
import subprocess

def set_env(name, value):
    env_file = os.getenv("GITHUB_ENV")
    with open(env_file, "a") as f:
        f.write(f"{name}=\"{value}\"")

tag = os.getenv("GITHUB_REF").replace("refs/tags/", "")
all_tags = subprocess.run(["git", "tag", "-l", "--sort=committerdate", "-l", "v*"], capture_output=True, text=True).stdout.split()
prev_tag = all_tags[all_tags.index(tag)-1]

print(f"Building changelogs for {prev_tag} -> {tag}")

subprocess.run(["git", "config", "user.name", "GithubActions"])
raw_commits = subprocess.run(["git", "log", f"{prev_tag}..{tag}", "--oneline", "--no-decorate", "--format=\"%s\""], capture_output=True, text=True).stdout

commits = { "fix": [], "feature": [], "tweak": [] }

for line in raw_commits.splitlines():
    line = line[1:-1]
    lowered = line.lower().strip()

    if lowered.startswith("[fix]"):
        commits["fix"] += [line[len("[fix]"):].strip()]
    elif lowered.startswith("[feature]"):
        commits["feature"] += [line[len("[feature]"):].strip()]
    elif lowered.startswith("[tweak]"):
        commits["tweak"] += [line[len("[tweak]"):].strip()]

result_markdown = f"Update **{tag}**\n"

result_markdown += "**Features:**\n"
for commit in commits["feature"]:
    result_markdown += f"*) {commit}\n"
result_markdown += "\n"

result_markdown += "**Tweaks:**\n"
for commit in commits["tweak"]:
    result_markdown += f"*) {commit}\n"
result_markdown += "\n"

result_markdown += "**Fixes:**\n"
for commit in commits["fix"]:
    result_markdown += f"*) {commit}\n"
result_markdown += "\n"

print(result_markdown)

with open("changelog.md", "w") as f:
    f.write(f"```{result_markdown}```")
