import ast
from typing import Iterable

from transpiler.phases.emit_cpp.function import emit_function
from transpiler.phases.emit_cpp.visitors import join, NodeVisitor
from transpiler.phases.typing.expr import ScoperExprVisitor
from transpiler.phases.typing.types import ConcreteType, TypeVariable, RuntimeValue, TY_OBJECT, GenericInstanceType

def emit_base_type(t: list[ConcreteType]):
    match t:
        case []:
            yield "referencemodel::object"
        case [par] if isinstance(par, GenericInstanceType) and not par.generic_args:
            yield "decltype(" + par.generic_parent.name() + ")"
        case [head, *tail] if tail:
            yield "referencemodel::meta::rebase<"
            yield from emit_base_type([head])
            yield ","
            yield from emit_base_type(tail)
            yield ">"
        case _:
            raise NotImplementedError("parent not handled yet: " + str(t))

def emit_class(name: str, node: ConcreteType) -> Iterable[str]:
    __TB_NODE__ = node.block_data.node
    yield "template <typename _Base0 ="
    yield from emit_base_type(node.get_mro()[1:-1])
    yield ">"
    yield f"struct {name}__oo : referencemodel::classtype<_Base0, {name}__oo<>> {{"
    yield f"static constexpr std::string_view name = \"{name}\";"
    yield f"auto operator=(const {name}__oo&) const {{ return *this; }}"

    # inner = ClassInnerVisitor2(node.inner_scope)
    # for stmt in node.body:
    #     yield from inner.visit(stmt)

    parameters = node.generic_parent.parameters if isinstance(node, GenericInstanceType) else []

    def template_params():
        if parameters:
            yield from (p.name for p in parameters)
        else:
            yield "_Void"

    yield "template<"
    yield from join(",", (f"typename {name}" for name in template_params()))
    yield ">"
    yield f"struct Obj : referencemodel::instance<{name}__oo<>, Obj"
    yield "<"
    if parameters:
        yield from join(",", (p.name for p in parameters))
    else:
        yield "_Void"
    yield ">"
    yield "> {"

    for mname, mdef in node.fields.items():
        if isinstance(mdef.val, RuntimeValue):
            yield from NodeVisitor().visit_BaseType(mdef.type)
            yield mname
            yield ";"

    # inner = ClassInnerVisitor4(node.inner_scope)
    # for stmt in node.body:
    #     yield from inner.visit(stmt)

    # yield "template <typename... U>"
    # yield "Obj(U&&... args) {"
    # yield "dot(this, __init__)(this, std::forward<U>(args)...);"
    # yield "}"


    yield "};"


    for mname, mdef in node.fields.items():
        if isinstance(mdef.val, ast.FunctionDef):
            gen_p = [TypeVariable(p.name, emit_as_is=True) for p in mdef.type.parameters]
            ty = mdef.type.instantiate(gen_p)
            ScoperExprVisitor(ty.block_data.scope).visit_function_call(ty, [TypeVariable(decltype_str=f"decltype({arg.arg})") for arg in ty.block_data.node.args.args])
            yield from emit_function(mname, ty, "method")

    yield "template <"

    if parameters:
        yield from join(",", (f"typename {p.name}" for p in parameters))
        yield ", typename... $T"
    else:
        yield "typename... $T, typename _Void = void"

    yield ">"
    def obj_params():
        yield from join(",", template_params())
    yield "auto operator() ($T&&... args) const -> typon::Task<decltype(referencemodel::rc(Obj<"
    yield from obj_params()
    yield ">{}))> {"
    yield "auto obj = referencemodel::rc(Obj<"
    yield from obj_params()
    yield ">{});"
    yield "co_await dot(obj, __init__)(std::forward<$T>(args)...);"
    yield "co_return obj;"
    yield "}"

    yield f"}};"
    yield f"static constexpr {name}__oo<> {name} {{}};"
    yield f"static_assert(sizeof {name} == 1);"
