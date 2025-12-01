#!/usr/bin/env python3
"""
表格复制行数工具
批量复制Excel文件中的指定行数据
"""

import pandas as pd
import os
import sys


def copy_excel_rows(input_file, output_file, columns="A:A", num_rows=22, repeat_times=128):
    """
    复制Excel文件中的指定行数据

    参数:
        input_file: 输入文件路径
        output_file: 输出文件路径
        columns: 要读取的列，默认"A:A"
        num_rows: 要读取的行数，默认22
        repeat_times: 每行复制次数，默认128
    """
    try:
        # 获取输出目录
        output_dir = os.path.dirname(output_file)

        # 创建输出目录（如果不存在）
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"已创建输出目录: {output_dir}")

        # 读取指定列和行数的数据
        print(f"正在读取文件: {input_file}")
        print(f"读取列: {columns}, 读取行数: {num_rows}")

        data = pd.read_excel(input_file, header=None, usecols=columns, nrows=num_rows)

        # 每行复制指定次数
        print(f"每行复制 {repeat_times} 次...")
        repeated_data = []
        for row in data.values:
            repeated_data.extend([row] * repeat_times)

        # 创建新的DataFrame并保存
        output_df = pd.DataFrame(repeated_data)
        output_df.to_excel(output_file, index=False, header=False)

        print(f"✓ 数据已成功复制并保存到: {output_file}")
        print(f"原始行数: {len(data)}, 输出行数: {len(output_df)}")
        return True

    except FileNotFoundError:
        print(f"✗ 错误：文件 {input_file} 未找到，请检查路径是否正确。")
        return False
    except Exception as e:
        print(f"✗ 发生错误：{e}")
        return False


def main():
    """主函数：交互式输入参数"""
    print("=" * 50)
    print("表格复制行数工具")
    print("=" * 50)

    # 获取输入参数
    if len(sys.argv) > 1:
        # 命令行参数模式
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        columns = sys.argv[3] if len(sys.argv) > 3 else "A:A"
        num_rows = int(sys.argv[4]) if len(sys.argv) > 4 else 22
        repeat_times = int(sys.argv[5]) if len(sys.argv) > 5 else 128
    else:
        # 交互式输入模式
        input_file = input("请输入源文件路径: ").strip()
        output_file = input("请输入输出文件路径（留空则在同目录生成）: ").strip()

        if not output_file:
            base_dir = os.path.dirname(input_file)
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_file = os.path.join(base_dir, f"{base_name}_复制.xlsx")

        columns = input("请输入要读取的列（默认A:A）: ").strip() or "A:A"
        num_rows_input = input("请输入要读取的行数（默认22）: ").strip()
        num_rows = int(num_rows_input) if num_rows_input else 22

        repeat_times_input = input("请输入每行复制次数（默认128）: ").strip()
        repeat_times = int(repeat_times_input) if repeat_times_input else 128

    print("\n处理参数:")
    print(f"  源文件: {input_file}")
    print(f"  输出文件: {output_file}")
    print(f"  读取列: {columns}")
    print(f"  读取行数: {num_rows}")
    print(f"  复制次数: {repeat_times}")
    print()

    # 执行复制
    success = copy_excel_rows(input_file, output_file, columns, num_rows, repeat_times)

    if success:
        print("\n处理完成！")
    else:
        print("\n处理失败，请检查错误信息。")
        sys.exit(1)


if __name__ == "__main__":
    main()
