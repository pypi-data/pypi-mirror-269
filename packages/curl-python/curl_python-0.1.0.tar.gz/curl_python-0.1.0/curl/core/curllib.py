import json
import os.path
from typing import Optional

from .requestslib import RequestsTqdm


def create_parent_dir(file_path):
    # Extract the directory path
    parent_dir = os.path.dirname(file_path)

    # Check if the directory exists, if not, create it
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)


class CurlRequest:
    """
    A class mimicking curl functionality using Python's requests module (customizable headers, cookies, and data, and displaying responses) with tqdm for progress tracking.

    Attributes:
        args: The arguments passed to the request handler (for example, command-line arguments).
        request_method (str): The HTTP request method (e.g., 'GET' or 'POST').
        level (int): The verbosity level for logging.
        header (list): A list of headers for the request.
        cookie (str): A string representing cookies for the request.
        url (str): The URL for the request.
        data (str): The body of the request.
        custom_request (RequestsTqdm): An instance of RequestsTqdm for making HTTP requests with progress tracking.
        result: The result of the HTTP request.

    Usage:
    ```python
    handler = CurlRequest(args)
    handler.get_res()
    handler.show_res()
    ```

    ```python
    import argparse

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="A tool mimicking curl functionality using Python.")
    parser.add_argument("request", help="HTTP request method (GET or POST).")
    # Add more arguments as needed (url, header, cookie, data, level)
    args = parser.parse_args()

    # Create CurlLikeRequest object
    curl_request = CurlLikeRequest(args)

    # Send request and display result
    curl_request.get_res()
    curl_request.show_res()
    ```
    """

    response_attributes_to_show = [
        "elapsed",
        "encoding",
        "headers",
        "history",
        "is_permanent_redirect",
        "is_redirect",
        "links",
        "next",
        "ok",
        "reason",
    ]

    def __init__(self, args):
        """
        Initializes the CurlRequest object with parsed command-line arguments.

        Args:
            args: Parsed command-line arguments.
        """
        self.args = args
        self.request_method = args.request.upper()
        self.level = args.level
        self.header = args.header
        self.cookie = args.cookie
        self.url = args.url
        self.data = args.data
        self.custom_request = RequestsTqdm()
        self.result = None

    def get_headers(self):
        """
        Returns the headers for the request.

        Returns:
            dict: A dictionary containing headers.

        Usage:
        This method is intended to be used internally within the class.
        """
        level = self.level
        headers = {}
        for header in self.header:
            key, value = header.split(": ")
            headers[key] = value
        if level >= 2:
            print("headers = ", headers)
        return headers

    def get_cookies(self):
        """
        Returns the cookies for the request.

        Returns:
            dict: A dictionary containing cookies.

        Usage:
        This method is intended to be used internally within the class.
        """
        level = self.level
        cookies = {}
        if self.cookie:
            cookie_parts = self.cookie.split("; ")
            for cookie_part in cookie_parts:
                key, value = cookie_part.split("=")
                cookies[key] = value
        if level >= 2:
            print("cookies = ", cookies)
        return cookies

    def get_data(self):
        """
        Returns the body for the request.

        Returns:
            str or dict: The body of the request.

        Usage:
        This method is intended to be used internally within the class.
        """
        level = self.level
        body = {}
        if self.data:
            body_parts = self.data.split("; ")
            for body_part in body_parts:
                key, value = body_part.split(":")
                body[key] = value

        if self.args.stringify:
            # Stringify the body object
            body_string: str = json.dumps(body)
        else:
            # Use the body object as is
            body_string: dict = body

        if level >= 2:
            print("body = ", body_string)
        return body_string

    def get_output_filename(self):
        """
        Returns the output filename based on the -o option or None if not specified.

        Returns:
            str or None: The output filename or None if not specified.

        Usage:
        This method is intended to be used internally within the class.
        """
        if self.args.o:
            return self.args.o

        if not self.args.O:
            return None

        # parse extension
        ext = ""  # no extension by default
        if self.args.e:
            ext = self.args.e
            if not ext.startswith("."):
                ext = "." + ext

        url_parts = self.url.split("/")
        filename = url_parts[-1] if url_parts[-1] else "output"
        return filename + ext

    def get_res(self):
        """
        Sends the request and returns the result.

        Returns:
            object: The result of the HTTP request.

        Usage:
        This method is intended to be used internally within the class.
        """
        headers = self.get_headers()
        cookies = self.get_cookies()
        data = self.get_data()
        url = self.url
        request_method = self.request_method

        result = None
        output_filename = self.get_output_filename()
        create_parent_dir(output_filename)

        if output_filename:
            print(f"response will be saved to file: {os.path.abspath(output_filename)}")

        print("sending request ...")

        try:
            if request_method == "GET":
                result = self.custom_request.get(
                    url, headers=headers, cookies=cookies, output_file=output_filename
                )
            elif request_method == "POST":
                result = self.custom_request.post(
                    url, headers=headers, cookies=cookies, data=data, output_file=output_filename
                )
            else:
                print(f"request_method not recognized. found request_method={request_method}")
                return None

            result.output_filename = self.custom_request.output_path
            result.file_prev_str = self.custom_request._file_prev_

            self.result = result

            return result

        except Exception as e_:
            print(e_)
            print("Connection refused. The server may be down or busy.")
            raise

    def show_res(self, level: Optional[int] = None, show_content: bool = True):
        """
        Displays the response from the HTTP request.

        Args:
            level (Optional[int]): The verbosity level for logging.
            show_content (bool): Whether to show the content of the response.

        Usage:
        This method is intended to be used internally within the class.
        """
        if level is None:
            level = self.level
        if self.result is None:
            self.get_res()
        response = self.result

        if response is None:
            return
        if level >= 2:
            print(2 * "\n----------------------------")

        if level >= 2:
            print(f">>> url: {response.url}")

        print(f">>> status_code: {response.status_code}")

        if level >= 3:
            print("\n>>> headers >>>")
            for key, val in response.headers.items():
                print(f"  {key}: {val}")

        if level >= 2:
            print("\n>>> cookies >>>")
            for key, val in response.cookies.items():
                print(f"  {key}: {val}")

        if level >= 4:
            print("\n>>> others >>>")
            for att in self.response_attributes_to_show:
                if "header" in att:
                    continue
                print(f"  {att}: {getattr(response, att)}")

        if level >= 1 and show_content:
            if level >= 2:
                print("\n>>> response >>>")
            print(response.file_prev_str)

        if level >= 2:
            print(2 * "----------------------------\n")
