# Odin PLN Calculator

A PLN (Profit/Loss Net) calculation tool for analyzing token trading performance on the Odin platform, suitable for Web3 users.

## Features

- Calculate PLN (Profit/Loss Net) for a single token
- Calculate total PLN for all tokens a user holds
- Analyze realized and unrealized profits/losses
- Smart caching system for improved calculation efficiency
- Support for custom time ranges (7/14/30/90/120 days)

## Installation and Setup

1. Ensure Python 3.6 or higher is installed
2. Clone this repository:
   ```
   git clone https://github.com/Tinycute00/odin-pln.git
   cd odin-pln
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line Arguments

```
python odin_pln.py [options]
```

Options:
- `--user <user_id>` - Specify the user ID for PLN calculation
- `--token <token_id>` - Specify the token ID to calculate
- `--days <number>` - Specify the day range for calculation (default: 30, options: 7, 14, 30, 90, 120)
- `--total-pln` - Calculate total PLN for all tokens
- `--top-tokens <number>` - Specify how many of the most active tokens to calculate (default: 5)

### Examples

1. Calculate PLN for a specific user and token:
   ```
   python odin_pln.py --user vj5mg-hquhw-x2amt-ukf2l-zgnjw-bbsac-s35gm-pycq6-fzuny-v6e7g-2ae --token 2933 --days 30
   ```

2. Calculate total PLN for a user (all tokens):
   ```
   python odin_pln.py --user vj5mg-hquhw-x2amt-ukf2l-zgnjw-bbsac-s35gm-pycq6-fzuny-v6e7g-2ae --total-pln --days 30
   ```

## PLN Calculation Method

PLN (Profit/Loss Net) calculation is based on the following principles:

- **Realized PLN**: Profit/loss from completed transactions (bought and then sold)
- **Unrealized PLN**: The difference between the current value of holdings and their cost
- **Total PLN**: Sum of realized PLN and unrealized PLN

The calculation uses the average cost method to handle buy and sell records.

## Development and Extensions

To extend functionality, you can modify the following parts:

- Add new API endpoint connections
- Implement additional transaction data analysis functions
- Extend time range options
- Add graphical visualization features

## License

MIT

---

# Odin PLN 計算器

這是一個用於分析 Odin 平台上代幣交易表現的 PLN (Profit/Loss Net) 計算工具，適用於 Web3 用戶。

## 功能特點

- 計算單一代幣的 PLN（盈虧淨值）
- 計算用戶所有代幣的總 PLN
- 分析已實現和未實現的盈虧
- 智能緩存系統，提高計算效率
- 支持自定義時間範圍（7/14/30/90/120天）

## 安裝與設置

1. 確保已安裝 Python 3.6 或更高版本
2. 克隆此代碼庫：
   ```
   git clone https://github.com/Tinycute00/odin-pln.git
   cd odin-pln
   ```
3. 安裝依賴：
   ```
   pip install -r requirements.txt
   ```

## 使用方法

### 命令行參數

```
python odin_pln.py [選項]
```

選項：
- `--user <用戶ID>` - 指定要計算 PLN 的用戶 ID
- `--token <代幣ID>` - 指定要計算的代幣 ID
- `--days <天數>` - 指定計算的天數範圍（默認：30，可選值：7, 14, 30, 90, 120）
- `--total-pln` - 計算所有代幣的總 PLN
- `--top-tokens <數量>` - 指定計算多少個最活躍的代幣（默認：5）

### 示例

1. 計算特定用戶特定代幣的 PLN：
   ```
   python odin_pln.py --user vj5mg-hquhw-x2amt-ukf2l-zgnjw-bbsac-s35gm-pycq6-fzuny-v6e7g-2ae --token 2933 --days 30
   ```

2. 計算用戶的總 PLN（所有代幣）：
   ```
   python odin_pln.py --user vj5mg-hquhw-x2amt-ukf2l-zgnjw-bbsac-s35gm-pycq6-fzuny-v6e7g-2ae --total-pln --days 30
   ```

## PLN 計算方法

PLN（Profit/Loss Net）計算基於以下原則：

- **已實現 PLN**：已完成的交易（買入後賣出）產生的盈虧
- **未實現 PLN**：當前持有的資產與其成本之間的差額
- **總 PLN**：已實現 PLN 和未實現 PLN 的總和

計算採用平均成本法處理買入和賣出記錄。

## 開發與擴展

如需擴展功能，可以修改以下部分：

- 添加新的 API 端點連接
- 實現額外的交易數據分析功能
- 擴展時間範圍選項
- 添加圖形化展示功能

## 許可證

MIT