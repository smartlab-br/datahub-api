from pylint import epylint as lint

print(">>>>> Starting linter")
# pylint ./app/**/*.py --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" --reports=n --score=n --output-format=parseable
(result, error) = lint.py_run('. --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" --reports=n --score=n --output-format=parseable', return_std=True)
print(result.getvalue())
# (result, error) = lint.py_run('.')

print(">>>>> Opening report file")
f = open("./lint/report.txt", "w+")
print(">>>>> Writing report")
f.write(result.getvalue())
f.close()
print(">>>>> Done")