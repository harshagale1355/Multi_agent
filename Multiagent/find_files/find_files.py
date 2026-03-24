import os


def find_all_files():
    all_files = []

    exclude_dirs = {
        'venv', 'env', '.venv', 'virtualenv', '__pycache__',
        'node_modules', '.git', '.idea', 'dist', 'build'
    }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    multi_agent_dir = os.path.dirname(os.path.dirname(script_dir))

    for root, dirs, files in os.walk(multi_agent_dir):

        path_parts = root.split(os.sep)

        if any(part in exclude_dirs for part in path_parts):
            continue

        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:

            full_path = os.path.join(root, file)

            rel_path = os.path.relpath(full_path, multi_agent_dir)

            rel_path = rel_path.replace('\\', '/')

            if rel_path:
                all_files.append(rel_path)

    return sorted(all_files)


def workspace_scanner_agent(state):
    """
    Agent that scans the workspace and returns all files
    """

    files = find_all_files()

    return {
        "all_files": files
    }

import re

all_files = find_all_files()


def refers_to_same_file(text1, text2):
    """
    Check if two strings refer to the same Python file,
    ignoring paths and line numbers.
    """
    # Extract just the filename from each (remove path and line number)
    file1 = text1.split('/')[-1].split(':')[0]
    file2 = text2.split('/')[-1].split(':')[0]
    
    return file1 == file2



