''' Pylint runner '''
from pylint import epylint as lint

with open("./lint/report.txt", "w+") as FILE:
    (RESULT, ERROR) = lint.py_run(
        '. --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
            --reports=n --score=n --output-format=parseable --rcfile=./lint/.pylintrc',
        return_std=True
    )
    FILE.write(RESULT.getvalue())
