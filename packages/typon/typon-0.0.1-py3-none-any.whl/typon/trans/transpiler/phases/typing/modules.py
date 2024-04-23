import ast
import importlib
from pathlib import Path
from logging import debug

from transpiler.phases.typing import PRELUDE
from transpiler.phases.typing.scope import Scope, VarKind, VarDecl, ScopeKind
from transpiler.phases.typing.types import MemberDef, ResolvedConcreteType, UniqueTypeMixin, BlockData, TypeVariable


class ModuleType(UniqueTypeMixin, ResolvedConcreteType):
    pass

class TyponModuleType(ModuleType):
    pass

class PythonModuleType(ModuleType):
    pass

def make_module(name: str, scope: Scope) -> TyponModuleType:
    class CreatedType(TyponModuleType):
        def name(self):
            return name
    ty = CreatedType()
    for n, v in scope.vars.items():
        ty.fields[n] = MemberDef(v.type, v.val, v.is_item_decl, v.from_node)
    return ty

visited_modules = {}

def parse_module(mod_name: str, python_path: list[Path], scope=None, preprocess=None) -> ModuleType:
    for path in python_path:
        path = path / mod_name

        if not path.exists():
            path = path.with_suffix(".py")

        if not path.exists():
            path = path.with_stem(mod_name + "_")

        if not path.exists():
            continue

        break
    else:
        """
        
          py_mod = importlib.import_module(name)
          mod_scope = Scope()
          # copy all functions to mod_scope
          for fname, obj in py_mod.__dict__.items():
              if callable(obj):
                  # fty = FunctionType([], TypeVariable())
                  # fty.is_python_func = True
                  fty = TypeVariable()
                  fty.is_python_func = True
                  mod_scope.vars[fname] = VarDecl(VarKind.LOCAL, fty)
          mod = make_mod_decl(name, mod_scope)
          mod.type.is_python = True
          self.scope.vars[name] = mod
        
        
        
        """
        if mod_name.startswith("python."):
            mod_name = mod_name[len("python."):]
        try:
            py_mod = importlib.import_module(mod_name)
        except ModuleNotFoundError:
            raise FileNotFoundError(f"Could not find {mod_name}")
        else:
            if mod := visited_modules.get(py_mod):
                return mod.type
            try:
                class OurModule(PythonModuleType):
                    def name(self):
                        return mod_name
                mod = OurModule()
                # copy all functions to mod_scope
                for fname, obj in py_mod.__dict__.items():
                    if callable(obj):
                        # fty = FunctionType([], TypeVariable())
                        # fty.is_python_func = True
                        fty = TypeVariable(python_func_placeholder = True)
                        #fty.is_python_func = True
                        mod.fields[fname] = MemberDef(fty)
                visited_modules[py_mod] = VarDecl(VarKind.LOCAL, mod)
                return mod
            except:
                raise NotImplementedError(f"Could not process python module {mod_name}")

    if path.is_dir():
        path = path / "__init__.py"

    if mod := visited_modules.get(path.as_posix()):
        return mod.type

    mod_scope = scope or PRELUDE.child(ScopeKind.GLOBAL)

    if path.suffix != ".py":
        raise NotImplementedError(f"Unsupported file type {path.suffix}")

    from transpiler.phases.typing.stdlib import StdlibVisitor
    node = ast.parse(path.read_text())
    if preprocess:
        node = preprocess(node)
    from transpiler.transpiler import TYPON_STD
    StdlibVisitor(python_path, mod_scope, is_native=TYPON_STD in path.parents).visit(node)

    mod = make_module(mod_name, mod_scope)
    mod.block_data = BlockData(node, mod_scope)
    visited_modules[path.as_posix()] = VarDecl(VarKind.LOCAL, mod)
    return mod

# def process_module(mod_path: Path, scope):
#     if mod := visited_modules.get(mod_path.as_posix()):
#         return mod
#
#     if mod_path.is_dir():
#         mod_scope = scope.child(ScopeKind.GLOBAL)
#         discover_module(mod_path, mod_scope)
#         mod = make_mod_decl(mod_path.name, mod_scope)
#         scope.vars[mod_path.name] = mod
#     elif mod_path.name == "__init__.py":
#         StdlibVisitor(mod_path, scope).visit(ast.parse(mod_path.read_text()))
#         mod = None
#         debug(f"Visited {mod_path}")
#     elif mod_path.suffix == ".py":
#         mod_scope = scope.child(ScopeKind.GLOBAL)
#         StdlibVisitor(mod_path, mod_scope).visit(ast.parse(mod_path.read_text()))
#         if mod_path.stem[-1] == "_":
#             mod_path = mod_path.with_name(mod_path.stem[:-1])
#         mod = make_mod_decl(mod_path.name, mod_scope)
#         scope.vars[mod_path.stem] = mod
#         debug(f"Visited {mod_path}")
#     return mod
#
# def discover_module(dir_path: Path, scope):
#     mod = make_mod_decl(dir_path.name, scope)
#     for child in sorted(dir_path.iterdir()):
#         # if child.name == "__init__.py":
#         #     StdlibVisitor(mod_scope).visit(ast.parse(child.read_text()))
#         # else:
#         #     process_module(child, mod_scope)
#         child_mod = process_module(child, scope)
#         visited_modules[child.as_posix()] = child_mod
#     return mod
