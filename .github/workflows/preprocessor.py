import os
 
for k, v in os.environ.items():
    print(f'{k}={v}')


print()

import os

env_file = os.getenv('GITHUB_ENV')

with open(env_file, "a") as myfile:
    myfile.write("MY_VAR=This comes from python, yea")