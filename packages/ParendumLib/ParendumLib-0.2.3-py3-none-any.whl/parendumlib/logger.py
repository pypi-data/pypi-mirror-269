import threading
import requests
import logging
import hashlib
import inspect
import hmac
import time


class Logger:

    def __init__(self, domain: str, api_key: str, api_secret: str, port: int = 443, log_file: str = None):
        self.protocol = "https" if port == 443 else "http"
        self.endpoint = f"{self.protocol}://{domain}:{port}"
        self.api_key = api_key
        self.api_secret = api_secret.encode()
        self.pending = list()
        self._start_thread()

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        if log_file:
            self.file_handler = logging.FileHandler(log_file)
            self.file_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.file_handler)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)

    def _start_thread(self):
        thread = threading.Thread(target=self._send_pending)
        thread.start()

    def _send_pending(self):
        while True:
            if self.pending:
                _pending = self.pending.pop()
                try:
                    self._log(*_pending)
                    time.sleep(100)
                except:
                    time.sleep(500)
            time.sleep(500)

    def _generate_signature(self, timestamp: str) -> str:
        """
        Generate HMAC signature using the provided timestamp.

        Args:
            timestamp (str): The timestamp to be used in signature generation.

        Returns:
            str: The generated HMAC signature.
        """
        return hmac.new(self.api_secret, timestamp.encode(), digestmod=hashlib.sha256).hexdigest()

    def _get_hmac_headers(self) -> dict:
        """
        Generate the HMAC headers required for API requests.

        Returns:
            dict: A dictionary containing the required headers.
        """
        timestamp = str(int(time.time()))
        return {
            "X-Signature": self._generate_signature(timestamp),
            "X-Timestamp": timestamp,
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _do_post(self, url: str, body: dict = None) -> dict:
        """
        Make a POST request to the specified URL.

        Args:
            url (str): The URL to make the request to.
            body (dict, optional): The body of the request. Defaults to None.

        Returns:
            dict: The API response.
        """
        try:
            response = requests.request("POST", url, headers=self._get_hmac_headers(), json=body, timeout=2)
            if response.status_code == 200:
                return response.json()
            return dict(code=response.status_code, error=response.json())
        except Exception as e:
            return dict(code=500, error=str(e))

    def _log(self, level: str, function: str, message: str, status_code: int, elapsed_time: int = 1,
             arguments: list = None, content: dict = None, save: bool = False):
        _new_log = dict(
            function=function,
            message=message,
            level=level.lower(),
            status_code=status_code or 0,
            elapsed_time=elapsed_time
        )
        if arguments:
            _new_log["arguments"] = arguments
        if content:
            _new_log["content"] = content
        if save:
            self._do_post(f"{self.endpoint}/api/logs/new", _new_log)

    def _do_log(self, level: str, function: str, message: str, status_code: int, elapsed_time: int = 1,
                arguments: list = None, content: dict = None, save: bool = False):
        if save:
            self.pending.append([level, function, message, status_code, elapsed_time, arguments, content, save])
        if hasattr(self.logger, level):
            getattr(self.logger, level)(f"[{function}] {message}")
        else:
            self.logger.info(f"[{level}:{function}] {message}")

    def log(self, level: str, message: str, status_code: int = 0, save: bool = False):
        stack = inspect.stack()
        caller_info = stack[1]
        caller_name = caller_info.function
        caller_line_no = caller_info.lineno
        self._do_log(level, f"{caller_name}():{caller_line_no}", message, status_code, save=save)

    def success(self, message: str, status_code: int = 0, save: bool = False):
        stack = inspect.stack()
        caller_info = stack[1]
        caller_name = caller_info.function
        caller_line_no = caller_info.lineno
        self._do_log('success', f"{caller_name}():{caller_line_no}", message, status_code, save=save)

    def debug(self, message: str, status_code: int = 100, save: bool = False):
        stack = inspect.stack()
        caller_info = stack[1]
        caller_name = caller_info.function
        caller_line_no = caller_info.lineno
        self._do_log('debug', f"{caller_name}():{caller_line_no}", message, status_code, save=save)

    def info(self, message: str, status_code: int = 200, save: bool = False):
        stack = inspect.stack()
        caller_info = stack[1]
        caller_name = caller_info.function
        caller_line_no = caller_info.lineno
        self._do_log('info', f"{caller_name}():{caller_line_no}", message, status_code, save=save)

    def warning(self, message: str, status_code: int = 400, save: bool = False):
        stack = inspect.stack()
        caller_info = stack[1]
        caller_name = caller_info.function
        caller_line_no = caller_info.lineno
        self._do_log('warning', f"{caller_name}():{caller_line_no}", message, status_code, save=save)

    def error(self, message: str, status_code: int = 500, save: bool = False):
        stack = inspect.stack()
        caller_info = stack[1]
        caller_name = caller_info.function
        caller_line_no = caller_info.lineno
        self._do_log('error', f"{caller_name}():{caller_line_no}", message, status_code, save=save)

    def exception(self, message: str, status_code: int = 600, save: bool = False):
        stack = inspect.stack()
        caller_info = stack[1]
        caller_name = caller_info.function
        caller_line_no = caller_info.lineno
        self._do_log('exception', f"{caller_name}():{caller_line_no}", message, status_code, save=save)
