# tripleuni
A python library for tripleuni.
## Installation
```bash
pip install tripleuni
```

## Usage
### Login
you need to login to use the library
#### login in terminal
```python
from tripleuni import TripleClient
client = TripleClient()
client.sendVerification("your email address")
client.verifyCode("your verification code")
```
#### login by token
```python
from tripleuni import TripleClient
client = TripleClient("your token")
```

### list of methods
```python
### login
def sendVerification(self, email: str) -> dict:
def verifyCode(self, code: str) -> dict:

### get post and comment
def getPostList(self, page: int = 0) -> dict:
def getDetail(self, uni_post_id: int) -> dict:

### post operations
def followPost(self, uni_post_id: int) -> dict:
def reportPost(self, uni_post_id: int, comment_order: int, comment_msg: str, report_msg: str) -> dict:

### comment and reply
def commentMsg(self, uniPostId: int, msg: str, real_name: str = 'false') -> dict:
def replyMsg(self, uni_post_id: int, comment_father_id: int, msg: str, real_name: str = 'false') -> dict:

### chat
def createChatSession(self, uni_post_id: int, real_name: str = 'false') -> dict:
def sendChatMsg(self, chat_id: int, msg: str) -> dict:
def sendChatMsgToPost(self, uni_post_id: int, msg: str, real_name: str = 'false') -> dict:

### chat with bot
#### return a string of chat messages
def chatWithChatbot(self, msg: str, history: str = '[]') -> str:
#### return a iterator of chat messages
def streamWithChatbot(self, msg: str, history: str = '[]') -> iterator:
```

### Some examples
```python
# get post list
postList = client.getPostList(page=1)

# comment a post
client.commentMsg(1234, "hello", real_name='false')

# send chat message to post owner
client.sendChatMsgToPost(1234, "hello", real_name='false')

```

## For Maintainers

### Build
```bash
py -m pip install --upgrade build
py -m build
```

```bash
py -m pip install --upgrade twine
twine upload dist/*
```

