"""
Simple usage example for Odin PLN Calculator
-------------------------------------------
This example demonstrates basic usage of the OdinPLNCalculator class.

Odin PLN 計算器的簡單使用示例
--------------------------
此示例演示 OdinPLNCalculator 類的基本用法。
"""

import sys
import os

# Add parent directory to path to import the odin_pln module
# 添加上級目錄到路徑，以便導入 odin_pln 模塊
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from odin_pln import OdinPLNCalculator

def main():
    """
    Main function that demonstrates calculator usage
    
    演示計算器使用方法的主函數
    """
    # Initialize PLN calculator | 初始化 PLN 計算器
    calculator = OdinPLNCalculator()
    
    # Example user ID and token ID | 示例用戶 ID 和代幣 ID
    user_id = "vj5mg-hquhw-x2amt-ukf2l-zgnjw-bbsac-s35gm-pycq6-fzuny-v6e7g-2ae"
    token_id = "2933"  # Replace with an actual token ID | 替換為實際存在的代幣ID
    
    # Specify time range in days | 指定時間範圍（天數）
    time_range_days = 30
    
    print(f"Calculating PLN for user {user_id}, token {token_id} over the last {time_range_days} days...")
    print(f"計算用戶 {user_id} 的代幣 {token_id} 在最近 {time_range_days} 天的 PLN...")
    
    # Calculate and format PLN results | 計算並格式化 PLN 結果
    result = calculator.get_formatted_token_pln(user_id, token_id, time_range_days)
    
    # Display results | 顯示結果
    if result["success"]:
        print("\n===== PLN Calculation Results | PLN 計算結果 =====")
        print(f"Realized PLN | 已實現 PLN: {result['realized_pln']}")
        print(f"Unrealized PLN | 未實現 PLN: {result['unrealized_pln']}")
        print(f"Total PLN | 總 PLN: {result['total_pln']}")
        print(f"Yield Rate | 收益率: {result['yield_rate']}")
        print(f"Current Holdings | 當前持有: {result['current_holdings']} tokens/個代幣")
        print("=" * 45)
    else:
        print(f"Calculation failed | 計算失敗: {result['error']}")

if __name__ == "__main__":
    main()