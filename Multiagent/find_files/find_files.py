import subprocess
import os

def find_python_files():
    python_files = []
    # Directories to skip
    exclude_dirs = {'venv', 'env', '.venv', 'virtualenv', '__pycache__', 
                    'node_modules', '.git', '.idea', 'dist', 'build'}
    
    for root, dirs, files in os.walk('.'):
        # Get the relative path
        rel_path = os.path.relpath(root, '.')
        
        # Skip if current directory is in exclude list
        # Check if any part of the path contains excluded dir
        path_parts = rel_path.split(os.sep)
        if any(part in exclude_dirs for part in path_parts):
            continue
        
        # Modify dirs in-place to prevent walking into excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        # A more comprehensive list for general development projects
        extensions = (
            '.py', '.java', '.js', '.ts', '.html', '.css',  # Code
            '.json', '.yaml', '.yml', '.toml', '.xml',   
        )

        # Add Python files
        for file in files:
            if file.endswith(extensions):
                full_path = os.path.join(rel_path, file)
                if full_path.startswith('./'):
                    full_path = full_path[2:]
                elif full_path == '.':
                    full_path = file
                python_files.append(full_path)
    
    return sorted(python_files)

def run_selected_script():
    py_files = find_python_files()
    
    if not py_files:
        print("No Python files found (excluding virtual environments)")
        return
    
    for i, file in enumerate(py_files):
        print(f"{file}")
    

if __name__ == "__main__":
    run_selected_script()