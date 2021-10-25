import smtplib
import os

class Notification:
    MY_EMAIL = os.environ.get("MY_EMAIL")
    PWD = os.environ.get("PWD")

    def __init__(self, to_email, item, new_price):
        self.to_email = to_email
        self.item = item
        self.new_price = new_price
        self.message = f"Subject:Better price for {self.item.product_title}!! \n\n<a href='{self.item.url}'>{self.item.product_title}</a> is now at ${self.new_price}.\n\nYour price limit has been updated to ${self.new_price}"

    def send_email_notification(self):
        print(self.MY_EMAIL)
        print(self.PWD)
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self.MY_EMAIL, password=self.PWD)
            connection.sendmail(from_addr=self.MY_EMAIL, to_addrs=self.to_email, msg=self.message.encode('utf-8'))