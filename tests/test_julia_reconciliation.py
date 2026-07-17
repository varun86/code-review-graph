"""Regression coverage for the safe Julia behavior ported from PR #560."""

from pathlib import Path

import pytest

from code_review_graph.parser import CodeParser


def _parse(source: str):
    return CodeParser().parse_bytes(
        Path("/repo/case.jl"),
        source.encode("utf-8"),
    )


def test_function_stub_is_a_function():
    nodes, _ = _parse("function hook end")

    assert [
        (node.kind, node.name)
        for node in nodes
        if node.kind != "File"
    ] == [("Function", "hook")]


def test_malformed_qualified_stub_fails_soft():
    nodes, edges = _parse("function A.B.hook end")

    assert [node.kind for node in nodes] == ["File"]
    assert edges == []


@pytest.mark.parametrize(
    ("signature", "expected"),
    [
        ("+(a, b) = a", "+"),
        ("Base.:+(a, b) = a", "+"),
        ("Base.:(==)(a, b) = true", "=="),
    ],
)
def test_operator_definition_uses_operator_name(signature, expected):
    nodes, _ = _parse(signature)

    assert [
        node.name for node in nodes if node.kind == "Function"
    ] == [expected]


def test_parameterized_const_only_is_a_type():
    nodes, _ = _parse(
        "const FloatVec = Vector{Float64}\n"
        "const PairMap = Dict{String, Tuple{Int, Int}}\n"
        "const MAX_RETRIES = 3\n"
    )

    assert {
        node.name for node in nodes if node.kind == "Type"
    } == {"FloatVec", "PairMap"}


def test_import_alias_records_real_dependency():
    _, edges = _parse(
        "import DataFrames as DF\n"
        "import Tables: AbstractColumns as Columns\n"
    )

    assert {
        edge.target for edge in edges if edge.kind == "IMPORTS_FROM"
    } == {"DataFrames", "Tables.AbstractColumns"}
