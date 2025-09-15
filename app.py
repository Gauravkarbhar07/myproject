from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Equipment, Cart  # models file se import karo
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, warning avoid karne ke liye

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    equipments = Equipment.query.all()
    return render_template('dashboard.html', equipments=equipments)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/add_to_cart/<int:equipment_id>')
@login_required
def add_to_cart(equipment_id):
    cart_item = Cart.query.filter_by(user_id=current_user.id, equipment_id=equipment_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(user_id=current_user.id, equipment_id=equipment_id, quantity=1)
        db.session.add(cart_item)
    db.session.commit()
    flash("Item added to cart!")
    return redirect(url_for('dashboard'))

@app.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', cart_items=cart_items)

# Optional: Add sample data route for testing
@app.route('/add_sample')
def add_sample():
    sample = Equipment(name="Football", description="Standard football", price=25.0, image_url="https://via.placeholder.com/150", seller_id=1)
    db.session.add(sample)
    db.session.commit()
    return "Sample equipment added!"

if __name__ == "__main__":
    app.run(debug=True)
