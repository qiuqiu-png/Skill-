#!/usr/bin/env python3
"""
视频黑边裁剪工具
自动检测并裁剪视频中的黑边区域
"""

import subprocess
import re
import os
import sys
import argparse
from pathlib import Path


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


def detect_crop(video_path, sample_duration=30):
    """
    检测视频黑边并返回裁剪参数

    参数:
        video_path: 视频文件路径
        sample_duration: 采样时长（秒），默认30秒

    返回:
        裁剪参数字符串，如 "1920:800:0:140" (width:height:x:y)
    """
    print(f"正在分析视频: {video_path}")
    print(f"采样前 {sample_duration} 秒进行黑边检测...")

    # 使用 FFmpeg 的 cropdetect 滤镜检测黑边
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-t', str(sample_duration),  # 只分析前N秒
        '-vf', 'cropdetect=24:16:0',  # cropdetect滤镜：阈值24，圆整16像素，跳过0帧
        '-f', 'null',
        '-'
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )

        # 从 stderr 中提取 crop 参数（FFmpeg 输出到 stderr）
        output = result.stderr

        # 查找所有 crop 参数
        crop_matches = re.findall(r'crop=(\d+:\d+:\d+:\d+)', output)

        if not crop_matches:
            print("⚠ 未检测到黑边，视频可能已经是完整画面")
            return None

        # 使用最后一个检测结果（通常最稳定）
        crop_params = crop_matches[-1]

        # 解析裁剪参数
        w, h, x, y = map(int, crop_params.split(':'))

        print(f"✓ 检测到黑边")
        print(f"  裁剪参数: {crop_params}")
        print(f"  输出尺寸: {w}x{h}")
        print(f"  偏移位置: x={x}, y={y}")

        return crop_params

    except Exception as e:
        print(f"✗ 检测失败: {e}")
        return None


def crop_video(input_path, output_path, crop_params):
    """
    裁剪视频

    参数:
        input_path: 输入视频路径
        output_path: 输出视频路径
        crop_params: 裁剪参数，格式 "width:height:x:y"
    """
    print(f"\n开始裁剪视频...")
    print(f"输入: {input_path}")
    print(f"输出: {output_path}")

    # 构建 FFmpeg 命令
    # -c:v copy 会尝试直接复制视频流（最快），如果不支持则会自动重编码
    # -c:a copy 直接复制音频流（无损）
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-vf', f'crop={crop_params}',
        '-c:a', 'copy',  # 音频直接复制
        '-y',  # 覆盖输出文件
        output_path
    ]

    try:
        # 显示进度
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        # 实时显示处理进度
        for line in process.stdout:
            # 提取时间进度信息
            if 'time=' in line:
                time_match = re.search(r'time=(\S+)', line)
                if time_match:
                    print(f"\r处理进度: {time_match.group(1)}", end='', flush=True)

        process.wait()

        if process.returncode == 0:
            print(f"\n✓ 裁剪完成: {output_path}")

            # 显示文件大小
            input_size = os.path.getsize(input_path) / (1024 * 1024)
            output_size = os.path.getsize(output_path) / (1024 * 1024)
            print(f"  原文件大小: {input_size:.2f} MB")
            print(f"  新文件大小: {output_size:.2f} MB")
            return True
        else:
            print(f"\n✗ 裁剪失败")
            return False

    except Exception as e:
        print(f"\n✗ 裁剪失败: {e}")
        return False


def process_video(input_path, output_path=None, sample_duration=30):
    """
    处理单个视频文件

    参数:
        input_path: 输入视频路径
        output_path: 输出视频路径（可选）
        sample_duration: 黑边检测采样时长
    """
    input_path = Path(input_path)

    if not input_path.exists():
        print(f"✗ 错误：文件不存在 {input_path}")
        return False

    # 自动生成输出路径
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_cropped{input_path.suffix}"
    else:
        output_path = Path(output_path)
        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)

    # 检测黑边
    crop_params = detect_crop(str(input_path), sample_duration)

    if crop_params is None:
        print("跳过此文件（无需裁剪）\n")
        return False

    # 裁剪视频
    success = crop_video(str(input_path), str(output_path), crop_params)
    print()

    return success


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='自动检测并裁剪视频黑边',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 单个视频
  %(prog)s video.mp4

  # 批量处理
  %(prog)s videos/*.mp4

  # 指定输出路径
  %(prog)s input.mp4 -o output/cropped.mp4

  # 自定义采样时长
  %(prog)s video.mp4 --sample 60
        """
    )

    parser.add_argument('input', nargs='+', help='输入视频文件（支持通配符）')
    parser.add_argument('-o', '--output', help='输出文件路径（仅单文件时有效）')
    parser.add_argument('-s', '--sample', type=int, default=30,
                       help='黑边检测采样时长（秒），默认30秒')

    args = parser.parse_args()

    # 检查 FFmpeg
    if not check_ffmpeg():
        sys.exit(1)

    print("=" * 60)
    print("视频黑边裁剪工具")
    print("=" * 60)
    print()

    # 处理输入文件
    input_files = []
    for pattern in args.input:
        # 支持通配符扩展
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

    # 批量处理模式
    if len(input_files) > 1:
        if args.output:
            print("⚠ 警告：批量处理时忽略 --output 参数")

        print(f"找到 {len(input_files)} 个文件，开始批量处理...\n")

        success_count = 0
        for i, video_file in enumerate(input_files, 1):
            print(f"[{i}/{len(input_files)}] 处理: {video_file}")
            if process_video(video_file, sample_duration=args.sample):
                success_count += 1
            print("-" * 60)

        print(f"\n处理完成！成功: {success_count}/{len(input_files)}")

    # 单文件处理模式
    else:
        process_video(input_files[0], args.output, args.sample)


if __name__ == "__main__":
    main()
