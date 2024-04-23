import shutil
import tempfile
from typing import Dict, Optional

import requests  # pip install requests
from tqdm import tqdm


class RequestsTqdm:
    """
    A class combining requests and tqdm for downloading files with progress tracking.

    Attributes:
        session (requests.Session): A session object for making HTTP requests.
        tmp_file (str): Path to the temporary file used during download.
        output_path (str): Path where the downloaded file is saved.

    Usage:
    ```python
    downloader = RequestsTqdm()
    downloader.get('http://example.com/file.zip', output_file='file.zip')
    ```
    """

    def __init__(self):
        """
        Initializes the RequestsTqdm object with an HTTP session, and paths for temporary and output files.
        """
        self.session = requests.Session()
        self.tmp_file: str = ""
        self.output_path: str = ""
        self._bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]"

    def get(self, url: str, **kwargs):
        """
        Downloads a file from the specified URL using an HTTP GET request.

        Args:
            url (str): The URL of the file to download.
            **kwargs: Additional keyword arguments to be passed to the requests.get function.
                - output_file (str): Path where the downloaded file should be saved.

        Returns:
            requests.Response: The response object returned by the GET request.

        Usage:
        ```python
        downloader.get('http://example.com/file.zip', output_file='file.zip')
        ```
        """
        output_file = kwargs.pop("output_file")
        response = self.session.get(url, stream=True, **kwargs)
        return self._process_response(response, output_file)

    def post(self, url: str, data: Dict = None, **kwargs):
        """
        Sends a POST request to the specified URL.

        Args:
            url (str): The URL to which the POST request will be sent.
            data (Dict): The data to be sent in the request body.
            **kwargs: Additional keyword arguments to be passed to the requests.post function.
                - output_file (str): Path where the downloaded file should be saved.

        Returns:
            requests.Response: The response object returned by the POST request.

        Usage:
        ```python
        downloader.post('http://example.com/upload', data={'key': 'value'}, output_file='response.json')
        ```
        """
        output_file = kwargs.pop("output_file")
        response = self.session.post(url, data=data, **kwargs)
        return self._process_response(response, output_file)

    def _process_response(self, response: requests.Response, output_file: Optional[str] = None):
        """
        Processes the HTTP response, writes the content to a temporary file, and moves it to the output file path.

        Args:
            response (requests.Response): The HTTP response object.
            output_file (Optional[str]): Path where the downloaded file should be saved.

        Returns:
            requests.Response: The input response object.

        Raises:
            Exception: If the output file path is not provided or does not exist.

        Usage:
        This method is intended for internal use within the class.
        """
        if not output_file:
            delete_tmp_file = True
        # elif not os.path.exists(output_file):
        #    raise Exception(f"Output file '{output_file}' does not exist.")
        else:
            delete_tmp_file = False

        if response.status_code < 300:
            print(f"Request suceeded with status {response.status_code}.")

        else:
            print(f"Request failed with status {response.status_code}.")

        total_size = int(response.headers.get("content-length", 0))
        bytes_received = 0

        with tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            # bar_format=self._bar_format,
        ) as progress_bar:
            with tempfile.NamedTemporaryFile(delete=delete_tmp_file) as tmp_file:
                self.tmp_file = tmp_file.name
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        tmp_file.write(chunk)
                        bytes_received += len(chunk)
                        progress_bar.update(len(chunk))

                # Move the file cursor to the beginning
                tmp_file.seek(0)

                # Read and print a preview of the file content
                try:
                    preview_content = tmp_file.read(1024).decode(
                        "utf-8"
                    )  # Adjust the number of bytes to read as desired
                    self._file_prev_ = f"Preview of file content:\n" + preview_content
                except Exception as e:
                    # codec can't decode byte 0xff in position 0:
                    self._file_prev_ = (
                        f"Preview of file content:\n"
                        + "[WARN] content not showing up as not decodable under utf-8"
                    )

        if output_file:
            shutil.move(self.tmp_file, output_file)
            self.output_path = output_file

        print("Download complete!")

        return response


def test_custom_req():
    # Example usage
    custom_request = RequestsTqdm()

    # GET request
    custom_request.get("https://example.com/file.txt")

    # POST request
    data = {"param1": "value1", "param2": "value2"}
    custom_request.post("https://example.com/submit", data=data)


if __name__ == "__main__":
    test_custom_req()
