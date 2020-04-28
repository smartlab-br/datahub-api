''' Pylint runner '''
from pylint import epylint as lint

print(">>>>> Starting linter")
(RESULT, ERROR) = lint.py_run(
    '. --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
        --reports=n --score=n --output-format=parseable',
    return_std=True
)
print(RESULT.getvalue())

print(">>>>> Opening report file")
FILE = open("./lint/report.txt", "w+")
print(">>>>> Writing report")
FILE.write(RESULT.getvalue())
FILE.close()
print(">>>>> Done")
