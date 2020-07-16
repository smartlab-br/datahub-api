''' Pylint runner '''
import os
from pylint import epylint as lint

(RESULT, ERROR) = lint.py_run(
    '. --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
        --reports=n --score=y --output-format=parseable',
    return_std=True
)

DEST_DIR = f"{os.getenv('GITHUB_WORKSPACE')}/{os.getenv('INPUT_DEST')}"
print(DEST_DIR)
# os.mkdir(DEST_DIR)
FILE = open(f"{DEST_DIR}/lint.txt", "w+")
FILE.write(RESULT.getvalue())
FILE.close()

with open(f"{DEST_DIR}/lint.txt", "r") as FILE:
    print(FILE.read())