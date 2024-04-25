import re
from subprocess import run

with open('README.md') as f:
    results = re.findall(r"```shell\s*([^`]+)```", f.read(), flags=re.MULTILINE | re.IGNORECASE)
    commands = [x.strip() for x in results if x.startswith('sdxl') and not 'listen' in x]
    failed, skipped, passed = 0, 0, 0
    process_all = False
    for c in commands:
        print(c)

        if not process_all:
            choice = input('[p]roceed, [s]kip or process [a]ll ([p]/s/a) ')
            if choice == 's':
                skipped = skipped + 1
                continue
            if choice == 'a':
                process_all = True

        result = run(c, shell=True)
        if result.returncode == 0:
            passed = passed + 1
        else:
            failed = failed + 1
    print(f"{failed=} {skipped=} {passed=}")
