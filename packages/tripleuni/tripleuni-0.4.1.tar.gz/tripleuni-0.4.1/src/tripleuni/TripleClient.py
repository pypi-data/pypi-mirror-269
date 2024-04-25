import requests
import os


class TripleClient:
    def __init__(self, token: str = None, domain: str = "uuunnniii.com", version: str = "v4"):
        self.session: requests.Session = requests.Session()
        self.if_login: bool = False if token is None else True
        self.stored_data: dict = {}
        self.token: str = token
        self.domain: str = domain
        self.version: str = version

    def checkToken(self) -> bool:
        """
        Check if the token is valid
        :return: bool
        """
        post_data = {
            "token": self.token,
            "language": "zh-CN"
        }
        post_response = self.session.post(f"https://api.{self.domain}/{self.version}/post/list/all.php", data=post_data)

        if post_response.status_code == 200:
            post_response_data = post_response.json()
            if post_response_data['code'] == 200:
                return True

        return False

    def sendVerification(self, email: str) -> dict:
        """
        Send a verification code to the email
        :param email:
        :return: bool
        """
        email_data = {
            "user_email": email,
            "language": "zh-CN"
        }
        email_response = self.session.post(f"https://api.{self.domain}/{self.version}/user/register/web/email.php", data=email_data)

        if email_response.status_code == 200:
            email_response_data = email_response.json()
            if email_response_data['code'] == 200:
                self.stored_data = email_response_data

            return email_response_data

        return {}

    def verifyCode(self, vcode: str) -> bool:
        """
        Verify the verification code
        :param vcode:
        :return: bool
        """
        stored_data = self.stored_data
        verify_data = {
            "vcode_vcode": vcode,
            "vcode_key": stored_data['vcode_key'],
            "user_itsc": stored_data['user_itsc'],
            "user_email_suffix": stored_data['user_email_suffix'],
            "user_school_label": stored_data['user_school_label'],
            "language": "zh-CN"
        }
        varify_response = self.session.post(f"https://api.{self.domain}/{self.version}/user/register/web/verify.php",
                                            data=verify_data)

        if varify_response.status_code == 200:
            varify_response_data = varify_response.json()
            if varify_response_data['code'] == 200:
                self.token = varify_response_data['token']

                return True

        return False

    def getPostList(self, page: int = 0) -> dict:
        """
        Get a list of posts
        :param page:
        :return: response data in dict or {}
        """
        post_data = {
            "token": self.token,
            "page": page,
            "language": "zh-CN"
        }
        post_response = self.session.post(f"https://api.{self.domain}/{self.version}/post/list/all.php", data=post_data)

        if post_response.status_code == 200:
            post_response_data = post_response.json()
            if post_response_data['code'] == 200:
                return post_response_data

        return {}

    def commentMsg(self, uniPostId: int, msg: str, real_name: str = 'false') -> dict:
        """
        Send a comment to a post
        :param uniPostId:
        :param msg:
        :param real_name:
        :return: response data in dict or {}
        """
        post_data = {
            "token": self.token,
            "uni_post_id": uniPostId,
            "comment_msg": msg,
            "language": "zh-CN",
            "user_is_real_name": real_name
        }

        post_response = self.session.post(f"https://api.{self.domain}/{self.version}/comment/post.php", data=post_data)

        if post_response.status_code == 200:
            return post_response.json()

        return {}

    def createChatSession(self, uni_post_id: int, real_name: str = 'false') -> dict:
        """
        Create a chat session with the post owner
        :param uni_post_id:
        :param real_name:
        :return: response data in dict or {}
        """
        post_data = {
            "token": self.token,
            "uni_post_id": uni_post_id,
            "language": "zh-CN",
            "to_type": "post",
            "sender_is_real_name": real_name,
            "comment_order": "null"
        }

        post_response = self.session.post(f"https://api.{self.domain}/{self.version}/pm/chat/create.php", data=post_data)

        if post_response.status_code == 200:
            return post_response.json()

        return {}

    def sendChatMsg(self, chat_id: int, msg: str) -> dict:
        """
        Send a private message to a chat session
        :param chat_id:
        :param msg:
        :return: response data in dict or {}
        """
        post_data = {
            "token": self.token,
            "chat_id": chat_id,
            "pm_msg": msg,
            "language": "zh-CN"
        }

        post_response = self.session.post(f"https://api.{self.domain}/{self.version}/pm/message/send.php", data=post_data)

        if post_response.status_code == 200:
            return post_response.json()

        return {}

    def sendChatMsgToPost(self, uni_post_id: int, msg: str, real_name: str = 'false') -> dict:
        """
        Send a private message to the post owner
        :param uni_post_id:
        :param msg:
        :param real_name:
        :return: response data in dict or {}
        """
        chat_id = self.createChatSession(uni_post_id, real_name)["chat_id"]
        return self.sendChatMsg(chat_id, msg)

    def replyMsg(self, uni_post_id: int, comment_father_id: int, msg: str, real_name: str = 'false') -> dict:
        """
        Reply to a comment
        :param uni_post_id:
        :param comment_father_id:
        :param msg:
        :param real_name:
        :return: response data in dict or {}
        """
        post_data = {
            "token": self.token,
            "uni_post_id": uni_post_id,
            "comment_msg": msg,
            "language": "zh-CN",
            "user_is_real_name": real_name,
            "comment_father_id": comment_father_id
        }

        post_response = self.session.post(f"https://api.{self.domain}/{self.version}/comment/post.php", data=post_data)

        if post_response.status_code == 200:
            return post_response.json()

        return {}

    def followPost(self, uni_post_id: int) -> dict:
        """
        Follow a post for the first time

        Unfollow a post for the second time
        :param uni_post_id:
        :return: response data in dict or {}
        """
        post_data = {
            "token": self.token,
            "uni_post_id": uni_post_id,
            "language": "zh-CN"
        }

        post_response = self.session.post(f"https://api.{self.domain}/{self.version}/post/single/follow.php", data=post_data)

        if post_response.status_code == 200:
            return post_response.json()

        return {}

    def reportPost(self, uni_post_id: int, comment_order: int, comment_msg: str, report_msg: str) -> dict:
        """
        Report a post
        :param uni_post_id:
        :param comment_order:
        :param comment_msg:
        :param report_msg:
        :return: response data in dict or {}
        """
        post_data = {
            "token": self.token,
            "uni_post_id": uni_post_id,
            "comment_order": comment_order,
            "comment_msg": comment_msg,
            "report_msg": report_msg,
            "language": "zh-CN"
        }

        post_response = self.session.post(f"https://api.{self.domain}/{self.version}/post/single/report.php", data=post_data)
        if post_response.status_code == 200:
            return post_response.json()

        return {}

    def getDetail(self, uni_post_id: int) -> dict:
        """
        Get the detail of a post including comments
        :param uni_post_id:
        :return: response data in dict or {}
        """
        post_data = {
            "token": self.token,
            "uni_post_id": uni_post_id,
            "language": "zh-CN"
        }

        post_response = self.session.post(f"https://api.{self.domain}/{self.version}/post/single/get.php", data=post_data)
        if post_response.status_code == 200:
            return post_response.json()

        return {}

    def streamWithChatbot(self, msg: str, history: str = "[]"):
        """
        Chat with the chatbot
        :param msg:
        :return: response stream iterator
        """
        
        # encode the message
        msg = msg.encode("utf-8")

        params = {
            "token": self.token,
            "question": msg,
            "history": history,
        }

        response = self.session.get(f"https://chat.{self.domain}", params=params, stream=True)
        for line in response.iter_lines():
            line = line.decode("utf-8")

            if line.startswith("event: close"):
                break

            if line.startswith("data:"):
                yield line.split(":")[-1].strip("}").strip('"')
    
    def chatWithChatbot(self, msg: str, history: str = "[]") -> str:
        """
        Chat with the chatbot
        :param msg:
        :return: response data in dict or {}
        """
        return "".join(list(self.streamWithChatbot(msg, history)))
            


if __name__ == "__main__":
    import os

    token = os.getenv("TRIPLE_TOKEN")
    client = TripleClient(token, domain="uuunnniii.com", version="v4")

    print(client.checkToken())

