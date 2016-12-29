from app.model.models import *
from app.controller.uniqid import uniqidEmail
from app.controller.update_key import update_key

class Email:

    def __init__(self, names, username, email):
        self.names = names
        self.username = username
        self.email = email
        self.key = uniqidEmail()
        self.login = "savinggroup.cartix.io/#/signin"
        self.recover = "savinggroup.cartix.io/#/recover/{email}/{random}".format(email=email, random = self.key)
        self.footer = "For any inquiry e-mail us on info@cartix.io or call us on +250 785-489-992</p><p>Thanks for using Cartix, enjoy.<br>Cartix Team"


    def account(self):

        msg = Message('[Cartix] Account creation', sender='Cartix Team', recipients=[self.email])
        content = "<h4><span style='font-weight:200'>Hello</span> {names} <span style='font-weight:200'>,</span> </h4> <p> Welcome to Cartix</p><p>- Your username : {username} <br> - Sign in here : {link}</p><p>{footer}</p>".format(names=self.names, username=self.username, link=self.login, footer=self.footer)
        msg.html = """ {content} """.format(content=content)
        mail.send(msg)
        return True

    def resetlink(self):

        msg = Message('[Cartix] Password reset link', sender='Cartix Team', recipients=[self.email])
        content = "<h4><span style='font-weight:200'>Hello</span> {names} <span style='font-weight:200'>,</span> </h4> <p> Reset your password, and we'll get you on your way. <br> To change your Cartix password, click *<a href='{link}'>here</a>* or paste the following link into your browser: <br> {link}</p><p>{footer}</p>".format(
            names=self.names, link=self.recover, footer= self.footer)
        msg.html = """ {content} """.format(content=content)
        mail.send(msg)

        update = update_key(self.email, self.key)

        if update:
            return True

    def resetsuccess(self):

        msg = Message('[Cartix] Password reset successful', sender='Cartix Team', recipients=[self.email])
        content = "<h4><span style='font-weight:200'>Hello</span> {names} <span style='font-weight:200'>,</span> </h4> <p> You've successfully changed your Cartix password. <br> {link}</p><p>{footer}</p>".format(
            names=self.names, link=self.login, footer=self.footer)
        msg.html = """ {content} """.format(content=content)
        mail.send(msg)
        return True

