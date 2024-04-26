# MyEmail
A simple library to send emails with python
## Example
```python
from myemail.myemail import send
import os

sslport = os.getenv("SSLPORT")  # For SSL
password = os.getenv("PASSWORD")
smtpserver = os.getenv("SMTPSERVER")
emailvar = os.getenv("EMAIL")
attachment_path = f"{os.getenv('HOME')}/testfile123.txt"
print(attachment_path)
send(
    msg_content="test",
    from_email=emailvar,
    to_email=emailvar,
    subject="test",
    sslport=sslport,
    password=password,
    attachment_path=attachment_path,
)

```

## Contact
- [GitHub (Repo)](https://github.com/tct123/myemail)
- [GitHub](https://github.com/tct123)
