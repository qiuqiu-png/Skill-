#!/usr/bin/env python3
"""
图片批量处理工具
批量压缩图片到指定大小并转换为 JPG 格式
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image
import io


def compress_image(input_path, output_path, max_size_kb=500, initial_quality=85):
    """
    压缩图片到指定大小并转换为 JPG

    参数:
        input_path: 输入图片路径
        output_path: 输出图片路径
        max_size_kb: 目标文件大小上限（KB）
        initial_quality: 初始 JPEG 质量（1-100）

    返回:
        是否成功
    """
    try:
        # 打开图片
        img = Image.open(input_path)

        # 转换 RGBA 或 LA 模式到 RGB（处理透明背景）
        if img.mode in ('RGBA', 'LA', 'P'):
            # 创建白色背景
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # 目标大小（字节）
        max_size_bytes = max_size_kb * 1024

        # 初始质量
        quality = initial_quality

        # 二分查找最佳质量值
        min_quality = 1
        max_quality = initial_quality
        best_quality = quality

        while min_quality <= max_quality:
            quality = (min_quality + max_quality) // 2

            # 保存到内存缓冲区
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
            size = buffer.tell()

            if size <= max_size_bytes:
                best_quality = quality
                min_quality = quality + 1
            else:
                max_quality = quality - 1

        # 使用最佳质量保存
        img.save(output_path, format='JPEG', quality=best_quality, optimize=True)

        # 获取最终文件大小
        final_size = os.path.getsize(output_path)

        return True, final_size, best_quality

    except Exception as e:
        return False, 0, 0


def process_images(input_files, output_dir='output', max_size_kb=500, initial_quality=85):
    """
    批量处理图片

    参数:
        input_files: 输入文件列表
        output_dir: 输出目录
        max_size_kb: 目标文件大小上限（KB）
        initial_quality: 初始 JPEG 质量
    """
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"输出目录: {output_path.absolute()}")
    print(f"目标大小: {max_size_kb} KB")
    print(f"初始质量: {initial_quality}")
    print("-" * 60)

    success_count = 0
    fail_count = 0
    total_original_size = 0
    total_compressed_size = 0

    for input_file in input_files:
        input_file = Path(input_file)

        if not input_file.exists():
            print(f"✗ 跳过: {input_file} (文件不存在)")
            fail_count += 1
            continue

        # 检查是否为图片文件
        if input_file.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.gif']:
            print(f"⚠ 跳过: {input_file} (不是支持的图片格式)")
            fail_count += 1
            continue

        # 生成输出文件名（保留原文件名，改为 .jpg）
        output_file = output_path / f"{input_file.stem}.jpg"

        # 获取原始文件大小
        original_size = input_file.stat().st_size

        # 处理图片
        print(f"处理: {input_file.name}", end=' ... ')

        success, final_size, quality = compress_image(
            str(input_file),
            str(output_file),
            max_size_kb,
            initial_quality
        )

        if success:
            original_size_kb = original_size / 1024
            final_size_kb = final_size / 1024
            compression_ratio = (1 - final_size / original_size) * 100 if original_size > 0 else 0

            print(f"✓ 完成")
            print(f"  原始: {original_size_kb:.1f} KB → 压缩后: {final_size_kb:.1f} KB")
            print(f"  压缩率: {compression_ratio:.1f}% | 质量: {quality}")

            success_count += 1
            total_original_size += original_size
            total_compressed_size += final_size
        else:
            print(f"✗ 失败")
            fail_count += 1

        print()

    # 统计信息
    print("=" * 60)
    print(f"处理完成！")
    print(f"成功: {success_count} | 失败: {fail_count} | 总计: {len(input_files)}")

    if success_count > 0:
        total_original_mb = total_original_size / (1024 * 1024)
        total_compressed_mb = total_compressed_size / (1024 * 1024)
        total_saved_mb = (total_original_size - total_compressed_size) / (1024 * 1024)
        total_compression_ratio = (1 - total_compressed_size / total_original_size) * 100

        print(f"\n统计:")
        print(f"  原始总大小: {total_original_mb:.2f} MB")
        print(f"  压缩后总大小: {total_compressed_mb:.2f} MB")
        print(f"  节省空间: {total_saved_mb:.2f} MB ({total_compression_ratio:.1f}%)")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='批量压缩图片到指定大小并转换为 JPG 格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 压缩单个图片到 500KB
  %(prog)s image.png

  # 批量处理
  %(prog)s *.png

  # 压缩到 300KB
  %(prog)s *.jpg --max-size 300

  # 自定义输出目录
  %(prog)s images/*.png -o compressed
        """
    )

    parser.add_argument('input', nargs='+', help='输入图片文件（支持通配符）')
    parser.add_argument('-s', '--max-size', type=int, default=500,
                       help='目标文件大小上限（KB），默认: 500')
    parser.add_argument('-o', '--output', default='output',
                       help='输出目录，默认: output')
    parser.add_argument('-q', '--quality', type=int, default=85,
                       help='初始 JPEG 质量（1-100），默认: 85')

    args = parser.parse_args()

    # 验证参数
    if args.max_size <= 0:
        print(f"✗ 错误：目标大小必须大于 0（当前：{args.max_size}）")
        sys.exit(1)

    if not (1 <= args.quality <= 100):
        print(f"✗ 错误：质量必须在 1-100 之间（当前：{args.quality}）")
        sys.exit(1)

    print("=" * 60)
    print("图片批量处理工具")
    print("=" * 60)
    print()

    # 处理通配符
    input_files = []
    for pattern in args.input:
        from glob import glob
        matched = glob(pattern)
        if matched:
            input_files.extend(matched)
        else:
            input_files.append(pattern)

    # 去重
    input_files = list(set(input_files))

    if not input_files:
        print("✗ 错误：未找到输入文件")
        sys.exit(1)

    # 处理图片
    process_images(
        input_files,
        args.output,
        args.max_size,
        args.quality
    )


if __name__ == "__main__":
    main()
