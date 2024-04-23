#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Hermann Agossou"

"""
Mimic Curl

This script is a Python version of curl, which allows you to make HTTP requests from the command line.

Usage:
$ # GET request
$ python curl.py https://jsonplaceholder.typicode.com/posts/1
$ # POST request
$ python curl.py -X POST https://jsonplaceholder.typicode.com/posts/ -d "userId:4"
$ # download a file (or put the content of the response in a file)
$ python curl.py -X POST https://jsonplaceholder.typicode.com/posts/ -d "userId:4" -o json
$ python curl.py https://google.com -o html

Author:
Hermann Agossou

"""

import argparse

from curl.core import CurlRequest


def get_parser():
    """
    Returns the argument parser for the curl script
    """
    parser = argparse.ArgumentParser(description="Python version of curl")
    parser.add_argument(
        "url",
        type=str,
        help="The URL to make a request to:::ex: https://jsonplaceholder.typicode.com/posts/1",
    )
    parser.add_argument(
        "-X",
        "--request",
        type=str,
        choices=["GET", "POST"],
        default="GET",
        help="The HTTP request method to use. default=GET",
    )
    parser.add_argument(
        "-H",
        "--header",
        action="append",
        default=[],
        help='Additional headers to include in the request, can be specified multiple times:::ex: -H "ttt: 449" -H "eee: 745"',
    )
    parser.add_argument(
        "-d",
        "--data",
        type=str,
        help='Data to send in the request body:::ex: -d "ttt:444; l:789" with space after the ";"',
    )
    parser.add_argument(
        "-b",
        "--cookie",
        type=str,
        help='Cookie string to send in the request header:::ex: -c "ttt=444; l=789"',
    )
    parser.add_argument(
        "-l",
        "--level",
        type=int,
        choices=[1, 2, 3, 4],
        default=1,
        help="Integer for the response level.default=1. 1 show the response, 2 adds res.header, 3 adds res.cookies, 4 adds res.others",
    )
    parser.add_argument("-o", type=str, help="Output file path; the parent folder should exists")
    parser.add_argument("-e", type=str, help="Output file extension:::ex: -e json")
    parser.add_argument(
        "-O",
        action="store_true",
        help='Use auto-generated output file name: will use fname from url or "output"',
    )
    parser.add_argument(
        "-s", "--stringify", action="store_true", help="Stringify the request body as JSON"
    )

    return parser.parse_args()


def main():
    args = get_parser()
    handle_curl = CurlRequest(args)
    _ = handle_curl.get_res()
    handle_curl.show_res()


if __name__ == "__main__":
    main()
