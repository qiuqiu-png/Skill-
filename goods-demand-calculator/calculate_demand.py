#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
货盘需求计算器
根据库存、在途、销售数据自动计算门店补货需求量
"""

import sys
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string


def calculate_goods_demand(input_file, output_file=None):
    """
    计算货盘需求

    参数:
        input_file: 输入Excel文件路径
        output_file: 输出Excel文件路径（可选，默认添加_处理后后缀）
    """
    # 如果没有指定输出文件，自动生成
    if output_file is None:
        if input_file.endswith('.xlsx'):
            output_file = input_file.replace('.xlsx', '_处理后.xlsx')
        else:
            output_file = input_file + '_处理后.xlsx'

    print("正在加载Excel文件...")
    wb = load_workbook(input_file)
    ws = wb.active

    print(f"工作表名称: {ws.title}")
    print(f"总行数: {ws.max_row}")

    # DS列到YD列的列号
    ds_col = column_index_from_string('DS')
    yd_col = column_index_from_string('YD')
    ci_col = column_index_from_string('CI')

    # 第一步：获取第6行的门店分组（合并单元格）
    print("\n=== 第一步：获取门店分组 ===")
    store_groups = []
    for merged_range in ws.merged_cells.ranges:
        if merged_range.min_row == 6 and merged_range.max_row == 6:
            if merged_range.min_col >= ds_col and merged_range.min_col <= yd_col:
                cell_value = ws.cell(6, merged_range.min_col).value
                store_groups.append({
                    'name': cell_value,
                    'min_col': merged_range.min_col,
                    'max_col': merged_range.max_col
                })

    # 按列号排序
    store_groups.sort(key=lambda x: x['min_col'])
    print(f"找到 {len(store_groups)} 个门店分组")

    # 第二步：对于每个门店分组，找到其中的"库存"、"在途"、"销售"、"需求"列
    print("\n=== 第二步：查找每个门店的关键列 ===")
    for store in store_groups:
        # 在第7行中查找对应的列标题
        store_cols = {}
        for col_idx in range(store['min_col'], store['max_col'] + 1):
            header = ws.cell(7, col_idx).value
            if header:
                header = str(header).strip()
                if header == '库存':
                    store_cols['库存'] = col_idx
                elif header == '在途':
                    store_cols['在途'] = col_idx
                elif header == '销售':
                    store_cols['销售'] = col_idx
                elif header == '需求':
                    store_cols['需求'] = col_idx

        store['cols'] = store_cols

    # 统计有完整列的门店数量
    valid_stores = sum(1 for s in store_groups if len(s['cols']) == 4)
    print(f"有完整列（库存/在途/销售/需求）的门店: {valid_stores}/{len(store_groups)}")

    # 第三步：筛选符合条件的行
    print("\n=== 第三步：筛选符合条件的行 ===")
    valid_rows = []
    for row_idx in range(8, ws.max_row + 1):
        b_val = ws.cell(row_idx, 2).value  # B列
        ci_val = ws.cell(row_idx, ci_col).value  # CI列

        # 检查B列是否为"足金"或"足金（新）"
        if b_val and (str(b_val).strip() == '足金' or str(b_val).strip() == '足金（新）'):
            # 检查CI列是否>0
            if ci_val and isinstance(ci_val, (int, float)) and ci_val > 0:
                valid_rows.append(row_idx)

    print(f"找到 {len(valid_rows)} 行符合条件（B列=足金/足金（新） 且 CI列>0）")
    if len(valid_rows) > 0:
        print(f"行号范围: {valid_rows[0]} - {valid_rows[-1]}")

    # 第四步：处理每个符合条件的行
    print("\n=== 第四步：填写需求值 ===")
    update_count = 0
    skip_count = 0

    for row_idx in valid_rows:
        # 对每个门店分组进行处理
        for store in store_groups:
            cols = store['cols']

            # 检查是否有所有需要的列
            if '库存' not in cols or '在途' not in cols or '销售' not in cols or '需求' not in cols:
                skip_count += 1
                continue

            # 获取库存、在途、销售的值
            inventory = ws.cell(row_idx, cols['库存']).value
            in_transit = ws.cell(row_idx, cols['在途']).value
            sales = ws.cell(row_idx, cols['销售']).value

            # 转换为数值，如果为None则为0
            inventory = float(inventory) if inventory and isinstance(inventory, (int, float)) else 0
            in_transit = float(in_transit) if in_transit and isinstance(in_transit, (int, float)) else 0
            sales = float(sales) if sales and isinstance(sales, (int, float)) else 0

            # 忽略销售<=0或为空的门店
            if sales <= 0:
                continue

            # 计算：库存 + 在途 - 销售
            diff = inventory + in_transit - sales

            # 根据条件填写需求值
            demand_col = cols['需求']
            if diff < 0:
                # 库存+在途-销售 < 0，填写绝对值*2
                demand_value = abs(diff) * 2
                ws.cell(row_idx, demand_col).value = demand_value
                update_count += 1
            else:
                # 库存+在途-销售 >= 0，填写1
                ws.cell(row_idx, demand_col).value = 1
                update_count += 1

    print(f"共更新了 {update_count} 个单元格的需求值")
    if skip_count > 0:
        print(f"跳过了 {skip_count} 个不完整的门店数据")

    # 保存文件
    print("\n正在保存文件...")
    wb.save(output_file)
    wb.close()

    print(f"\n✅ 处理完成！")
    print(f"📁 输出文件: {output_file}")

    return output_file


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python3 calculate_demand.py <输入文件路径> [输出文件路径]")
        print("示例: python3 calculate_demand.py /path/to/货盘数据.xlsx")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        calculate_goods_demand(input_file, output_file)
    except Exception as e:
        print(f"\n❌ 处理失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
