<%!
    exec(compile(open("verify.py").read(), "verify.py", "exec"))
    c = verify.__code__
%>
import sys
from types import CodeType, FunctionType

exec('assert sys.version_info == (3, 12, 8, "final", 0)')

verify = FunctionType(
    CodeType(
        ${c.co_argcount},
        ${c.co_posonlyargcount},
        ${c.co_kwonlyargcount},
        ${c.co_nlocals},
        ${c.co_stacksize},
        ${c.co_flags},
        ${c.co_code},
        ${c.co_consts},
        ${c.co_names},
        ${c.co_varnames},
        "chall.py",
        ${repr(c.co_name)},
        ${repr(c.co_qualname)},
        ${c.co_firstlineno},
        ${c.co_linetable},
        ${c.co_exceptiontable},
        ${c.co_freevars},
        ${c.co_cellvars}
    ),
    globals()
)
print((verify(input("Enter flag: ")) and "Correct!") or "Wrong!")
