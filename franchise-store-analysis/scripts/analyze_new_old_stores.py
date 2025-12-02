#!/usr/bin/env python3
"""
加盟新老店批发毛利分析脚本
按品类统计新店和老店的批发额和毛利额
"""

import sys
import pandas as pd
from pathlib import Path
from datetime import datetime


def filter_warehouse_receipt(df):
    """
    过滤加盟入库单数据

    过滤规则：
    1. 门店含"宁波开元"的全部删除
    2. 门店含"慈溪附海"且业务时间>=2025-04-25的不计入（使用创建时间判断）
    3. 门店含"绍兴斗门"的不计入（不分年份）
    4. 单据编码以"JMCX"开头的不计入
    5. 仅保留大类='足金'
    """
    original_count = len(df)

    # 1. 删除门店含"宁波开元"
    df = df[~df['组织'].str.contains('宁波开元', na=False)]
    print(f"   剔除'宁波开元'后行数: {len(df)} (减少{original_count - len(df)}行)")

    # 2. 门店含"慈溪附海"且创建时间>=2025-04-25的不计入
    time_col = None
    if '业务时间' in df.columns:
        time_col = '业务时间'
    elif '创建时间' in df.columns:
        time_col = '创建时间'

    if time_col:
        df['时间_dt'] = pd.to_datetime(df[time_col], errors='coerce')
        cixi_fuhai_mask = df['组织'].str.contains('慈溪附海', na=False) & \
                         (df['时间_dt'] >= pd.Timestamp('2025-04-25'))
        before_count = len(df)
        df = df[~cixi_fuhai_mask]
        print(f"   剔除'慈溪附海'(>=2025-04-25)后行数: {len(df)} (减少{before_count - len(df)}行)")

    # 3. 门店含"绍兴斗门"的不计入
    before_count = len(df)
    df = df[~df['组织'].str.contains('绍兴斗门', na=False)]
    print(f"   剔除'绍兴斗门'后行数: {len(df)} (减少{before_count - len(df)}行)")

    # 4. 单据编码以"JMCX"开头的不计入
    # 检查可能的单据编码字段
    doc_col = None
    for col in ['单号', '单据编码', '加盟收货单']:
        if col in df.columns:
            doc_col = col
            break

    if doc_col:
        before_count = len(df)
        df = df[~df[doc_col].str.startswith('JMCX', na=False)]
        print(f"   剔除'{doc_col}'以'JMCX'开头后行数: {len(df)} (减少{before_count - len(df)}行)")

    # 5. 仅保留大类='足金'
    if '大类' in df.columns:
        before_count = len(df)
        df = df[df['大类'] == '足金']
        print(f"   仅保留'大类=足金'后行数: {len(df)} (减少{before_count - len(df)}行)")

    print(f"   总计过滤: {original_count} -> {len(df)} (减少{original_count - len(df)}行)")

    return df


def analyze_new_old_stores(sales_file, return_file, org_mapping_file, warehouse_file=None, other_settlement_file=None, year_2024_data=None, output_path=None):
    """
    分析新老店批发和毛利情况

    参数:
        sales_file: 销售表格文件路径
        return_file: 退货表格文件路径
        org_mapping_file: 组织匹配表文件路径
        warehouse_file: 加盟入库单文件路径（可选,用于黄金外采批发额计算）
        other_settlement_file: 其他结算单文件路径（可选,用于黄金外采毛利额计算）
        year_2024_data: 2024年数据文件路径（可选，用于同比计算）
        output_path: 输出文件路径（可选）
    """
    try:
        print("📊 读取组织匹配表...")
        org_mapping = pd.read_excel(org_mapping_file)
        print(f"   组织数量: {len(org_mapping)}")

        # 处理组织名称，去除末尾的*和M
        org_mapping['组织'] = org_mapping['加盟门店'].str.replace(r'[*M]+$', '', regex=True)

        # 创建新店和已闭店字典
        new_stores = set(org_mapping[org_mapping['2025年新店'] == '是']['组织'].values)
        closed_stores = set(org_mapping[org_mapping['已闭店'] == '是']['组织'].values)
        all_orgs_in_mapping = set(org_mapping['组织'].values)

        print(f"   2025年新店数量: {len(new_stores)}")
        print(f"   已闭店数量: {len(closed_stores)}")

        # 读取销售数据
        print("\n📊 读取销售数据...")
        df_sales = pd.read_excel(sales_file, sheet_name=0)
        print(f"   原始数据行数: {len(df_sales)}")

        # 只保留组织名称以M结尾的门店（可能有空格）
        df_sales = df_sales[df_sales['组织'].str.rstrip().str.endswith('M', na=False)]
        print(f"   仅保留以M结尾的门店后行数: {len(df_sales)}")

        # 处理组织名称
        df_sales['组织_cleaned'] = df_sales['组织'].str.replace(r'[*M]+$', '', regex=True)

        # 剔除已闭店
        df_sales = df_sales[~df_sales['组织_cleaned'].isin(closed_stores)]
        print(f"   剔除闭店后行数: {len(df_sales)}")

        # 标记新店/老店
        df_sales['是否新店'] = df_sales['组织_cleaned'].isin(new_stores)

        # 读取退货数据
        print("\n📊 读取退货数据...")
        df_return = pd.read_excel(return_file, sheet_name=0)
        print(f"   原始数据行数: {len(df_return)}")

        # 只保留组织名称以M结尾的门店（可能有空格）
        df_return = df_return[df_return['组织'].str.rstrip().str.endswith('M', na=False)]
        print(f"   仅保留以M结尾的门店后行数: {len(df_return)}")

        # 处理组织名称
        df_return['组织_cleaned'] = df_return['组织'].str.replace(r'[*M]+$', '', regex=True)

        # 剔除已闭店
        df_return = df_return[~df_return['组织_cleaned'].isin(closed_stores)]
        print(f"   剔除闭店后行数: {len(df_return)}")

        # 标记新店/老店
        df_return['是否新店'] = df_return['组织_cleaned'].isin(new_stores)

        # 读取入库单数据（如果提供）
        df_warehouse = None
        if warehouse_file:
            print("\n📊 读取入库单数据...")
            df_warehouse = pd.read_excel(warehouse_file, sheet_name=0)
            print(f"   原始数据行数: {len(df_warehouse)}")

            # 应用入库单过滤规则
            print("   应用过滤规则:")
            df_warehouse = filter_warehouse_receipt(df_warehouse)

            # 只保留组织名称以M结尾的门店（可能有空格）
            before_count = len(df_warehouse)
            df_warehouse = df_warehouse[df_warehouse['组织'].str.rstrip().str.endswith('M', na=False)]
            print(f"   仅保留以M结尾的门店后行数: {len(df_warehouse)} (减少{before_count - len(df_warehouse)}行)")

            # 处理组织名称
            df_warehouse['组织_cleaned'] = df_warehouse['组织'].str.replace(r'[*M]+$', '', regex=True)

            # 剔除已闭店
            df_warehouse = df_warehouse[~df_warehouse['组织_cleaned'].isin(closed_stores)]
            print(f"   剔除闭店后行数: {len(df_warehouse)}")

            # 标记新店/老店
            df_warehouse['是否新店'] = df_warehouse['组织_cleaned'].isin(new_stores)

        # 读取其他结算单数据（如果提供）
        df_other_settlement = None
        if other_settlement_file:
            print("\n📊 读取其他结算单数据...")
            df_other_settlement = pd.read_excel(other_settlement_file, sheet_name=0)
            print(f"   原始数据行数: {len(df_other_settlement)}")

            # 筛选：已扣款 + 服务费(挂标签）
            df_other_settlement = df_other_settlement[
                (df_other_settlement['状态'] == '已扣款') &
                (df_other_settlement['结算类型'] == '服务费(挂标签）')
            ]
            print(f"   筛选已扣款+服务费(挂标签)后行数: {len(df_other_settlement)}")

            # 处理组织名称
            if '加盟门店' in df_other_settlement.columns:
                # 只保留组织名称以M结尾的门店（可能有空格）
                before_count = len(df_other_settlement)
                df_other_settlement = df_other_settlement[df_other_settlement['加盟门店'].str.rstrip().str.endswith('M', na=False)]
                print(f"   仅保留以M结尾的门店后行数: {len(df_other_settlement)} (减少{before_count - len(df_other_settlement)}行)")

                df_other_settlement['组织_cleaned'] = df_other_settlement['加盟门店'].str.replace(r'[*M]+$', '', regex=True)

                # 剔除已闭店
                df_other_settlement = df_other_settlement[~df_other_settlement['组织_cleaned'].isin(closed_stores)]
                print(f"   剔除闭店后行数: {len(df_other_settlement)}")

                # 标记新店/老店
                df_other_settlement['是否新店'] = df_other_settlement['组织_cleaned'].isin(new_stores)

        # 确保数值列为数字类型
        df_sales['销售金额'] = pd.to_numeric(df_sales['销售金额'], errors='coerce').fillna(0)
        df_sales['暂估成本'] = pd.to_numeric(df_sales['暂估成本'], errors='coerce').fillna(0)
        df_return['退回金额'] = pd.to_numeric(df_return['退回金额'], errors='coerce').fillna(0)
        df_return['暂估成本'] = pd.to_numeric(df_return['暂估成本'], errors='coerce').fillna(0)

        # 检查是否有组织不在匹配表中
        print("\n🔍 检查组织匹配情况...")
        missing_orgs = set()

        # 收集所有数据源中的组织
        sales_orgs = set(df_sales['组织_cleaned'].unique())
        return_orgs = set(df_return['组织_cleaned'].unique())

        all_data_orgs = sales_orgs | return_orgs

        if df_warehouse is not None:
            warehouse_orgs = set(df_warehouse['组织_cleaned'].unique())
            all_data_orgs |= warehouse_orgs

        if df_other_settlement is not None:
            settlement_orgs = set(df_other_settlement['组织_cleaned'].unique())
            all_data_orgs |= settlement_orgs

        # 找出不在匹配表中的组织
        missing_orgs = all_data_orgs - all_orgs_in_mapping

        if missing_orgs:
            print(f"\n⚠️  警告：发现 {len(missing_orgs)} 个组织不在组织匹配表中！")
            print("   请将以下组织添加到组织匹配表：")
            for org in sorted(missing_orgs):
                print(f"   - {org}")
            print("\n   这些组织的数据将被视为老店处理。")
            print("   建议更新组织匹配表后重新运行分析。\n")
        else:
            print("   ✅ 所有组织都在匹配表中")

        print("\n📊 开始按品类统计...")

        # 品类列表
        categories = ['黄金外采-新模式', '黄金', '钻石', '爱尚炫', '18K', '翡翠', '其他']

        results = []

        for category in categories:
            # 黄金外采-新模式使用特殊计算逻辑
            if category == '黄金外采-新模式':
                # 老店批发/毛利 = 0 (黄金外采是新模式,没有老店)
                old_wholesale_2025 = 0
                old_profit_2025 = 0

                # 计算入库单总成本
                warehouse_cost = 0
                if df_warehouse is not None and len(df_warehouse) > 0:
                    # 确保总成本字段为数字
                    df_warehouse['总成本'] = pd.to_numeric(df_warehouse['总成本'], errors='coerce').fillna(0)
                    warehouse_cost = df_warehouse['总成本'].sum()

                # 计算其他结算单发生金额/1.06
                settlement_amount = 0
                if df_other_settlement is not None and len(df_other_settlement) > 0:
                    # 确保发生金额字段为数字
                    df_other_settlement['发生金额'] = pd.to_numeric(df_other_settlement['发生金额'], errors='coerce').fillna(0)
                    settlement_amount = df_other_settlement['发生金额'].sum() / 1.06

                # 批发额 = 入库单总成本 + 其他结算单发生金额/1.06
                new_wholesale_2025 = warehouse_cost + settlement_amount

                # 毛利额 = 其他结算单发生金额/1.06
                new_profit_2025 = settlement_amount

                # 汇总
                total_wholesale = old_wholesale_2025 + new_wholesale_2025
                total_profit = old_profit_2025 + new_profit_2025
            else:
                # 其他品类使用常规计算逻辑
                sales_cat = df_sales[df_sales['品类'] == category]
                return_cat = df_return[df_return['品类'] == category]

                # 老店数据
                old_sales = sales_cat[sales_cat['是否新店'] == False]
                old_return = return_cat[return_cat['是否新店'] == False]

                # 新店数据
                new_sales = sales_cat[sales_cat['是否新店'] == True]
                new_return = return_cat[return_cat['是否新店'] == True]

                # 老店批发（含税）= 销售金额 - 退回金额
                old_wholesale_2025 = old_sales['销售金额'].sum() - old_return['退回金额'].sum()

                # 新店批发（含税）
                new_wholesale_2025 = new_sales['销售金额'].sum() - new_return['退回金额'].sum()

                # 老店毛利（未税）= (销售金额 - 暂估成本)/1.13 - (退回金额 - 暂估成本)/1.13
                old_profit_2025 = (old_sales['销售金额'].sum() - old_sales['暂估成本'].sum()) / 1.13 - \
                                 (old_return['退回金额'].sum() - old_return['暂估成本'].sum()) / 1.13

                # 新店毛利（未税）
                new_profit_2025 = (new_sales['销售金额'].sum() - new_sales['暂估成本'].sum()) / 1.13 - \
                                 (new_return['退回金额'].sum() - new_return['暂估成本'].sum()) / 1.13

                # 批发额
                total_wholesale = old_wholesale_2025 + new_wholesale_2025

                # 毛利额
                total_profit = old_profit_2025 + new_profit_2025

            results.append({
                '品类': category,
                '老店批发（含税）_2024年': 0,  # 需要2024年数据
                '老店批发（含税）_2025年': old_wholesale_2025,
                '老店批发（含税）_同比增长率': 0,  # 需要2024年数据
                '老店批发（含税）_同比差异': 0,  # 需要2024年数据
                '新店批发（含税）_2025年': new_wholesale_2025,
                '2025年新老店合计_批发额': total_wholesale,
                '2025年新老店合计_同比增长率': 0,  # 需要2024年数据
                '老店毛利（未税）_2024年': 0,  # 需要2024年数据
                '老店毛利（未税）_2025年': old_profit_2025,
                '老店毛利（未税）_同比增长率': 0,  # 需要2024年数据
                '老店毛利（未税）_同比差异': 0,  # 需要2024年数据
                '新店毛利（未税）_2025年': new_profit_2025,
                '2025年新老店合计_毛利额': total_profit,
                '2025年新老店合计_同比增长率_毛利': 0,  # 需要2024年数据
            })

        # 创建结果DataFrame
        result_df = pd.DataFrame(results)

        # 计算合计行（剔除黄金外采-新模式）
        total_row_data = result_df[result_df['品类'] != '黄金外采-新模式']
        total_row = {
            '品类': '合计',
            '老店批发（含税）_2024年': total_row_data['老店批发（含税）_2024年'].sum(),
            '老店批发（含税）_2025年': total_row_data['老店批发（含税）_2025年'].sum(),
            '老店批发（含税）_同比增长率': 0,
            '老店批发（含税）_同比差异': 0,
            '新店批发（含税）_2025年': total_row_data['新店批发（含税）_2025年'].sum(),
            '2025年新老店合计_批发额': total_row_data['2025年新老店合计_批发额'].sum(),
            '2025年新老店合计_同比增长率': 0,
            '老店毛利（未税）_2024年': total_row_data['老店毛利（未税）_2024年'].sum(),
            '老店毛利（未税）_2025年': total_row_data['老店毛利（未税）_2025年'].sum(),
            '老店毛利（未税）_同比增长率': 0,
            '老店毛利（未税）_同比差异': 0,
            '新店毛利（未税）_2025年': total_row_data['新店毛利（未税）_2025年'].sum(),
            '2025年新老店合计_毛利额': total_row_data['2025年新老店合计_毛利额'].sum(),
            '2025年新老店合计_同比增长率_毛利': 0,
        }

        # 插入合计行（在黄金外采-新模式之前）
        result_df = pd.concat([
            result_df[result_df['品类'] != '黄金外采-新模式'],
            pd.DataFrame([total_row]),
            result_df[result_df['品类'] == '黄金外采-新模式']
        ], ignore_index=True)

        # 计算总计行（包含黄金外采-新模式）
        grand_total_row = {
            '品类': '总计',
            '老店批发（含税）_2024年': result_df[result_df['品类'].isin(['合计', '黄金外采-新模式'])]['老店批发（含税）_2024年'].sum(),
            '老店批发（含税）_2025年': result_df[result_df['品类'].isin(['合计', '黄金外采-新模式'])]['老店批发（含税）_2025年'].sum(),
            '老店批发（含税）_同比增长率': 0,
            '老店批发（含税）_同比差异': 0,
            '新店批发（含税）_2025年': result_df[result_df['品类'].isin(['合计', '黄金外采-新模式'])]['新店批发（含税）_2025年'].sum(),
            '2025年新老店合计_批发额': result_df[result_df['品类'].isin(['合计', '黄金外采-新模式'])]['2025年新老店合计_批发额'].sum(),
            '2025年新老店合计_同比增长率': 0,
            '老店毛利（未税）_2024年': result_df[result_df['品类'].isin(['合计', '黄金外采-新模式'])]['老店毛利（未税）_2024年'].sum(),
            '老店毛利（未税）_2025年': result_df[result_df['品类'].isin(['合计', '黄金外采-新模式'])]['老店毛利（未税）_2025年'].sum(),
            '老店毛利（未税）_同比增长率': 0,
            '老店毛利（未税）_同比差异': 0,
            '新店毛利（未税）_2025年': result_df[result_df['品类'].isin(['合计', '黄金外采-新模式'])]['新店毛利（未税）_2025年'].sum(),
            '2025年新老店合计_毛利额': result_df[result_df['品类'].isin(['合计', '黄金外采-新模式'])]['2025年新老店合计_毛利额'].sum(),
            '2025年新老店合计_同比增长率_毛利': 0,
        }

        result_df = pd.concat([result_df, pd.DataFrame([grand_total_row])], ignore_index=True)

        # 格式化输出
        print("\n" + "=" * 150)
        print("📈 2025年加盟新老店批发&毛利情况")
        print("=" * 150)
        print()

        pd.options.display.float_format = '{:,.0f}'.format
        print(result_df[['品类', '老店批发（含税）_2025年', '新店批发（含税）_2025年',
                        '2025年新老店合计_批发额', '老店毛利（未税）_2025年',
                        '新店毛利（未税）_2025年', '2025年新老店合计_毛利额']].to_string(index=False))
        print()

        # 保存到Excel
        if output_path:
            output_file = output_path
        else:
            output_file = "加盟新老店批发毛利分析结果.xlsx"

        # 先保存原始数据到临时文件
        temp_file = output_file.replace('.xlsx', '_temp.xlsx')
        result_df.to_excel(temp_file, index=False)

        # 美化输出
        try:
            from format_beautiful_excel import format_beautiful_excel
            format_beautiful_excel(temp_file, output_file)
            # 删除临时文件
            import os
            os.remove(temp_file)
        except Exception as e:
            print(f"⚠️  美化格式失败，使用原始格式: {e}")
            result_df.to_excel(output_file, index=False)

        print(f"✅ 结果已保存到: {output_file}")
        print(f"   注：剔除关闭店；移店、更换加盟商视同老店；净批发额、净毛利额数据")

        return result_df

    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python analyze_new_old_stores.py <销售文件> <退货文件> <组织匹配表> [入库单文件] [其他结算单文件] [输出文件]")
        print("\n示例:")
        print("  # 基本用法")
        print("  python analyze_new_old_stores.py 销售.xlsx 退货.xlsx 组织匹配.xlsx")
        print()
        print("  # 包含入库单")
        print("  python analyze_new_old_stores.py 销售.xlsx 退货.xlsx 组织匹配.xlsx 入库.xlsx")
        print()
        print("  # 包含入库单和其他结算单")
        print("  python analyze_new_old_stores.py 销售.xlsx 退货.xlsx 组织匹配.xlsx 入库.xlsx 其他结算单.xlsx")
        print()
        print("  # 指定输出文件")
        print("  python analyze_new_old_stores.py 销售.xlsx 退货.xlsx 组织匹配.xlsx 入库.xlsx 其他结算单.xlsx 结果.xlsx")
        sys.exit(1)

    sales_file = sys.argv[1]
    return_file = sys.argv[2]
    org_mapping = sys.argv[3]

    # 解析可选参数
    warehouse_file = None
    other_settlement_file = None
    output_file = None

    if len(sys.argv) > 4:
        # 第4个参数：入库单或输出文件
        if sys.argv[4].endswith('.xlsx') and '入库' in sys.argv[4]:
            warehouse_file = sys.argv[4]

            if len(sys.argv) > 5:
                # 第5个参数：其他结算单或输出文件
                if sys.argv[5].endswith('.xlsx') and ('结算' in sys.argv[5] or '其他' in sys.argv[5]):
                    other_settlement_file = sys.argv[5]
                    output_file = sys.argv[6] if len(sys.argv) > 6 else None
                else:
                    output_file = sys.argv[5]
        else:
            output_file = sys.argv[4]

    analyze_new_old_stores(sales_file, return_file, org_mapping,
                          warehouse_file=warehouse_file,
                          other_settlement_file=other_settlement_file,
                          output_path=output_file)
