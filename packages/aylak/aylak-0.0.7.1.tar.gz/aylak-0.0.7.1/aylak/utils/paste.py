import traceback
from typing import Any, Dict, Union

import aiohttp
import requests


class Paste:
    def __init__(self):
        self.paste_url = "http://basicbots.pw:7070/create_paste/"
        self.get_paste_url = "http://basicbots.pw:7070/get_paste/"
        self.headers = {"Content-Type": "application/json"}

    async def aio_paste(
        self,
        content: str,
        language: str = "python",
        paste_by: str = "",
        title: str = "",
        return_url: bool = True,
        trace: bool = False,
    ) -> Union[str, None, Exception]:
        payload = {
            "content": content,
            "language": language,
            "paste_by": paste_by,
            "title": title,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.paste_url, json=payload, headers=self.headers
                ) as response:
                    paste_id = (await response.json())["paste_id"]
                    if return_url:
                        return f"http://basicbots.pw:7070/get_paste/{paste_id}"
                    return paste_id
        except Exception as e:
            trace = traceback.format_exc()
            if trace:
                return trace
            return e

    async def aio_get_paste(
        self, paste_id: str, trace: bool = False
    ) -> Union[Dict[str, Any], None, Exception]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.get_paste_url}{paste_id}") as response:
                    return await response.json()
        except Exception as e:
            trace = traceback.format_exc()
            if trace:
                return trace
            return e

    def paste(
        self,
        content: str,
        language: str = "python",
        paste_by: str = "",
        title: str = "",
        return_url: bool = True,
        trace: bool = False,
    ) -> Union[str, None, Exception]:
        payload = {
            "content": content,
            "language": language,
            "paste_by": paste_by,
            "title": title,
        }
        try:
            response = requests.post(self.paste_url, json=payload, headers=self.headers)
            if response.status_code != 200:
                return None
            paste_id = response.json()["paste_id"]
            if return_url:
                return f"http://basicbots.pw:7070/get_paste/{paste_id}"
            return paste_id
        except Exception as e:
            trace = traceback.format_exc()
            if trace:
                return trace
            return e

    def get_paste(
        self, paste_id: str, trace: bool = False
    ) -> Union[Dict[str, Any], None, Exception]:
        try:
            response = requests.get(f"{self.get_paste_url}{paste_id}")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            trace = traceback.format_exc()
            if trace:
                return trace
            return e


paste = Paste()

__all__ = ["paste"]
