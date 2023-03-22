# Process output from `vault operator init` and write to files in the .secrets directory:

output = """
Unseal Key 1: <redacted>
Unseal Key 2: <redacted>
Unseal Key 3: <redacted>
Unseal Key 4: <redacted>
Unseal Key 5: <redacted>

Initial Root Token: <redacted>
"""

import re
import pathlib
for line in output.splitlines(keepends=False):
    got = re.match(r"^Unseal Key ([0-9])\: (.*)$", line)
    if got:
        num = got.group(1)
        key = got.group(2)
        p :pathlib.Path = pathlib.Path.home() / ".secrets" / "hashicorp-vault" / f"unseal_key{num}.txt"
        p.write_text (key)
        print (f"Wrote Unseal Key {num} to {p}")
    got = re.match(r"^Initial Root Token\: (.*)$", line)
    if got:
        token = got.group(1)
        p :pathlib.Path = pathlib.Path.home() / ".secrets" / "hashicorp-vault" / f"initial_root_token.txt"
        p.write_text (token)
        print (f"Wrote Initial Root Token to {p}")