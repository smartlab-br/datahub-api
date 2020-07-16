''' Pylint runner '''
import os
from pylint import epylint as lint

(RESULT, ERROR) = lint.py_run(
    '. --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
        --reports=n --score=y --output-format=parseable',
    return_std=True
)

print(RESULT.getvalue())

FILE = open(f"{os.getenv('INPUT_DEST')}/lint.txt", "w+")
FILE.write(RESULT.getvalue())
FILE.close()
