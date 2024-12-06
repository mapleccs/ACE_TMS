import os


def generate_project_tree(startpath, indent='', ignore_dirs=None, ignore_exts=None):
    """
    生成项目树结构，同时可以忽略隐藏文件、特定文件夹以及特定后缀名的文件。

    :param startpath: 项目根路径
    :param indent: 当前缩进
    :param ignore_dirs: 忽略的文件夹列表
    :param ignore_exts: 忽略的文件扩展名列表
    """
    if ignore_dirs is None:
        ignore_dirs = []
    if ignore_exts is None:
        ignore_exts = []

    items = [item for item in os.listdir(startpath) if not item.startswith('.')]  # 过滤隐藏文件
    for i, item in enumerate(items):
        path = os.path.join(startpath, item)
        if os.path.isdir(path):
            if item in ignore_dirs:  # 如果该文件夹在忽略列表中，跳过
                continue
            print(f"{indent}├── {item}/")
            generate_project_tree(path, indent + "│   ", ignore_dirs, ignore_exts)  # 递归处理子文件夹
        else:
            # 检查文件扩展名，忽略指定的文件类型
            if any([item.endswith(ext) for ext in ignore_exts]):
                continue
            is_last_item = (i == len(items) - 1)
            connector = "└──" if is_last_item else "├──"
            print(f"{indent}{connector} {item}")


# 使用你项目的路径
project_path = ".."
# ignore_folders = ['lab_env', '__pycache__']  # 忽略的文件夹，比如 'data'
# ignore_extensions = ['.pyc']  # 忽略的文件后缀，比如 '.pyc'
ignore_folders = []  # 忽略的文件夹，比如 'data'
ignore_extensions = []  # 忽略的文件后缀，比如 '.pyc'
generate_project_tree(project_path, ignore_dirs=ignore_folders, ignore_exts=ignore_extensions)
