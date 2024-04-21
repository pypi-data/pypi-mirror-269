# main.py
import os
import subprocess
from pathlib import Path
import argparse


def git_pull_in_directories(base_dir):
    # 获取当前目录下的所有一级子目录
    directories = [d for d in Path(base_dir).iterdir() if d.is_dir()]
    for dir in directories:
        # 构建完整的目录路径
        dir_path = os.path.join(base_dir, dir.name)
        try:
            os.chdir(dir_path)
            if Path(".git").exists():
                print(f"Pulling in {dir.name}...")
                result = subprocess.run(["git", "pull"], capture_output=True, text=True)
                if result.returncode == 0:
                    print(result.stdout)
                else:
                    print(f"Failed to pull in {dir.name}. Error: {result.stderr}")
            else:
                print(f"{dir.name} is not a git repository.")
        except Exception as e:
            print(f"Error processing {dir.name}: {e}")
        finally:
            os.chdir(base_dir)
    print("Finished processing all directories.")


def main():
    parser = argparse.ArgumentParser(
        description="Automatically pull git repositories in specified directory."
    )
    parser.add_argument(
        "-b",
        "--base_dir",
        type=str,
        default=".",
        help="The directory where batch execution of `git pull` is expected.",
    )
    args = parser.parse_args()

    current_dir = Path.cwd()
    git_pull_in_directories(os.path.join(current_dir, args.base_dir))


if __name__ == "__main__":
    main()
