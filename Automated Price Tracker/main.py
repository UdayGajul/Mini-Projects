#
# ! Amazon product price tracking and sending email

from get_product_price import GetProductPrice
from send_mail import SendMail
import os
from dotenv import load_dotenv

load_dotenv()

BUY_PRICE = 3140 #INR
# ? changable link, your amazon product link
PRODUCT_LINK_1 = "https://www.amazon.in/CALISTHENICS-PARALLETTES-BODYMECHANICS-Specially-Calisthenics/dp/B08R61Y3LV/ref=sr_1_7?crid=3P5SYJCTT2P47&dib=eyJ2IjoiMSJ9.NidcQUNHCpougFGeFNiOBKluywanVnxJYIHlCqK9gh5QwKYz7JkP6fxofdw38l7f7HpdZLwTEVCc19k2WPXuEcn1F4mrNvsYYq7xHHa4oaN6engZMcFyibMRblaXIRSqTGSXeBU_nELPYddF3UTYukn_BLETt0kCbI2Il9llJoFr9o67HWZkd4FeLmzFHxTqeYNaG61tAzEiVoOtaN9-rozreBT_q1DmhpTalFiwF_6Xf6DzRtgfVQgYAQxs9Sp5obkIMY8pZmpvUBrIZpm4i5nXUwvl6b3m1E7RPJ3jX7s.c4RQBiUa0zYpioGnMiTIPZIrVj2qe00a7MNVXqn50uQ&dib_tag=se&keywords=calisthenics%2Bequipment&qid=1773065408&refinements=p_36%3A295000-410000&rnid=1318502031&sprefix=calisthenics%2Caps%2C559&sr=8-7&th=1"


gpp = GetProductPrice(
    product_url=PRODUCT_LINK_1,
)

price, name = gpp.get_price_and_product()

print(price, name)

sm = SendMail(
    current_price=price,
    expected_price=BUY_PRICE,
    receiver_mail=os.getenv("RECEIVER_MAIL"),
    product_name=name,
    product_link=PRODUCT_LINK_1,
)

sm.send_email()
