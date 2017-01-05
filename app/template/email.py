from app.model.models import *
from app.controller.uniqid import uniqidEmail
from app.controller.update_key import update_key

class Email:

    def __init__(self, names, username, email):
        self.names = names
        self.username = username
        self.email = email
        self.key = uniqidEmail()
        self.login = "http://savinggroup.cartix.io/#/signin"
        self.recover = "http://savinggroup.cartix.io/#/recover/{email}/{random}".format(email=email, random = self.key)
        self.footer = "For any inquiry e-mail us on info@cartix.io or call us on +250 785-489-992<p>Thanks for using Cartix, enjoy.<br>Cartix Team"


    def account(self):

        msg = Message('[Cartix] Account creation', sender='Cartix Team', recipients=[self.email])
        content = '<div style="margin: auto;width:60%;background-color:white;"> <div style="margin-left:30px;padding-top:50px;padding-bottom:50px;"> <img style="margin-left:12px;margin-top:20px;height:40px;" src="http://savinggroup.cartix.io/assets/img/mail/letter-logo1.png"> <p style="font-family:sans-serif;margin-left:10px;padding-top:15px;color:#424242">Hallo <span style="font-weight:bold">{names},</span></p> <p style="font-family:sans-serif;margin-left:10px;color:#424242">Welcome to Cartix</p> <p style="font-family:sans-serif;margin-left:10px;color:#424242"> -Your Username: {username} <br> - Sign in here : {link} </p> <p style="font-family:sans-serif;margin-left:10px;color:#424242"> {footer} </p> </div> </div> <div style="margin: auto;width: 60%; padding-top:20px;background-color:#FAFAFA;"> <div style="margin-left:30px"> <img style="margin-left:12px;margin-top:20px;height:50px;" src="http://savinggroup.cartix.io/assets/img/mail/cartix-logo2.svg"><br> <span style="font-family:sans-serif;font-size:12px;margin-left:12px;color:#424242">You\'re receiving this message because you are a cartix user</span><br> <span style="font-family:sans-serif;font-size:12px;margin-left:12px;color:#424242">send us feedback on info@cartix.io or call us +250785489992</span> <p style="font-family:sans-serif;font-size:12px;margin-left:12px;color:#424242">Cartix is a product of <a href="http://www.exuus.com"target="_blank">exuus Ltd.</a><br> Exuus is a limited corporation registered in Republic of Rwanda.</p> <br> </div> </div>'.format(names=self.names, username=self.username, link=self.login, footer=self.footer)
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

