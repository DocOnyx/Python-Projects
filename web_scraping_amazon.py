from bs4 import BeautifulSoup
import requests
import lxml
import smtplib

print('Hey there, ShopBot can help you track an item from Amazon.co.uk and alert you when there is a price slash!')

URL = input('Enter the URL of the item to track: ')
curr_price = float(input('Enter item current price: '))
EMAIL = input('Enter your email address: ')
PASSWORD = input('Enter your password: ')
smtp_address = input("Enter 1 for GMAIL, 2 for HOTMAIL, 3  for OUTLOK and 4 for YAHOO: ")
SMTP = {'1': 'smtp.gmail.com', '2': 'smtp.live.com', '3': 'outlook.office365.com', '4': 'smtp.mail.yahoo.com'}

# GO TO http://myhttpheader.com/ to view your browser headers
headers = {
    'User-Agent': 'ENTER USER_AGENT',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

response = requests.get(URL, headers=headers).text
soup = BeautifulSoup(response, 'lxml')
item_name = soup.find(id='productTitle').getText()
item_price = soup.select_one('.priceToPay span').getText()
item_price_numeric = float(item_price.split('£')[1])


if item_price_numeric < curr_price:
    percent_reduction = ((curr_price - item_price_numeric)/curr_price) * 100
    message = f'Price slash alert!\n\n***{percent_reduction}%*** reduction in the price of ***{item_name.strip()}***.\n\nClick {URL} to buy now!\n\nSincerely,\nShopBot Team.'

    with smtplib.SMTP(SMTP[smtp_address], port=587) as connection:
        connection.starttls()
        result = connection.login(EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{message}"
        )



