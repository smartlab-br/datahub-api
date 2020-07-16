''' Pylint runner '''
import os
from pylint import epylint as lint

(RESULT, ERROR) = lint.py_run(
    '. --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
        --reports=n --score=y --output-format=parseable',
    return_std=True
)

FILE_DEST = f"{os.getenv('GITHUB_WORKSPACE')}/{os.getenv('INPUT_DEST')}/lint.txt"
print(FILE_DEST)
FILE = open(FILE_DEST, "w+")
FILE.write(RESULT.getvalue())
FILE.close()

with open(FILE_DEST, "r") as FILE:
    print(FILE.read())