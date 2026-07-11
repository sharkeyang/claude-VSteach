# quick syntax check
import ast, sys
f = sys.argv[1]
try:
    ast.parse(open(f, encoding='utf-8').read())
    print("OK:", f)
except SyntaxError as e:
    print("FAIL:", f, "-", e.msg, "line", e.lineno)
    sys.exit(1)