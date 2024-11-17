"""
This Python code shows how to post on Bluesky using hashtags that can be linked.
"""

import re
from atproto import Client, models


class BlueSky:
    def __init__(self, user: str, password: str):
        self.client = Client()
        self.client.login(user, password)

    def publish(self, text: str):
        facets: list[models.AppBskyRichtextFacet.Main] = []
        hashtags = re.finditer(r'#\w+', text)
        for match in hashtags:
            byte_start = match.regs[0][0]
            byte_end = match.regs[0][1]
            tag = match.string[byte_start+1:byte_end]  # We have to remove the hash character
            m = models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Tag(
                    tag=tag
                )],
                index=models.AppBskyRichtextFacet.ByteSlice(
                    byteStart=byte_start,
                    byteEnd=byte_end
                )
            )
            facets.append(m)
        post = self.client.send_post(text=text, facets=facets)
        return post


if __name__ == "__main__":
    b = BlueSky(user='your_user_name.bsky.social', password='some_very_strong_password')
    b.publish("A #post #with #some #tags")
