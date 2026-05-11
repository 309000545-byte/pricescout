"""
HTTP客户端
封装requests库,提供统一的HTTP请求接口
"""
import requests
import random
import time
from typing import Optional, Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HTTPClient:
    """HTTP客户端"""

    def __init__(self, timeout: int = 10, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = self._create_session()
        self.request_count = 0

        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]

    def _create_session(self) -> requests.Session:
        """创建会话,配置重试策略"""
        session = requests.Session()

        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _get_random_user_agent(self) -> str:
        """获取随机User-Agent"""
        return random.choice(self.user_agents)

    def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, str]] = None
    ) -> Optional[str]:
        """
        GET请求

        Args:
            url: 请求URL
            headers: 请求头
            params: 查询参数
            cookies: Cookies

        Returns:
            响应文本内容,失败返回None
        """
        if headers is None:
            headers = {}

        headers['User-Agent'] = self._get_random_user_agent()

        try:
            response = self.session.get(
                url,
                headers=headers,
                params=params,
                cookies=cookies,
                timeout=self.timeout
            )

            response.raise_for_status()

            self.request_count += 1

            if self.request_count > 1:
                time.sleep(random.uniform(1, 3))

            return response.text

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {url} - {str(e)}")
            return None

    def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Optional[str]:
        """
        POST请求

        Args:
            url: 请求URL
            data: 表单数据
            json: JSON数据
            headers: 请求头

        Returns:
            响应文本内容,失败返回None
        """
        if headers is None:
            headers = {}

        headers['User-Agent'] = self._get_random_user_agent()

        try:
            response = self.session.post(
                url,
                data=data,
                json=json,
                headers=headers,
                timeout=self.timeout
            )

            response.raise_for_status()

            self.request_count += 1

            return response.text

        except requests.exceptions.RequestException as e:
            print(f"POST请求失败: {url} - {str(e)}")
            return None

    def download_file(self, url: str, file_path: str) -> bool:
        """
        下载文件

        Args:
            url: 文件URL
            file_path: 保存路径

        Returns:
            是否成功
        """
        try:
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            return True

        except Exception as e:
            print(f"文件下载失败: {url} - {str(e)}")
            return False

    def close(self):
        """关闭会话"""
        if self.session:
            self.session.close()

    def get_request_count(self) -> int:
        """获取请求计数"""
        return self.request_count

    def reset_count(self):
        """重置请求计数"""
        self.request_count = 0
