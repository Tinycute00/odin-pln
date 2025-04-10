# Odin PLN Calculator API Documentation

This document describes the main API and usage methods for the Odin PLN calculator.

## OdinPLNCalculator Class

`OdinPLNCalculator` is the main calculator class, providing the following key methods:

### `calculate_token_pln(user_id, token_id, time_range_days=30)`

Calculates PLN data for a specified user and token.

**Parameters:**
- `user_id` (str): User ID
- `token_id` (str): Token ID
- `time_range_days` (int, optional): Calculation time range in days. Default is 30 days.

**Returns:**
A dictionary containing the following fields:
- `realized_pln`: Realized PLN in satoshis
- `unrealized_pln`: Unrealized PLN in satoshis
- `total_pln`: Total PLN in satoshis
- `yield_rate`: Yield rate as a percentage
- `current_value`: Current value in satoshis
- `current_holdings`: Current number of tokens held

### `get_formatted_token_pln(user_id, token_id, time_range_days=30)`

Gets formatted PLN results for easy display.

**Parameters:**
- Same as `calculate_token_pln`

**Returns:**
A dictionary containing the following fields:
- `success`: Whether calculation was successful
- `realized_pln`: Realized PLN, formatted as BTC
- `unrealized_pln`: Unrealized PLN, formatted as BTC
- `total_pln`: Total PLN, formatted as BTC
- `yield_rate`: Yield rate, formatted as percentage
- `current_value`: Current value, formatted as BTC
- `current_holdings`: Current number of tokens held
- `time_range`: Time range, formatted in days

### `calculate_total_pln(user_id, time_range_days=30, top_n=5)`

Calculates total PLN for all tokens a user holds.

**Parameters:**
- `user_id` (str): User ID
- `time_range_days` (int, optional): Calculation time range in days. Default is 30 days.
- `top_n` (int, optional): Calculate the top N most active tokens. Default is 5.

**Returns:**
A dictionary containing the following fields:
- `total_pln`: Total PLN in satoshis
- `yield_rate`: Yield rate as a percentage
- `token_count`: Number of tokens calculated

## Example

```python
from odin_pln import OdinPLNCalculator

# Initialize calculator
calculator = OdinPLNCalculator()

# Calculate and format PLN results
user_id = "user123"
token_id = "token456"
result = calculator.get_formatted_token_pln(user_id, token_id, time_range_days=30)

# Display results
if result["success"]:
    print(f"Total PLN: {result['total_pln']}")
    print(f"Yield Rate: {result['yield_rate']}")
else:
    print(f"Calculation failed: {result['error']}")
```

---

# Odin PLN 計算器 API 文檔

此文檔描述 Odin PLN 計算器的主要 API 和使用方法。

## OdinPLNCalculator 類

`OdinPLNCalculator` 是主要的計算器類，提供以下主要方法：

### `calculate_token_pln(user_id, token_id, time_range_days=30)`

計算指定用戶和代幣的 PLN 數據。

**參數:**
- `user_id` (str): 用戶 ID
- `token_id` (str): 代幣 ID
- `time_range_days` (int, 可選): 計算時間範圍，單位為天。默認為 30 天。

**返回:**
包含以下字段的字典：
- `realized_pln`: 已實現 PLN，單位為聰 (satoshi)
- `unrealized_pln`: 未實現 PLN，單位為聰
- `total_pln`: 總 PLN，單位為聰
- `yield_rate`: 收益率，百分比
- `current_value`: 當前價值，單位為聰
- `current_holdings`: 當前持有的代幣數量

### `get_formatted_token_pln(user_id, token_id, time_range_days=30)`

獲取格式化的 PLN 結果，方便顯示。

**參數:**
- 與 `calculate_token_pln` 相同

**返回:**
包含以下字段的字典：
- `success`: 是否成功計算
- `realized_pln`: 已實現 PLN，格式化為 BTC
- `unrealized_pln`: 未實現 PLN，格式化為 BTC
- `total_pln`: 總 PLN，格式化為 BTC
- `yield_rate`: 收益率，格式化為百分比
- `current_value`: 當前價值，格式化為 BTC
- `current_holdings`: 當前持有的代幣數量
- `time_range`: 時間範圍，格式化為天

### `calculate_total_pln(user_id, time_range_days=30, top_n=5)`

計算用戶所有代幣的總 PLN。

**參數:**
- `user_id` (str): 用戶 ID
- `time_range_days` (int, 可選): 計算時間範圍，單位為天。默認為 30 天。
- `top_n` (int, 可選): 計算前 N 個最活躍的代幣。默認為 5。

**返回:**
包含以下字段的字典：
- `total_pln`: 總 PLN，單位為聰
- `yield_rate`: 收益率，百分比
- `token_count`: 計算的代幣數量

## 示例

```python
from odin_pln import OdinPLNCalculator

# 初始化計算器
calculator = OdinPLNCalculator()

# 計算並格式化 PLN 結果
user_id = "user123"
token_id = "token456"
result = calculator.get_formatted_token_pln(user_id, token_id, time_range_days=30)

# 顯示結果
if result["success"]:
    print(f"總 PLN: {result['total_pln']}")
    print(f"收益率: {result['yield_rate']}")
else:
    print(f"計算失敗: {result['error']}")
```