# Stubs for symbol (Python 3)

import sys
from typing import Dict

single_input: int
file_input: int
eval_input: int
decorator: int
decorators: int
decorated: int
if sys.version_info >= (3, 5):
    async_funcdef: int
funcdef: int
parameters: int
typedargslist: int
tfpdef: int
varargslist: int
vfpdef: int
stmt: int
simple_stmt: int
small_stmt: int
expr_stmt: int
if sys.version_info >= (3, 6):
    annassign: int
testlist_star_expr: int
augassign: int
del_stmt: int
pass_stmt: int
flow_stmt: int
break_stmt: int
continue_stmt: int
return_stmt: int
yield_stmt: int
raise_stmt: int
import_stmt: int
import_name: int
import_from: int
import_as_name: int
dotted_as_name: int
import_as_names: int
dotted_as_names: int
dotted_name: int
global_stmt: int
nonlocal_stmt: int
assert_stmt: int
compound_stmt: int
if sys.version_info >= (3, 5):
    async_stmt: int
if_stmt: int
while_stmt: int
for_stmt: int
try_stmt: int
with_stmt: int
with_item: int
except_clause: int
suite: int
test: int
test_nocond: int
lambdef: int
lambdef_nocond: int
or_test: int
and_test: int
not_test: int
comparison: int
comp_op: int
star_expr: int
expr: int
xor_expr: int
and_expr: int
shift_expr: int
arith_expr: int
term: int
factor: int
power: int
if sys.version_info >= (3, 5):
    atom_expr: int
atom: int
testlist_comp: int
trailer: int
subscriptlist: int
subscript: int
sliceop: int
exprlist: int
testlist: int
dictorsetmaker: int
classdef: int
arglist: int
argument: int
comp_iter: int
comp_for: int
comp_if: int
encoding_decl: int
yield_expr: int
yield_arg: int

sym_name: Dict[int, str]
