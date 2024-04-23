import re
import os
import pyreportgen.style as style
import pyreportgen.layout as layout
import pyreportgen.helpers as helpers
import pyreportgen.statistic as statistic
from pyreportgen.base import Component, _DATA_DIR
import uuid
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
import os

if not (_DATA_DIR in os.listdir()):
    os.makedirs(_DATA_DIR, exist_ok=True)


_RE_COMBINE_WHITESPACE = re.compile(r"\s+")

class MailAttachment:
    def __init__(self, path, filename) -> None:
        self.path = path
        self.filename = filename
    
    def get_attachment(self) -> MIMEBase:
        with open(self.path, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            att = MIMEBase("application", "octet-stream")
            att.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(att)

            # Add header as key/value pair to attachment part
            att.add_header(
                "Content-Disposition",
                f"attachment; filename={self.filename}",
            )
            return att

class Report(Component):
    def __init__(self, children:list[Component]=[], style:str=style.STYLE_NORMAL):
        super().__init__()
        self.children = children
        self.style = style

    def render(self) -> str:
        html = ""
        for i in self.children:
            html += i.render()
        html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>{self.style}</style>
                <title>Report</title>
            </head>
            <body>
                <main class="Main">
                    {html}
                </main>
            </body>
        """

        return _RE_COMBINE_WHITESPACE.sub(" ", html).strip()
    
    def pdf(self, path:str, html:str=""):
        import pdfkit 
        if html == "":
            html = self.render()

        with open(os.path.join(_DATA_DIR,'out.html'), 'w', encoding="UTF-8") as f:
            f.write(html)

        pdfkit.from_file(os.path.join(_DATA_DIR,'out.html'), path, options={"--enable-local-file-access":None, "--print-media-type":None})
    
    def email(self, user:str, password:str, subject:str, sender:str, recipient:str, smtp_server:str, smtp_port:int, context=ssl.create_default_context(), attachments:list[MailAttachment] = []):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender
        message["To"] = recipient


        html = self.render()

        filenames = []

        image_lookup = {}

        # Get image tags
        for img in re.findall(r"<img [^>]*>", html):
            # Get the content of the src attribute.
            path = re.findall(r"(?<=src=')[^']*(?=')",img)[0]
            image_lookup[path] = str(uuid.uuid4()) 
            html = html.replace(path, f"cid:{image_lookup[path]}")
            filenames.append(path)



        # Turn these into plain/html MIMEText objects
        html_message = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(html_message)

        for i in filenames:
            # This example assumes the image is in the current directory
            prefix = ""
            if not ((i.startswith("/")) or (i.startswith("*:\\"))):
                prefix = f"{_DATA_DIR}/"
            fp = open(f"{prefix}{i}", 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()

            # Define the image's ID as referenced above
            msgImage.add_header('Content-ID', f'<{image_lookup[i]}>')
            message.attach(msgImage)

        
        for i in attachments:
            # Add attachment to message and convert message to string
            message.attach(i.get_attachment())

        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(user, password)
            server.sendmail(sender, recipient, message.as_string())
    
class Html(Component):
    def __init__(self, html:str):
        super().__init__()
        self.html = html
    def render(self) -> str:
        return self.html
    
class ConditionalHtml(Component):
    def __init__(self, filepath:str, children:list[Component] = []):
        super().__init__()
        self.filepath:str = filepath
        self.children:list[Component] = children
    
    def render(self) -> str:
        if os.path.isfile(self.filepath):
            html = open(self.filepath, "r", encoding="UTF-8").read()
        else:
            html = ""
            for i in self.children:
                html += i.render()
        return helpers.tagwrap(html, "div")


class Text(Component):
    element = "p"

    def __init__(self, text:str, center=False):
        super().__init__()
        self.text = text
        self.center = center
    
    def render(self) -> str:
        classlist = ""
        if self.center:
            classlist += "CenterText "

        return helpers.tagwrap(self.text, self.element, classList=classlist)

class Header(Text):
    def __init__(self, text: str, center=True, heading=1):
        super().__init__(text, center)
        self.element = "h"+str(helpers.clamp(heading, 1, 6))
    
    def render(self) -> str:
        return super().render()

class Image(Component):
    def __init__(self, src: str):
        super().__init__()
        
        if src.startswith("http"):
            self.src = src
        else:

            self.src: str = f"file://{os.path.abspath(src)}"
    
    def render(self) -> str:
        return helpers.tagwrap("", "img", "Image", f"src='{self.src}'", close=False)
    
class ConditionalImage(Component):
    def __init__(self, filepath:str, children:list[Component] = []):
        super().__init__()
        self.filepath:str = filepath
        self.children:list[Component] = children
    
    def render(self) -> str:
        if os.path.isfile(self.filepath):
            html = helpers.tagwrap("", "img", "Image", f"src='file://{os.path.abspath(self.filepath)}'", close=False)
        else:
            html = ""
            for i in self.children:
                html += i.render()
            html = helpers.tagwrap(html, "div")
        return html