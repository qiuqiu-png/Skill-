#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加盟入库单过滤与核算工具

功能：
1. 过滤指定门店和时间范围的数据
2. 过滤JMCX开头的单据
3. 仅保留指定品类（足金、足金（新）、爱尚金）
4. 判断按件/按克
5. 核算挂签费

作者：Claude
创建日期：2025-12-24
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional


def filter_and_calculate(
    input_file: str,
    output_file: Optional[str] = None
) -> str:
    """
    过滤加盟入库单数据并进行核算

    参数：
        input_file: 输入Excel文件路径
        output_file: 输出Excel文件路径，如果为None则自动生成

    返回：
        输出文件路径
    """

    # 读取原始文件
    print(f"正在读取文件: {input_file}")
    df = pd.read_excel(input_file)

    original_count = len(df)
    print(f"原始数据行数: {original_count}")

    # 将创建时间转换为日期格式
    df['创建时间_dt'] = pd.to_datetime(df['创建时间'])

    # ==================== 应用过滤条件 ====================

    # 1. 剔除: 门店含"宁波开元" 且 时间>=2025-01-01
    condition1 = ~((df['组织'].str.contains('宁波开元', na=False)) &
                   (df['创建时间_dt'] >= '2025-01-01'))
    removed_ningbo = original_count - len(df[condition1])

    # 2. 剔除: 门店含"慈溪附海" 且 时间>=2025-04-25
    condition2 = ~((df['组织'].str.contains('附海', na=False)) &
                   (df['创建时间_dt'] >= '2025-04-25'))
    removed_cixi = original_count - len(df[condition2])

    # 3. 剔除: 门店含"绍兴斗门"（不分年份）
    condition3 = ~(df['组织'].str.contains('斗门', na=False))
    removed_shaoxing = original_count - len(df[condition3])

    # 4. 剔除: 单据编码以"JMCX"开头
    condition4 = ~(df['加盟收货单'].str.startswith('JMCX', na=False))
    removed_jmcx = original_count - len(df[condition4])

    # 5. 仅保留: 大类='足金'、'足金（新）'、'爱尚金'
    condition5 = df['大类'].isin(['足金', '足金（新）', '爱尚金'])
    kept_categories = len(df[condition5])

    # 应用所有条件
    df_filtered = df[condition1 & condition2 & condition3 & condition4 & condition5].copy()

    # 删除临时时间列
    df_filtered.drop('创建时间_dt', axis=1, inplace=True)

    filtered_count = len(df_filtered)
    print(f"\n过滤后数据行数: {filtered_count}")

    # 显示过滤统计
    print("\n过滤统计:")
    print(f"  剔除宁波开元(2025-01-01后): {removed_ningbo}")
    print(f"  剔除慈溪附海(2025-04-25后): {removed_cixi}")
    print(f"  剔除绍兴斗门(全部): {removed_shaoxing}")
    print(f"  剔除JMCX开头单据: {removed_jmcx}")
    print(f"  保留指定大类: {kept_categories}")
    print(f"  总共剔除: {original_count - filtered_count} 条")

    # ==================== 新增功能：按件/按克判断 ====================

    print("\n正在判断按件/按克...")
    df_filtered['按件/按克'] = df_filtered['基础价'].apply(
        lambda x: '按件' if pd.notna(x) and x > 0 else '按克'
    )

    # ==================== 新增功能：挂签费核算 ====================

    print("正在核算挂签费...")

    def calculate_guaqian_fee(row):
        """
        计算挂签费

        规则：
        - 如果基础价不为空，挂签费 = 基础价 * 0.04
        - 基础价为空，按克产品：
          - 款式含"金条": 挂签费 = 总重 * 5
          - 款式含"笼统款"不含3D/5G: 挂签费 = 总重 * 13
          - 款式含"笼统款"含3D/5G: 挂签费 = 总重 * 28
        """
        # 如果基础价不为空，挂签费 = 基础价 * 0.04
        if pd.notna(row['基础价']) and row['基础价'] > 0:
            return row['基础价'] * 0.04

        # 基础价为空，按克产品
        款式名称 = str(row['款式']) if pd.notna(row['款式']) else ''
        总重 = row['总重'] if pd.notna(row['总重']) else 0

        # 款式名称含"金条"
        if '金条' in 款式名称:
            return 总重 * 5

        # 款式名称含"笼统款"
        if '笼统款' in 款式名称:
            # 含"3D"或"5G"
            if '3D' in 款式名称 or '5G' in 款式名称:
                return 总重 * 28
            # 不含"3D"或"5G"
            else:
                return 总重 * 13

        # 其他情况返回0
        return 0

    df_filtered['挂签费核算'] = df_filtered.apply(calculate_guaqian_fee, axis=1)

    # ==================== 显示统计信息 ====================

    print("\n按件/按克统计:")
    print(df_filtered['按件/按克'].value_counts())

    print("\n大类分布:")
    print(df_filtered['大类'].value_counts())

    print("\n挂签费核算统计:")
    print(f"  最小值: {df_filtered['挂签费核算'].min():.2f} 元")
    print(f"  最大值: {df_filtered['挂签费核算'].max():.2f} 元")
    print(f"  平均值: {df_filtered['挂签费核算'].mean():.2f} 元")
    print(f"  总金额: {df_filtered['挂签费核算'].sum():.2f} 元")

    # ==================== 保存文件 ====================

    if output_file is None:
        # 自动生成输出文件名
        import os
        base_dir = os.path.dirname(input_file)
        base_name = os.path.basename(input_file)
        name_without_ext = os.path.splitext(base_name)[0]
        output_file = os.path.join(base_dir, f"{name_without_ext}_已过滤.xlsx")

    print(f"\n正在保存到: {output_file}")
    df_filtered.to_excel(output_file, index=False)

    print(f"✅ 完成！共处理 {filtered_count} 条数据")

    return output_file


def main():
    """命令行入口"""
    import sys

    if len(sys.argv) < 2:
        print("用法: python filter_warehouse.py <输入文件路径> [输出文件路径]")
        print("示例: python filter_warehouse.py /path/to/加盟入库单.xlsx")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result_path = filter_and_calculate(input_file, output_file)
        print(f"\n输出文件: {result_path}")
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
