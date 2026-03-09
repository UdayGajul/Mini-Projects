#
# ! this is a python script that has a class to send a mail if a product price is less than user expected

import smtplib
from dotenv import load_dotenv
import os

load_dotenv()


class SendMail:
    """
    Takes the current price, expected price of a amazon product and checks if the current product is less than expected price
    if yes then sends a mail mentioning that is price is low now and you are ready to by
    """

    def __init__(
        self,
        current_price: int,
        expected_price: int,
        receiver_mail: str,
        product_name: str,
        product_link: str,
    ):
        self.current_price = current_price
        self.expected_price = expected_price
        self.receiver_mail = receiver_mail
        self.product_name = product_name
        self.product_link = product_link

    def send_email(self):
        """
        Sends mail if current price is less than the expected price, with the product name, price and link
        """

        senders_mail = os.getenv("SENDER_MAIL")

        if self.current_price != 0 or self.product_name != "No product":
            if self.current_price < self.expected_price:
                connection = smtplib.SMTP(os.getenv("SMTP_ADDRESS"), 587)

                connection.starttls()

                connection.login(user=senders_mail, password=os.getenv("APP_PASSWORD"))

                msg1 = f"""\n
                Great news! The price for {self.product_name} has been reduced to INR *{self.current_price}*.\n
                So now's the perfect time to grab it before the offer ends!\n
                The link - {self.product_link} 
                """

                connection.sendmail(
                    from_addr=senders_mail,
                    to_addrs=self.receiver_mail,
                    msg=f"Subject: *Price Drop Alert* - Get Your Product at the Best Price Now!{msg1}",
                )

                connection.close()

                print("mail sent, please check indbox")
        else:
            print(
                "wait the product price is more than you expect\nOR\nfailed to retrieve the product data check the html above!"
            )
