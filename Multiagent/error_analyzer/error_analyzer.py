
important_extensions = ['.py', '.html', '.htm', '.js', '.css', '.json', 
                       '.xml', '.yaml', '.yml', '.md', '.txt', '.csv', 
                        '.ipynb', '.php', '.java', '.cpp', '.c', '.h', 
                        '.rb', '.go', '.rs', '.swift', '.kt', '.sh', 
                        '.bat', '.ps1', '.md', '.rst', '.ini', '.cfg', 
                        '.conf', '.toml', '.sql', '.db', '.sqlite3']

record = []

def find_main_files(state):
    files = state["all_files"]
    for file in files:
        for ext in important_extensions:
            if file.endswith(ext):
                record.append(file)
    
    return record
    









