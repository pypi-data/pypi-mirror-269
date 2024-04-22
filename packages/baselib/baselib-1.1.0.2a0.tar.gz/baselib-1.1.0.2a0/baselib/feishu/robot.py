"""
https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot#f62e72d5
"""
import requests
import json


class FeishuRobot(object):

    def __init__(self, token, debug=True):
        self.token = token
        self.url = f"https://open.feishu.cn/open-apis/bot/v2/hook/{token}"
        self.debug = debug

    def _send(self, data: dict, headers: dict = None):
        headers = self.common_headers(headers)
        if self.debug:
            print(f'[url]{self.url}')
            print(f'[headers]{headers}')
            print(f'[data]{data}')
        response = requests.post(self.url, headers=headers, json=data)
        # if response.status_code == 200:
        #     print("消息发送成功")
        # else:
        #     print("消息发送失败")
        if self.debug:
            print(f"[rsp]{response.text}")
        return json.loads(str(response.text))

    def common_headers(self, headers=None):
        if headers is None:
            headers = {}
        headers['Content-Type'] = headers.get(
            'Content-Type', 'application/json')
        return headers

    def get_username_by_id(self, user_id):
        return user_id

    def send_text(self, content, at_list=None):
        """ 发送文本消息
        :param content:
        :param at_list:
        :return:
        """
        if at_list is None:
            at_list = []
        at_msg_list = []
        for user_id in at_list:
            user_name = self.get_username_by_id(user_id)
            at_msg_list.append(f'<at user_id="{user_id}>{user_name}</at>"')
        at_msg_msg = ",".join(at_msg_list)
        data = {
            "msg_type": "text",
            "content": {
                "text": f"{content}{at_msg_msg}"
            }
        }
        return self._send(data)

    def send_post(self, title, content):
        """ 发送富文本
        :param title:
        :param content: 二维字典列表，富文本消息内容。由多个段落组成，每个段落为一个[]节点，其中包含若干个节点。
            content = [
                [
                    dict(tag="text", text="项目有更新:"),
                    dict(tag="a", text="请查看", href="http://www.example.com/"),
                    dict(tag="at", user_id="oui_xxxxxx")
                ],
                [],
            ]
            上述的标签tag，支持：
            - text： 文本
            - a: 超链接
            - img: 图片
            - at: @相关人
        :return:
        """
        if content and not isinstance(content[0], list):
            content = [content]
        data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": content
                    }
                }
            }
        }
        return self._send(data)

    def send_share_chat(self, share_chat_id):
        """ 发送群名片
        :param share_chat_id: 群 ID。获取方式请参见 群 ID 说明。
        :return:
        """
        data = {
            "msg_type": "share_chat",
            "content": {
                "share_chat_id": share_chat_id
            }
        }
        return self._send(data)

    def send_img(self, image_key):
        """ 发送图片
        :param image_key: 图片Key。可通过 上传图片 接口获取 image_key。
        :return:
        """
        data = {
            "msg_type": "image",
            "content": {
                "image_key": image_key
            }
        }
        return self._send(data)

    def send_card(self, card):
        """
        :param card: 可以通过消息卡片工具生成卡片数据库
            https://open.feishu.cn/tool/cardbuilder?templateId=ctp_AA1o9hqhLG0u
        :return:
        """
        data = {
            "msg_type": "interactive",
            "card": card
        }
        return self._send(data)


if __name__ == "__main__":
    token = ""
    robot = FeishuRobot(token=token)
    content = [
        dict(tag="text", text="项目有更新:"),
        dict(tag="a", text="请查看", href="http://www.example.com/"),
        dict(tag="at", user_id="oui_xxxxxx")
    ]
    card = {
        "config": {
            "wide_screen_mode": True
        },
        "elements": [
            {
                "tag": "markdown",
                "content": "zheg"
            },
            {
                "alt": {
                    "content": "",
                    "tag": "plain_text"
                },
                "img_key": "img_v2_041b28e3-5680-48c2-9af2-497ace79333g",
                "tag": "img",
                "mode": "crop_center",
                "compact_width": True
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "这是跳转按钮"
                        },
                        "type": "default",
                        "multi_url": {
                            "url": "https://feishu.cn",
                            "pc_url": "",
                            "android_url": "",
                            "ios_url": ""
                        },
                        "value": {
                            "sss": "fdsa"
                        }
                    }
                ]
            }
        ],
        "header": {
            "template": "blue",
            "title": {
                "content": "xxxxx",
                "tag": "plain_text"
            }
        }
    }
    print(robot.send_card(card))
