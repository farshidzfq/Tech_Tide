from flask import Flask, render_template, url_for, flash, redirect, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models import db, User, Product, Order, OrderItem
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize the database and login manager
db.init_app(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    order_item = OrderItem(product_id=product_id, order_id=current_user.id)
    db.session.add(order_item)
    db.session.commit()
    flash('Product added to cart.', 'success')
    return redirect(url_for('index'))

@app.route('/cart')
@login_required
def cart():
    cart_items = OrderItem.query.filter_by(order_id=current_user.id).all()
    products = [Product.query.get(item.product_id) for item in cart_items]
    return render_template('cart.html', products=products)

@app.route('/checkout')
@login_required
def checkout():
    order = Order(user_id=current_user.id)
    db.session.add(order)
    db.session.commit()
    flash('Your order has been placed!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
