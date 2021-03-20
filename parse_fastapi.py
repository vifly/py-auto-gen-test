import ast
from typing import Optional, NamedTuple


class FuncNameArgsKeywordsTuple(NamedTuple):
    name: str
    args: list[str]
    keywords: list[str]


class FuncInfoTuple(NamedTuple):
    name: str
    path: str
    method: str
    arg_num: int
    arg_names: list[str]
    arg_types: list[str]


def get_ast_root(file_path: str) -> ast.Module:
    with open(file_path, "r") as f:
        content = f.read()

    return ast.parse(content)


def find_async_func_def(ast_root: ast.Module) -> list["ast.Module"]:
    return [i for i in ast_root.body if isinstance(i, ast.AsyncFunctionDef)]


def find_func_def(ast_root: ast.Module) -> list["ast.Module"]:
    return [i for i in ast_root.body if isinstance(i, ast.FunctionDef)]


def get_decorator_name_args_keywords(
    decorator_list: list,
) -> list["FuncNameArgsKeywordsTuple"]:
    result = []

    for decorator in decorator_list:
        args = []
        for arg in decorator.args:
            val = arg.value
            if val:
                args.append(val)
        keywords = {}
        # for example, decorator is @app.get(path="/"), so arg is path, val is /
        for keyword in decorator.keywords:
            arg = keyword.arg
            val = keyword.value.value
            if val:
                keywords[arg] = val

        func_name = decorator.func.attr
        if func_name:
            result.append(FuncNameArgsKeywordsTuple(func_name, args, keywords))

    return result


def get_info_from_any_func_def(
    func_def: ast.Module,
) -> Optional["FuncInfoTuple"]:
    decorator_list = func_def.decorator_list
    func_name = func_def.name
    decorator_name_args_keywords_list = get_decorator_name_args_keywords(
        decorator_list
    )
    if decorator_name_args_keywords_list == []:
        return None
    for decorator_name_args_keywords in decorator_name_args_keywords_list:
        if len(decorator_name_args_keywords.args) == 1:
            arg = decorator_name_args_keywords.args[0]
        else:
            arg = decorator_name_args_keywords.keywords.get("path")

        arg_names = [i.arg for i in func_def.args.args]
        arg_types = [
            i.annotation.id for i in func_def.args.args if i.annotation
        ]
        info = FuncInfoTuple(
            func_name,
            arg,
            decorator_name_args_keywords.name,
            len(func_def.args.args),
            arg_names,
            arg_types,
        )

    return info


def get_info_list(
    file_path: str,
) -> list["FuncInfoTuple"]:
    ast_root = get_ast_root(file_path)
    func_def_list = find_async_func_def(ast_root) + find_func_def(ast_root)
    info_list = []
    for func_def in func_def_list:
        try:
            info = get_info_from_any_func_def(func_def)
            if info:
                if info.method in ["get", "post", "delete", "put", "head"]:
                    info_list.append(info)
        except Exception as e:
            print(e)

    return info_list


if __name__ == "__main__":
    info_list = get_info_list("./main.py")
    print(info_list)
