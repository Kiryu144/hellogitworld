import os

def set_env(name, value):
    env_file = os.getenv('GITHUB_ENV')
    with open(env_file, "a") as f:
        f.write(f"{name}=\"{value}\"")

print("Ref: " + os.getenv('GITHUB_ENV'))