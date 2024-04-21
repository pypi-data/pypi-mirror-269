#  エラー処理を行う関数を定義するモジュール

class ErrorPrint:
    """
    error_print: error message print function
    """
    def __init__(self):
        pass

    @staticmethod
    def handle_http_error(response):
        """
        Handles errors in HTTP responses.

        Parameters:
            response: response object

        Return value:
            bool: True if an error occurs, otherwise False
        """
        if response.status_code ==  200:
            #  200 OKの処理
            return False
        if response.status_code ==  404:
            #  404エラーの処理
            raise APIResponseException("404 Not Found error\nリクエストされたリソースが見つかりませんでした")
        elif response.status_code ==  403:
            #  403エラーの処理
            raise APIResponseException("403 Forbidden error\nアクセスが拒否されました")
        elif response.status_code ==  400:
            #  400エラーの処理
            raise APIResponseException(f"400 Bad Request error\n{response.json()['body']}\nAPIリクエストが不正です")

class APIResponseException(Exception):
    pass