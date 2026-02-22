#!/usr/bin/env python3
"""
视频随机拼接工具
将视频按指定时长分段，随机打乱顺序后拼接
"""

import subprocess
import os
import sys
import argparse
import re
import random
import tempfile
import shutil
from pathlib import Path
from typing import List, Tuple


def check_ffmpeg():
    """检查 FFmpeg 是否已安装"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ 错误：未找到 FFmpeg")
        print("请先安装 FFmpeg：")
        print("  macOS: brew install ffmpeg")
        print("  Ubuntu: sudo apt install ffmpeg")
        print("  Windows: 从 https://ffmpeg.org/download.html 下载")
        return False


def get_video_duration(video_path):
    """
    获取视频时长（秒）

    参数:
        video_path: 视频文件路径

    返回:
        视频时长（秒），失败返回 None
    """
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'csv=p=0',
        video_path
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        return duration
    except Exception as e:
        print(f"✗ 无法获取视频时长: {e}")
        return None


def split_video(input_path, segment_duration, temp_dir):
    """
    将视频按指定时长分段

    参数:
        input_path: 输入视频路径
        segment_duration: 每段时长（秒）
        temp_dir: 临时目录

    返回:
        分段文件路径列表
    """
    print(f"正在将视频分段（每段 {segment_duration} 秒）...")
    
    duration = get_video_duration(input_path)
    if duration is None:
        return []

    # 计算分段数量
    num_segments = int(duration / segment_duration)
    if num_segments == 0:
        print("⚠ 警告：视频时长小于分段时长，将使用完整视频")
        num_segments = 1

    print(f"视频总时长: {duration:.2f} 秒")
    print(f"将分为 {num_segments} 段")

    segments = []
    input_stem = Path(input_path).stem

    for i in range(num_segments):
        start_time = i * segment_duration
        segment_path = temp_dir / f"{input_stem}_segment_{i:04d}.mp4"

        # 使用 FFmpeg 提取片段
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-ss', str(start_time),
            '-t', str(segment_duration),
            '-c', 'copy',  # 直接复制流，不重新编码（快速）
            '-avoid_negative_ts', 'make_zero',
            '-y',
            str(segment_path)
        ]

        try:
            subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            segments.append(segment_path)
            print(f"  ✓ 分段 {i+1}/{num_segments}: {segment_path.name}")
        except subprocess.CalledProcessError as e:
            print(f"  ✗ 分段 {i+1} 失败: {e}")
            continue

    return segments


def create_concat_file(segments, concat_file_path):
    """
    创建 FFmpeg concat 文件

    参数:
        segments: 分段文件路径列表
        concat_file_path: concat 文件路径
    """
    with open(concat_file_path, 'w', encoding='utf-8') as f:
        for segment in segments:
            # 使用绝对路径，避免路径问题
            abs_path = os.path.abspath(segment)
            # 转义特殊字符
            abs_path = abs_path.replace("'", "'\\''")
            f.write(f"file '{abs_path}'\n")


def concatenate_videos(segments, output_path, temp_dir):
    """
    拼接视频片段

    参数:
        segments: 分段文件路径列表（已打乱顺序）
        output_path: 输出文件路径
        temp_dir: 临时目录
    """
    if not segments:
        print("✗ 错误：没有可拼接的视频片段")
        return False

    print(f"\n正在拼接 {len(segments)} 个片段...")

    # 创建 concat 文件
    concat_file = temp_dir / "concat_list.txt"
    create_concat_file(segments, concat_file)

    # 使用 FFmpeg concat demuxer 拼接
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(concat_file),
        '-c', 'copy',  # 直接复制流，不重新编码（快速）
        '-y',
        str(output_path)
    ]

    try:
        print("处理中...", flush=True)
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        # 显示进度
        for line in process.stdout:
            if 'time=' in line:
                time_match = re.search(r'time=(\S+)', line)
                if time_match:
                    print(f"\r处理进度: {time_match.group(1)}", end='', flush=True)

        process.wait()

        if process.returncode == 0:
            print(f"\n✓ 拼接完成: {output_path}")
            
            # 显示文件大小
            output_size = os.path.getsize(output_path) / (1024 * 1024)
            print(f"  输出文件大小: {output_size:.2f} MB")
            return True
        else:
            print(f"\n✗ 拼接失败")
            return False

    except Exception as e:
        print(f"\n✗ 拼接失败: {e}")
        return False


def cleanup_temp_files(temp_dir):
    """
    清理临时文件

    参数:
        temp_dir: 临时目录路径
    """
    try:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            print(f"✓ 已清理临时文件: {temp_dir}")
    except Exception as e:
        print(f"⚠ 警告：清理临时文件失败: {e}")


def process_video(input_path, output_path, segment_duration, shuffle=True, cleanup=True):
    """
    处理视频：分段、打乱、拼接

    参数:
        input_path: 输入视频路径
        output_path: 输出视频路径
        segment_duration: 每段时长（秒）
        shuffle: 是否随机打乱顺序
        cleanup: 是否清理临时文件
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        print(f"✗ 错误：文件不存在 {input_path}")
        return False

    # 创建临时目录
    temp_dir = Path(tempfile.mkdtemp(prefix="video_random_concatenate_"))
    print(f"临时目录: {temp_dir}")

    try:
        # 1. 分段
        segments = split_video(str(input_path), segment_duration, temp_dir)
        
        if not segments:
            print("✗ 错误：无法创建视频分段")
            return False

        # 2. 随机打乱顺序
        if shuffle:
            print(f"\n正在随机打乱 {len(segments)} 个片段...")
            random.shuffle(segments)
            print("✓ 顺序已打乱")
        else:
            print("\n保持原始顺序")

        # 显示打乱后的顺序
        print("\n片段顺序:")
        for i, seg in enumerate(segments, 1):
            # 从文件名提取原始序号
            match = re.search(r'segment_(\d+)', seg.name)
            original_idx = match.group(1) if match else "?"
            print(f"  {i}. 原片段 {original_idx}: {seg.name}")

        # 3. 拼接
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        success = concatenate_videos(segments, output_path, temp_dir)

        return success

    finally:
        # 4. 清理临时文件
        if cleanup:
            cleanup_temp_files(temp_dir)
        else:
            print(f"\n⚠ 临时文件保留在: {temp_dir}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='视频随机拼接工具：将视频分段后随机打乱顺序拼接',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法：每段5秒，随机打乱
  %(prog)s video.mp4 -d 5

  # 指定输出文件
  %(prog)s video.mp4 -o output.mp4 -d 3

  # 不打乱顺序（按原顺序拼接）
  %(prog)s video.mp4 -d 5 --no-shuffle

  # 保留临时文件（用于调试）
  %(prog)s video.mp4 -d 5 --no-cleanup

  # 批量处理
  %(prog)s videos/*.mp4 -d 5
        """
    )

    parser.add_argument('input', nargs='+', help='输入视频文件（支持通配符）')
    parser.add_argument('-o', '--output', help='输出文件路径（仅单文件时有效）')
    parser.add_argument('-d', '--duration', type=float, required=True,
                       help='每段时长（秒）')
    parser.add_argument('--no-shuffle', action='store_true',
                       help='不打乱顺序，保持原顺序拼接')
    parser.add_argument('--no-cleanup', action='store_true',
                       help='不清理临时文件（用于调试）')
    parser.add_argument('--seed', type=int, default=None,
                       help='随机种子（用于可重复的随机结果）')

    args = parser.parse_args()

    # 检查 FFmpeg
    if not check_ffmpeg():
        sys.exit(1)

    # 设置随机种子
    if args.seed is not None:
        random.seed(args.seed)
        print(f"使用随机种子: {args.seed}")

    print("=" * 60)
    print("视频随机拼接工具")
    print("=" * 60)
    print()

    # 验证分段时长
    if args.duration <= 0:
        print(f"✗ 错误：分段时长必须大于 0（当前：{args.duration}）")
        sys.exit(1)

    # 处理输入文件
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

    shuffle = not args.no_shuffle
    cleanup = not args.no_cleanup

    # 批量处理模式
    if len(input_files) > 1:
        if args.output:
            print("⚠ 警告：批量处理时忽略 --output 参数")

        print(f"找到 {len(input_files)} 个文件，开始批量处理...\n")

        success_count = 0
        for i, video_file in enumerate(input_files, 1):
            print(f"[{i}/{len(input_files)}] 处理: {video_file}")
            
            # 自动生成输出路径
            input_path = Path(video_file)
            output_path = input_path.parent / f"{input_path.stem}_random{input_path.suffix}"
            
            if process_video(
                video_file,
                output_path,
                args.duration,
                shuffle,
                cleanup
            ):
                success_count += 1
            
            print("-" * 60)

        print(f"\n处理完成！成功: {success_count}/{len(input_files)}")

    # 单文件处理模式
    else:
        input_file = input_files[0]
        
        # 自动生成输出路径
        if args.output is None:
            input_path = Path(input_file)
            output_path = input_path.parent / f"{input_path.stem}_random{input_path.suffix}"
        else:
            output_path = args.output

        success = process_video(
            input_file,
            output_path,
            args.duration,
            shuffle,
            cleanup
        )

        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()


