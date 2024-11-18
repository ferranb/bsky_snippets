"""
This Python code shows how to post on Bluesky using hashtags that can be linked. 
The code handles Unicode characters within the string
"""

import re
from atproto import Client, models


def idx_from_str_to_byte(text: str, idx: int) -> int:
    idx_byte = 0
    for i in range(0, idx):
        c = text[i]
        c_unicode = c.encode('utf-8')
        idx_byte += len(c_unicode)
    return idx_byte


class BlueSky:
    def __init__(self, user: str, password: str):
        self.client = Client()
        self.client.login(user, password)

    def publish(self, text: str):
        facets: list[models.AppBskyRichtextFacet.Main] = []
        hashtags = re.finditer(r'#\w+', text, re.DOTALL)
        for match in hashtags:
            idx_start = match.regs[0][0]
            idx_end = match.regs[0][1]
            tag = match.string[idx_start+1:idx_end]  # We have to remove the hash character
            m = models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Tag(
                    tag=tag
                )],
                index=models.AppBskyRichtextFacet.ByteSlice(
                    byteStart=idx_from_str_to_byte(text, idx_start),
                    byteEnd=idx_from_str_to_byte(text, idx_end),
                )
            )
            facets.append(m)
        post = self.client.send_post(text=text, facets=facets)
        return post
