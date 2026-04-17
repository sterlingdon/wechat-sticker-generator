#!/usr/bin/env python3
"""
Skill Packager for qclaw
打包当前 skill 目录，排除不必要的文件，生成上架用的 zip 文件
"""

import os
import zipfile
from pathlib import Path

EXCLUDE_DIRS = {
    "__pycache__",
    ".ruff_cache",
    ".claude",
    "tmp",
    "output",
    ".git",
    "node_modules",
}

EXCLUDE_FILES = {
    ".gitignore",
    ".DS_Store",
    "CACHEDIR.TAG",
    "package-lock.json",
    "pack_skill.py",
}

EXCLUDE_EXTENSIONS = {
    ".pyc",
}


def should_exclude(path: Path, skill_dir: Path) -> bool:
    """判断是否应该排除该文件/目录"""
    rel_path = path.relative_to(skill_dir)

    for part in rel_path.parts:
        if part in EXCLUDE_DIRS:
            return True

    if path.name in EXCLUDE_FILES:
        return True

    if path.suffix in EXCLUDE_EXTENSIONS:
        return True

    return False


def pack_skill(skill_dir: Path, output_dir: Path) -> str:
    """打包 skill 目录"""
    skill_name = skill_dir.name
    zip_path = output_dir / f"{skill_name}.zip"

    print(f"\n📦 打包 {skill_name}...")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_dir):
            root_path = Path(root)

            dirs[:] = [d for d in dirs if not should_exclude(root_path / d, skill_dir)]

            for file in files:
                file_path = root_path / file
                if not should_exclude(file_path, skill_dir):
                    rel_path = file_path.relative_to(skill_dir)
                    zf.write(file_path, rel_path)
                    print(f"  ✓ {rel_path}")

    zip_size_kb = zip_path.stat().st_size / 1024
    print(f"  ✅ 完成: {zip_path} ({zip_size_kb:.1f} KB)")
    return str(zip_path)


def main():
    """主函数"""
    script_dir = Path(__file__).parent.absolute()
    output_dir = script_dir / "output"

    output_dir.mkdir(exist_ok=True)

    old_zips = list(output_dir.glob("*.zip"))
    if old_zips:
        print(f"🧹 清理旧 zip 文件...")
        for old_zip in old_zips:
            old_zip.unlink()
            print(f"  ✓ 删除 {old_zip.name}")

    print(f"\n📁 Skill 目录: {script_dir}")
    print(f"📁 输出目录: {output_dir}")

    zip_path = pack_skill(script_dir, output_dir)

    print(f"\n{'=' * 50}")
    print(f"✨ 打包完成！")
    print(f"输出位置: {zip_path}")
    size_kb = Path(zip_path).stat().st_size / 1024
    print(f"文件大小: {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
