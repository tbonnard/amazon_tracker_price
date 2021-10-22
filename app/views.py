from flask import redirect, url_for, render_template, flash, request, session, Blueprint
from flask_login import login_user, login_required, current_user, logout_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap

from .forms import UserForm, UserLoginForm, ItemPriceForm
from .models import db, User, Item
from .product import Product

main = Blueprint('main', __name__)
login_manager = LoginManager()
bootstrap = Bootstrap()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_item(url, price):
    new_item = Item(url=url, price_limit=price, user=current_user)
    db.session.add(new_item)
    new_product = Product(new_item.url)
    try:
        product_name = new_product.get_product_title()
    except:
        pass
    else:
        new_item.product_title = product_name
    db.session.commit()


# ROUTES
@main.route('/', methods=['GET', "POST"])
def home():
    form = ItemPriceForm()
    if form.validate_on_submit():
        if 'amazon' in form.url.data:
            if not current_user.is_authenticated:
                session['url'] = form.url.data
                session['price'] = form.price_limit.data
                return redirect(url_for('main.register'))
            else:
                create_item(form.url.data, form.price_limit.data)
                return redirect(url_for('main.home'))
        else:
            flash('Must be an Amazon url')
    if current_user.is_authenticated:
        items = Item.query.filter_by(user=current_user)
        return render_template("index.html", form=form, items=items)
    return render_template("index.html", form=form, items=None)


@main.route("/login", methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main.home'))
            else:
                flash("Sorry, those credentials (pwd) info do not allow an access")
        else:
            flash("Sorry, those credentials (email) info do not allow an access ")
    return render_template('login.html', form=form)


@main.route("/register", methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("It seems an error occurred. Try with other credentials or try to login if you already have an account!")
            return redirect(url_for('main.register'))
        else:
            pwd_hashed = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)
            new_user = User(email=form.email.data, password=pwd_hashed, name=form.name.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            if session.get('url') and session.get('price'):
                create_item(session.get('url'), session.get('price'))
        return redirect(url_for('main.home'))
    return render_template('register.html', form=form)


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@main.route("/delete")
@login_required
def delete():
    product_id = request.args.get('product_id')
    product_do_delete = Item.query.get(product_id)
    if product_do_delete and product_do_delete.user == current_user:
        db.session.delete(product_do_delete)
        db.session.commit()
    return redirect(url_for('main.home'))


@main.route("/faq")
def faq():
    return render_template('faq.html')
