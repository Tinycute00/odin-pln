"""
API Utilities for Odin PLN Calculator
-------------------------------------
Utility functions for making API requests with retry logic.

Odin PLN 計算器的 API 工具
------------------------
帶有重試邏輯的 API 請求工具函數。
"""

import requests
import json
import logging
import time
from typing import Dict, Any, Optional

# Get logger instance | 獲取日誌實例
logger = logging.getLogger('Odin_PLN_Calculation')

def make_api_request(url: str, params: Dict[str, Any] = None, max_retries: int = 3, retry_delay: int = 2) -> Optional[Dict[str, Any]]:
    """
    Make API request with retry mechanism
    
    Args:
        url: API endpoint URL
        params: Query parameters
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries (seconds)
        
    Returns:
        Response data or None if request fails
        
    帶有重試機制的 API 請求工具函數
    
    參數:
        url: API 端點 URL
        params: 查詢參數
        max_retries: 最大重試次數
        retry_delay: 重試延遲（秒）
        
    返回:
        響應數據或 None（如果請求失敗）
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed (attempt {attempt+1}/{max_retries}): {e}")
            logger.warning(f"請求失敗 (嘗試 {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                logger.info(f"Waiting {retry_delay} seconds before retrying...")
                logger.info(f"等待 {retry_delay} 秒後重試...")
                time.sleep(retry_delay)
                # Increase retry delay (exponential backoff)
                # 增加重試延遲（指數退避）
                retry_delay *= 2
            else:
                logger.error(f"Maximum retry attempts reached, abandoning request: {url}")
                logger.error(f"達到最大重試次數，放棄請求: {url}")
                return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            logger.error(f"JSON 解析錯誤: {e}")
            return None
    
    return None