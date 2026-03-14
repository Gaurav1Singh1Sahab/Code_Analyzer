import os


SUPPORTED_EXTENSIONS = [
    ".py",
    ".js",
    ".ts",
    ".java",
    ".go",
    ".cpp",
    ".c",
    ".cs"
]


def scan_code_files(repo_path: str):

    code_files = []

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            for ext in SUPPORTED_EXTENSIONS:

                if file.endswith(ext):
                    code_files.append(
                        os.path.join(root, file)
                    )

    return code_files

def chunk_code(file_path, chunk_size=500):

    chunks = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    for i in range(0, len(content), chunk_size):
        chunks.append(content[i:i+chunk_size])

    return chunks