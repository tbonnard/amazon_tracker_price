from .models import Item
from .product import Product
from .notification import Notification

from app import db, create_app

app=create_app()


def script_check_price_users():
    with app.app_context():
        all_items = Item.query.all()
        print(all_items)
        for i in all_items:
            print(i.product_title)
            item_to_check = Product(i.url)
            item_price = item_to_check.define_price()
            if item_price is not None:
                if item_price < i.price_limit:
                    print(i.user.email)
                    new_notification = Notification(i.user.email, i, item_price)
                    new_notification.send_email_notification()
                    print(f"OLD: {i.price_limit}")
                    i.price_limit = item_price
                    db.session.commit()
                    print(f"NEW: {i.price_limit}")
