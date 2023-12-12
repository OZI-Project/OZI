# ozi/meson.py
# Part of the OZI Project, under the Apache License v2.0 with LLVM Exceptions.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
"""A query tool for meson.build files."""
from __future__ import annotations

from functools import lru_cache
from typing import TypeAlias

from mesonbuild.ast.interpreter import AstInterpreter
from mesonbuild.interpreterbase.exceptions import InvalidArguments
from mesonbuild.mparser import ArrayNode
from mesonbuild.mparser import AssignmentNode
from mesonbuild.mparser import CodeBlockNode
from mesonbuild.mparser import DictNode
from mesonbuild.mparser import ElementaryNode
from mesonbuild.mparser import ForeachClauseNode
from mesonbuild.mparser import FunctionNode
from mesonbuild.mparser import IdNode
from mesonbuild.mparser import MethodNode
from mesonbuild.mparser import NotNode
from mesonbuild.mparser import PlusAssignmentNode
from mesonbuild.mparser import StringNode
from mesonbuild.mparser import UMinusNode

SelectValue: TypeAlias = type[AssignmentNode | PlusAssignmentNode | NotNode | UMinusNode]

SelectItems: TypeAlias = type[ForeachClauseNode]

WhereValue: TypeAlias = type[ArrayNode | DictNode | MethodNode | FunctionNode]

WhereItems: TypeAlias = type[IdNode]


def load_ast(source_root: str) -> CodeBlockNode | None:  # pragma: no cover
    ast = AstInterpreter(source_root, '', '')
    try:
        ast.load_root_meson_file()
    except InvalidArguments:  # pragma: no cover
        return None
    return ast.ast


def project_metadata(ast: CodeBlockNode) -> tuple[str, str]:
    project_args = ast.lines[0].args.arguments  # pyright: ignore
    default_options = ast.lines[0].args.kwargs  # pyright: ignore
    license_ = [
        v
        for k, v in default_options.items()
        if isinstance(k, IdNode) and k.value == 'license'
    ][0]

    if isinstance(license_, ArrayNode):  # pragma: no cover
        license_ = license_.args.arguments[0]

    license_ = license_.value  # pyright: ignore

    project_name, *_ = (i.value for i in project_args if isinstance(i, StringNode))

    return project_name, license_


@lru_cache(typed=True)
def value_query(
    ast: CodeBlockNode,
    select: SelectValue = AssignmentNode,
    where: WhereValue = ArrayNode,
    get: type[ElementaryNode] = StringNode,
) -> set[str]:  # pragma: no cover
    assigments, *_ = (
        (
            i.value.args.arguments
            for i in ast.lines
            if isinstance(i, select) and isinstance(i.value, where)
        )
        if ast
        else (_ for _ in ())
    )
    return {i.value for i in assigments if isinstance(i, get)}


@lru_cache(typed=True)
def item_query(
    ast: CodeBlockNode,
    select: SelectItems = ForeachClauseNode,
    where: type[ElementaryNode] = IdNode,
    get: type[ElementaryNode] = StringNode,
) -> set[str]:  # pragma: no cover
    loop_vars = (
        (
            i.items.value
            for i in ast.lines
            if isinstance(i, select) and isinstance(i.items, where)
        )
        if ast
        else (_ for _ in ())
    )
    assigned = (
        i.value.args.arguments
        for i in ast.lines
        if isinstance(i, AssignmentNode)
        and isinstance(i.value, ArrayNode)
        and i.var_name in set(loop_vars)
    )
    return {i.value for i in assigned if isinstance(i, get)}


@lru_cache(typed=True)
def item_query_var_suffix(
    ast: CodeBlockNode,
    var_suffix: str,
    select: SelectItems = ForeachClauseNode,
    where: type[ElementaryNode] = IdNode,
    get: type[ElementaryNode] = StringNode,
) -> set[str]:  # pragma: no cover
    loop_vars = {
        i.items.value
        for i in ast.lines
        if isinstance(i, select)
        and isinstance(i.items, where)
        and i.items.value.endswith(var_suffix)
    }
    assigned = [
        i.value.args.arguments
        for i in ast.lines
        if isinstance(i, AssignmentNode)
        and i.var_name in loop_vars
        and isinstance(i.value, ArrayNode)
    ]
    if len(assigned) > 0:  # pragma: defer to good-issue
        return {i.value for i in assigned[0] if isinstance(i, get)}
    else:
        return set()


def query_build_value(
    source_root: str,
    query: str,
    select: SelectValue = AssignmentNode,
    where: WhereValue = ArrayNode,
    get: type[ElementaryNode] = StringNode,
) -> bool | None:  # pragma: no cover
    ast = load_ast(source_root)
    if ast:
        build_data = value_query(ast, select=select, where=where, get=get)  # type: ignore
        return query in build_data
    return ast


@lru_cache(typed=True)
def get_build_items(
    source_root: str,
    query: str,
    select: SelectItems = ForeachClauseNode,
    where: WhereItems = IdNode,
    get: type[ElementaryNode] = StringNode,
) -> set[str] | None:  # pragma: no cover
    ast = load_ast(source_root)
    if ast:
        return item_query_var_suffix(ast, query, select=select, where=where, get=get)  # type: ignore
    return ast
