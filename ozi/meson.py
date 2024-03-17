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
from mesonbuild.mparser import BaseNode
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

from ozi.tap import TAP

SelectValue: TypeAlias = type[AssignmentNode | PlusAssignmentNode | NotNode | UMinusNode]

SelectItems: TypeAlias = type[ForeachClauseNode]

WhereValue: TypeAlias = type[ArrayNode | DictNode | MethodNode | FunctionNode]

WhereItems: TypeAlias = type[IdNode]


def load_ast(source_root: str) -> CodeBlockNode | None:
    """Load the :abbr:`AST (Abstract Syntax Tree)` from the root :file:`meson.build`.

    :param source_root: Directory containing a top-level :file:`meson.build`.
    :type source_root: str
    :return: The AST for a meson build definition if one is available OR None.
    :rtype: CodeBlockNode | None
    """
    ast = AstInterpreter(source_root, '', '')  # pyright: ignore
    try:
        ast.load_root_meson_file()
    except InvalidArguments:  # pragma: no cover
        return None
    return ast.ast


def project_metadata(ast: CodeBlockNode) -> tuple[str, str]:
    """Extract project metadata from :file:`meson.build`

    :param ast: The AST for a :file:`meson.build`.
    :type ast: CodeBlockNode
    :return: The project name and license identifier.
    :rtype: tuple[str, str]
    """
    project_args = ast.lines[0].args.arguments  # pyright: ignore
    default_options = ast.lines[0].args.kwargs  # pyright: ignore
    license_ = [
        v
        for k, v in default_options.items()
        if isinstance(k, IdNode) and k.value == 'license'
    ][0]

    if isinstance(license_, ArrayNode):  # pragma: no cover
        license_ = license_.args.arguments[0]
        TAP.diagnostic(
            'Found an array of licenses in meson.build, OZI will only use the first: ',
            license_.value,  # pyright: ignore
        )

    license_ = license_.value  # pyright: ignore

    project_name, *_ = (i.value for i in project_args if isinstance(i, StringNode))

    return project_name, license_


@lru_cache(typed=True)
def query_simple(
    ast: CodeBlockNode,
    select: SelectValue = AssignmentNode,
    where: WhereValue = ArrayNode,
) -> set[BaseNode]:  # pragma: no cover
    """Run a simplistic query with no node filtering.

    :param ast: The AST for a :file:`meson.build`.
    :type ast: CodeBlockNode
    :param select: Select node type, defaults to AssignmentNode
    :type select: SelectValue, optional
    :param where: Where node type, defaults to ArrayNode
    :type where: WhereValue, optional
    :return: Set of all nodes matching the selector.
    :rtype: set[BaseNode]
    """
    matches, *_ = (
        (
            i.value.args.arguments
            for i in ast.lines
            if isinstance(i, select) and isinstance(i.value, where)
        )
        if ast
        else (_ for _ in ())
    )
    return set(matches)


@lru_cache(typed=True)
def query_complex(
    ast: CodeBlockNode,
    select: SelectValue = AssignmentNode,
    where: WhereValue = ArrayNode,
    get: type[ElementaryNode] = StringNode,
) -> set[str]:  # pragma: no cover
    """Run a complex (filtered) query of build item values.

    :param ast: The AST for a :file:`meson.build`.
    :type ast: CodeBlockNode
    :param select: select type, defaults to AssignmentNode
    :type select: SelectValue, optional
    :param where: where type, defaults to ArrayNode
    :type where: WhereValue, optional
    :param get: get type, defaults to StringNode
    :type get: type[ElementaryNode], optional
    :return: A set of node values matching the selector
    :rtype: set[str]
    """
    matches, *_ = (
        (
            i.value.args.arguments
            for i in ast.lines
            if isinstance(i, select) and isinstance(i.value, where)
        )
        if ast
        else (_ for _ in ())
    )
    return {i.value for i in matches if isinstance(i, get)}


@lru_cache(typed=True)
def query_loop_assignments(
    ast: CodeBlockNode,
    select: SelectItems = ForeachClauseNode,
    where: type[ElementaryNode] = IdNode,
    get: type[ElementaryNode] = StringNode,
) -> set[str]:  # pragma: no cover
    """Get a set of selected array items (must be assigned to a variable).

    :param ast: The AST for a :file:`meson.build`.
    :type ast: CodeBlockNode
    :param select: Select node type, defaults to ForeachClauseNode
    :type select: SelectItems, optional
    :param where: Where node type, defaults to IdNode
    :type where: WhereItems, optional
    :param get: Query node type, defaults to StringNode
    :type get: type[ElementaryNode], optional
    :return: A set of query matches
    :rtype: set[str]
    """
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
def find_var_suffix(
    ast: CodeBlockNode,
    var_suffix: str,
) -> set[str]:  # pragma: no cover
    """Get a set of build items based on a variable name suffix.

    :param ast: The AST for a :file:`meson.build`.
    :type ast: CodeBlockNode
    :param var_suffix: The text to look for.
    :type var_suffix: str
    :return: A set of query matches
    :rtype: set[str] | None
    """
    loop_vars = {
        i.items.value
        for i in ast.lines
        if isinstance(i, ForeachClauseNode)
        and isinstance(i.items, IdNode)
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
        return {i.value for i in assigned[0] if isinstance(i, StringNode)}
    else:
        return set()


def query_build_value(
    source_root: str,
    query: str,
) -> bool | None:  # pragma: no cover
    """Load a :file:`meson.build` project and check if a query exists in array assignments.

    :param source_root: The path to directory containing a :file:`meson.build`
    :type source_root: str
    :param query: The text to look for.
    :type query: str
    :return: True if a query match is found, False if not, and None if the
             :file:`meson.build` could not be loaded.
    :rtype: set[str] | None
    """
    ast = load_ast(source_root)
    if ast:
        build_data = query_complex(ast)
        return query in build_data
    return ast


def get_items_by_suffix(
    source_root: str,
    query: str,
) -> set[str] | None:  # pragma: no cover
    """Load a :file:`meson.build` project and return build items.

    :param source_root: The path to directory containing a :file:`meson.build`
    :type source_root: str
    :param query: The text to look for.
    :type query: str
    """
    ast = load_ast(source_root)
    if ast:
        return find_var_suffix(ast, query)
    return ast
