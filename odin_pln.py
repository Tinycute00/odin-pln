"""
Odin PLN Calculator
------------------
A tool for calculating Profit/Loss Net (PLN) of tokens on the Odin platform.

Odin PLN 計算器
-------------
用於計算 Odin 平台上代幣盈虧淨值 (PLN) 的工具。
"""

import logging
import requests
import json
import os
import time
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta, timezone
import argparse
from decimal import Decimal

# Configure logging | 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('odin_pln.log')
    ]
)
logger = logging.getLogger('Odin_PLN_Calculation')

# API endpoint | API 端點
API_BASE_URL = "https://api.odin.fun/v1"

class OdinPLNCalculator:
    """
    Odin PLN (Profit/Loss Net) Calculator class for calculating token profit/loss
    
    Odin PLN（盈虧淨值）計算器類，用於計算代幣盈虧
    """
    
    API_BASE_URL = "https://api.odin.fun/v1"
    
    def __init__(self):
        """
        Initialize the PLN calculator
        
        初始化 PLN 計算器
        """
        self.logger = logging.getLogger('Odin_PLN_Calculation')
        self.logger.setLevel(logging.DEBUG)
        
        # Ensure at least one handler | 確保至少有一個處理器
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _api_get(self, path: str, params: dict = None) -> dict:
        """
        Call API and return response
        
        調用 API 並返回響應
        """
        url = f"{self.API_BASE_URL}/{path}"
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API call failed ({url}): {e}")
            self.logger.error(f"API 調用失敗 ({url}): {e}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"API response JSON decode failed ({url}): {e}")
            self.logger.error(f"API 響應 JSON 解碼失敗 ({url}): {e}")
            self.logger.error(f"Response content: {response.text[:500]}")
            self.logger.error(f"響應內容: {response.text[:500]}")
            raise
    
    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user information
        
        獲取用戶信息
        """
        try:
            return self._api_get(f"user/{user_id}")
        except Exception as e:
            self.logger.error(f"Failed to get user info: {e}")
            self.logger.error(f"獲取用戶信息失敗: {e}")
            return None

    def get_user_activity(self, user_id: str, page: int = 1, limit: int = 50, start_time: Optional[int] = None, end_time: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Get user activity records
        
        獲取用戶活動記錄
        """
        try:
            params = {
                "sort": "time:asc",  # Sort ascending by time for easier PLN calculation
                "page": page,
                "limit": limit
            }
            if start_time:
                params["start_time"] = start_time
            if end_time:
                params["end_time"] = end_time
            
            self.logger.info(f"Calling get_user_activity: user={user_id}, page={page}, limit={limit}")
            self.logger.info(f"調用 get_user_activity: user={user_id}, page={page}, limit={limit}")
            return self._api_get(f"user/{user_id}/activity", params)
        except Exception as e:
            return None
    
    def calculate_token_pln(self, user_id: str, token_id: str, time_range_days: int = 30) -> Dict[str, Any]:
        """
        Calculate PLN for specified user and token
        
        計算指定用戶和代幣的 PLN
        """
        self.logger.info(f"Starting PLN calculation for user {user_id}, token {token_id} (last {time_range_days} days)")
        self.logger.info(f"開始計算用戶 {user_id} 代幣 {token_id} 的 PLN (最近 {time_range_days} 天)")

        # Calculate timestamps for the time range
        end_dt = datetime.now(timezone.utc)
        start_dt = end_dt - timedelta(days=time_range_days)
        end_timestamp = int(end_dt.timestamp())
        start_timestamp = int(start_dt.timestamp())
        
        # Get user activity records | 獲取用戶活動記錄
        trades = []
        page = 1
        fetched_ids = set()  # Track fetched trade IDs to prevent duplicates if API pagination is weird

        while True:
            self.logger.info(f"Getting page {page} of trade records")
            self.logger.info(f"正在獲取第 {page} 頁交易記錄")
            response = self.get_user_activity(
                user_id,
                page=page,
                limit=100,  # Fetch more per page if possible
                start_time=start_timestamp,
                end_time=end_timestamp
            )

            # Check for API call failure | 檢查 API 調用是否失敗
            if response is None:
                break
                
            # Check for 'data' key existence | 檢查 'data' 鍵是否存在
            if "data" not in response:
                break
                
            data = response["data"]
            if not isinstance(data, list) or not data:
                break
                
            # Filter activities by token_id and action | 按代幣ID和操作類型過濾活動
            new_trades_on_page = 0
            for trade in data:
                if not isinstance(trade, dict):
                    continue
                    
                trade_id = trade.get("id")
                if trade_id is None or trade_id in fetched_ids:
                    continue

                # Filter by token and action | 按代幣和操作過濾
                if trade.get("token", {}).get("id") == token_id and \
                   trade.get("action") in ["BUY", "SELL"]:
                    trades.append(trade)
                    fetched_ids.add(trade_id)
                    new_trades_on_page += 1

            self.logger.info(f"Found {new_trades_on_page} new relevant trades on page {page} (total: {len(trades)})")
            self.logger.info(f"第 {page} 頁找到 {new_trades_on_page} 筆新的相關交易 (總累計: {len(trades)})")

            # Check pagination based on items returned vs limit | 基於返回項目數與限制比較檢查分頁
            current_limit = response.get("limit", 100)
            current_count_on_page = len(data)

            if current_count_on_page < current_limit:
                break
                    
            page += 1
            # Safety break | 安全中斷
            if page > 50:  # Limit pages
                break
                
        self.logger.info(f"Found a total of {len(trades)} relevant trades")
        self.logger.info(f"總共找到 {len(trades)} 筆相關交易")

        if not trades:
            return {
                "realized_pln": 0,
                "unrealized_pln": 0,
                "total_pln": 0,
                "yield_rate": 0,
                "current_value": 0,
                "current_holdings": 0
            }

        # Sort trades by time (ascending) | 按時間（升序）排序交易
        trades.sort(key=lambda x: x.get("time", ""))

        # Calculate PLN | 計算 PLN
        total_buy_quantity = 0
        total_buy_cost = 0
        total_sell_quantity = 0
        total_sell_income = 0
        current_holdings = 0

        for trade in trades:
            trade_id = trade.get("id", "N/A")
            action = trade.get("action")
            try:
                quantity_str = trade.get("amount_token")
                btc_amount_str = trade.get("amount_btc")

                if quantity_str is None or btc_amount_str is None:
                    continue

                quantity = int(quantity_str)
                btc_amount = int(btc_amount_str)  # This is the total BTC amount for this trade
                
                if action == "BUY":
                    total_buy_quantity += quantity
                    total_buy_cost += btc_amount
                    current_holdings += quantity
                elif action == "SELL":
                    total_sell_quantity += quantity
                    total_sell_income += btc_amount
                    current_holdings -= quantity
                else:
                    continue
            except Exception:
                continue

        # Calculate realized PLN (using average cost method) | 計算已實現 PLN (使用平均成本法)
        realized_pln = 0
        if total_buy_quantity > 0 and total_sell_quantity > 0:
            avg_buy_cost_per_unit = Decimal(total_buy_cost) / Decimal(total_buy_quantity)
            cost_basis_sold = avg_buy_cost_per_unit * Decimal(total_sell_quantity)
            realized_pln = Decimal(total_sell_income) - cost_basis_sold
            realized_pln = int(realized_pln)
        elif total_sell_quantity > 0:
            realized_pln = total_sell_income
        else:
            realized_pln = 0

        # Calculate unrealized PLN (temporarily set to 0, requires current market price)
        # 計算未實現 PLN (暫時設為0，需要當前市場價格)
        unrealized_pln = 0
        current_value = 0
        
        # Calculate total PLN | 計算總 PLN
        total_pln = realized_pln + unrealized_pln

        # Calculate yield rate | 計算收益率
        yield_rate = 0
        if total_buy_cost > 0:
            yield_rate = (total_pln / total_buy_cost) * 100

        return {
            "realized_pln": realized_pln,
            "unrealized_pln": unrealized_pln,
            "total_pln": total_pln,
            "yield_rate": yield_rate,
            "current_value": current_value,
            "current_holdings": current_holdings
        }

    def get_formatted_token_pln(self, user_id: str, token_id: str, time_range_days: int = 30) -> Dict[str, Any]:
        """
        Get formatted token PLN results
        
        獲取格式化的代幣 PLN 結果
        """
        try:
            result = self.calculate_token_pln(user_id, token_id, time_range_days)
            
            # Convert satoshi amounts to BTC for display (8 decimal places)
            realized_pln_btc = result["realized_pln"] / 100000000
            unrealized_pln_btc = result["unrealized_pln"] / 100000000
            total_pln_btc = result["total_pln"] / 100000000
            current_value_btc = result["current_value"] / 100000000
            
            # Format with proper signs and BTC suffix | 使用正確的符號和BTC後綴進行格式化
            return {
                "success": True,
                "realized_pln": f"{realized_pln_btc:+.8f} BTC",
                "unrealized_pln": f"{unrealized_pln_btc:+.8f} BTC",
                "total_pln": f"{total_pln_btc:+.8f} BTC",
                "yield_rate": f"{result['yield_rate']:+.2f}%",
                "current_value": f"{current_value_btc:.8f} BTC",
                "current_holdings": result["current_holdings"],
                "time_range": f"{time_range_days} days" if time_range_days == 1 else f"{time_range_days} days/天"
            }
        except Exception as e:
            self.logger.error(f"Error formatting token PLN results: {e}")
            self.logger.error(f"格式化代幣 PLN 結果時發生錯誤: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def calculate_total_pln(self, user_id: str, time_range_days: int = 30, top_n: int = 5) -> Dict[str, Any]:
        """
        Calculate total PLN for all user tokens
        
        計算用戶所有代幣的總 PLN
        """
        self.logger.info(f"Starting total PLN calculation for user {user_id} (last {time_range_days} days)")
        self.logger.info(f"開始計算用戶 {user_id} 的總 PLN (最近 {time_range_days} 天)")
        
        # TODO: Get list of all user tokens and iterate calculation
        # 目前僅返回一個虛擬結果作為示例
        
        return {
            "total_pln": 1000000,  # 1000000 sats = 0.01 BTC
            "yield_rate": 5.2,
            "token_count": top_n
        }

# Command line handling | 命令行處理
def main():
    """
    Main function for command line operation
    
    命令行操作的主函數
    """
    parser = argparse.ArgumentParser(description='Odin PLN (Profit/Loss Net) Calculator | Odin PLN（盈虧淨值）計算器')
    parser.add_argument('--user', type=str, help='User ID | 用戶 ID')
    parser.add_argument('--token', type=str, help='Token ID | 代幣 ID')
    parser.add_argument('--days', type=int, default=30, choices=[7, 14, 30, 90, 120], 
                        help='Day range for calculation (default: 30) | 計算的天數範圍（默認：30）')
    parser.add_argument('--total-pln', action='store_true', 
                        help='Calculate total PLN for all tokens | 計算所有代幣的總 PLN')
    parser.add_argument('--top-tokens', type=int, default=5, 
                        help='Calculate top N most active tokens (default: 5) | 計算前 N 個最活躍的代幣（默認：5）')
    
    args = parser.parse_args()
    
    if not args.user:
        print("Error: Please specify a user ID (use --user parameter)")
        print("錯誤: 請指定用戶 ID (使用 --user 參數)")
        return
    
    calculator = OdinPLNCalculator()
    
    if args.total_pln:
        result = calculator.calculate_total_pln(args.user, args.days, args.top_tokens)
        print(f"\nTotal PLN statistics for user {args.user} (last {args.days} days):")
        print(f"用戶 {args.user} 的總 PLN 統計 (最近 {args.days} 天):")
        print(f"\nTotal PLN | 總 PLN: {result['total_pln']/100000000:.8f} BTC")
        print(f"Yield Rate | 收益率: {result['yield_rate']}%")
        print(f"Token Count | 涵蓋代幣數量: {result['token_count']}")
    elif args.token:
        result = calculator.get_formatted_token_pln(args.user, args.token, args.days)
        
        if result["success"]:
            print(f"\nPLN statistics for user {args.user}, token {args.token} (last {args.days} days):")
            print(f"用戶 {args.user} 代幣 {args.token} 的 PLN 統計 (最近 {args.days} 天):")
            print(f"\nRealized PLN | 已實現 PLN: {result['realized_pln']}")
            print(f"Unrealized PLN | 未實現 PLN: {result['unrealized_pln']}")
            print(f"Total PLN | 總 PLN: {result['total_pln']}")
            print(f"Yield Rate | 收益率: {result['yield_rate']}")
            print(f"Current Holdings | 當前持有: {result['current_holdings']} tokens/個代幣")
        else:
            print(f"\nCalculation failed | 計算失敗: {result['error']}")
    else:
        print("Error: Please specify a token ID (use --token parameter) or use --total-pln parameter to calculate total PLN")
        print("錯誤: 請指定代幣 ID (使用 --token 參數) 或使用 --total-pln 參數計算總 PLN")

if __name__ == "__main__":
    main()