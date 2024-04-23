import ast
from typing import Iterable

from transpiler.phases.emit_cpp.class_ import emit_class
from transpiler.phases.emit_cpp.expr import ExpressionVisitor
from transpiler.phases.emit_cpp.function import emit_function, BlockVisitor
from transpiler.phases.emit_cpp.visitors import NodeVisitor, CoroutineMode
from transpiler.phases.typing.modules import ModuleType, TyponModuleType, PythonModuleType
from transpiler.phases.typing.types import CallableInstanceType, ClassTypeType, TypeVariable, BaseType, GenericType, \
    GenericInstanceType, UserGenericType, RuntimeValue, BuiltinFeatureType, UserType
from transpiler.utils import linenodata


def emit_module(mod: ModuleType) -> Iterable[str]:
    __TB_NODE__ = mod.block_data.node
    yield "#include <python/builtins.hpp>"
    yield "#include <python/sys.hpp>"
    emitted = set()

    def emit(mod_obj: ModuleType):
        if mod_obj in emitted:
            return
        emitted.add(mod_obj)
        name = mod_obj.name()
        match mod_obj:
            case TyponModuleType():
                yield f"#include <python/{name}.hpp>"
            case PythonModuleType():
                yield f"namespace py_python_{name} {{"

                yield "template <typename _Unused = void>"
                yield f"struct {name}__oo : referencemodel::moduletype<{name}__oo<>> {{"

                for fname, obj in mod_obj.fields.items():
                    obj = obj.type.resolve()
                    if type(obj) is TypeVariable:
                        continue  # unused python function
                    assert isinstance(obj, CallableInstanceType)
                    yield "struct : referencemodel::function {"
                    yield "auto operator()("

                    for i, argty in enumerate(obj.parameters):
                        if i != 0:
                            yield ", "
                        yield "lvalue_or_rvalue<"
                        yield from NodeVisitor().visit_BaseType(argty)
                        yield f"> arg{i}"

                    yield ") const {"

                    yield "InterpGuard guard{};"
                    yield "try {"
                    yield f"return py::module_::import(\"{name}\").attr(\"{fname}\")("
                    for i, argty in enumerate(obj.parameters):
                        if i != 0:
                            yield ", "
                        yield f"*arg{i}"
                    yield ").cast<"
                    yield from NodeVisitor().visit_BaseType(obj.return_type)
                    yield ">();"
                    yield "} catch (py::error_already_set& e) {"
                    yield 'std::cerr << "Python exception: " << e.what() << std::endl;'
                    yield "throw;"
                    yield "}"

                    yield "}"
                    yield f"}} static constexpr {fname} {{}};"

                yield "};"

                yield f"{name}__oo<> all;"
                yield "}"

    incl_vars = []
    for node in mod.block_data.node.body:
        match node:
            case ast.Import(names):
                for alias in names:
                    yield from emit(alias.module_obj)
                    prefix = "python_" if isinstance(alias.module_obj, PythonModuleType) else ""
                    incl_vars.append(f"auto& {alias.asname or alias.name} = py_{prefix}{alias.module_obj.name()}::all;")
            case ast.ImportFrom(module, names, _):
                yield from emit(node.module_obj)
                prefix = "python_" if isinstance(node.module_obj, PythonModuleType) else ""
                for alias in names:
                    # if isinstance(node.module_obj, PythonModuleType):
                    if isinstance(node.module_obj.fields[alias.name].type.resolve(), (TypeVariable, BuiltinFeatureType)):
                        continue # unused function
                    incl_vars.append(f"auto& {alias.asname or alias.name} = py_{prefix}{node.module_obj.name()}::all.{alias.name};")
    yield "namespace PROGRAMNS {"
    yield from incl_vars
    yield "template <typename _Unused = void>"
    yield f"struct {mod.name()}__oo : referencemodel::moduletype<{mod.name()}__oo<>>"
    yield "{"
    init_lines = []
    for name, field in mod.fields.items():
        if not field.in_class_def:
            continue

        ty = field.type

        if isinstance(field.from_node, ast.Assign):
            yield "static inline"
            yield from NodeVisitor().visit_BaseType(field.from_node.value.type)
            yield name
            yield "="
            yield from ExpressionVisitor(mod.block_data.scope, CoroutineMode.SYNC).visit(field.from_node.value)
            yield ";"
            # if not isinstance(field.from_node.value, RuntimeValue):
            #     assign_node = ast.Assign([ast.Name(name)], field.from_node.value, None, **linenodata(field.from_node))
            #     assign_node.is_declare = None
            #     init_lines.append(BlockVisitor(mod.block_data.scope).visit(assign_node))
            continue

        if isinstance(ty, ClassTypeType):
            ty = ty.inner_type

        if isinstance(ty, GenericType):
            gen_p = [TypeVariable(p.name, emit_as_is=True) for p in ty.parameters]
            ty = ty.instantiate(gen_p)
        else:
            gen_p = []

        from transpiler.phases.typing.expr import ScoperExprVisitor
        x = 5
        match ty:
            case CallableInstanceType():
                ty.generic_parent.instance_cache = []
                ScoperExprVisitor(ty.block_data.scope).visit_function_call(
                    ty, [TypeVariable(decltype_str=arg.arg) for arg in ty.block_data.node.args.args])
                yield from emit_function(name, ty, gen_p=gen_p)
            case GenericInstanceType() if isinstance(ty.generic_parent, UserGenericType):
                yield from emit_class(name, ty)
            case UserType():
                yield from emit_class(name, ty)
            case _:
                raise NotImplementedError(f"Unsupported module item type {ty}")

    yield f"{mod.name()}__oo() {{"
    for line in init_lines:
        yield from line
    yield "}"

    yield "};"
    yield f"{mod.name()}__oo<> {mod.name()};"
    yield f"static_assert(sizeof {mod.name()} == 1);"
    yield "}"
