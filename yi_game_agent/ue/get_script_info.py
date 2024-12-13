import os
import json
from yi_game_agent.constants import _DEFAULT_UE_DOCS

# 配置项目路径和输出路径（请根据实际项目路径调整）
PROJECT_ROOT = "F:\Epic\Projects\LyraStarterGame"  # UE5工程根目录
OUTPUT_JSONL_PATH = os.path.join(_DEFAULT_UE_DOCS, "code_index.jsonl")

# 确保输出目录存在
os.makedirs(os.path.dirname(OUTPUT_JSONL_PATH), exist_ok=True)

# 要扫描的目录列表（请根据实际项目路径进行调整）
TARGET_DIRS = [
    os.path.join(PROJECT_ROOT, "Source"),
    os.path.join(PROJECT_ROOT, "Plugins")
]

CODE_EXTENSIONS = [".h", ".hpp", ".cpp", ".cc", ".cxx"]
MAX_FILES = 10


def is_code_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename)
    return ext.lower() in CODE_EXTENSIONS


def extract_code_metadata(file_path: str):
    relative_path = os.path.relpath(file_path, os.path.dirname(PROJECT_ROOT))
    file_name = os.path.basename(file_path)
    _, ext = os.path.splitext(file_name)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    code_record = {
        "file_path": relative_path,
        "file_name": file_name,
        "file_type": ext,
        "content": content,
        "annotations": {
            "module_relation": [],
            "class_definitions": [],
            "function_definitions": [],
        },
    }

    return code_record


def main():
    results = []
    processed_count = 0

    for target_dir in TARGET_DIRS:
        if not os.path.exists(target_dir):
            print(f"路径不存在: {target_dir}")
            continue

        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if is_code_file(file):
                    file_path = os.path.join(root, file)
                    code_record = extract_code_metadata(file_path)
                    results.append(code_record)
                    processed_count += 1

                    if processed_count >= MAX_FILES:
                        break
            if processed_count >= MAX_FILES:
                break
        if processed_count >= MAX_FILES:
            break

    with open(OUTPUT_JSONL_PATH, "w", encoding="utf-8") as f:
        for record in results:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(
        f"已构建代码知识库测试数据: {OUTPUT_JSONL_PATH}, 总计 {len(results)} 条记录。"
    )


if __name__ == "__main__":
    main()
