from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User, Product, CartItem, favorites, Review
from .forms import RegistrationForm, LoginForm

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# ------------------------------------------------
# Регистрация и вход пользователя
# ------------------------------------------------
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Пользователь с таким email уже существует.')
            return redirect(url_for('main_bp.register'))
        
        hashed_pwd = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password_hash=hashed_pwd)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация прошла успешно. Можете войти.')
        return redirect(url_for('main_bp.login'))
    return render_template('register.html', form=form)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Вы вошли в систему.')
            return redirect(url_for('main_bp.index'))
        else:
            flash('Неверный email или пароль.')
    return render_template('login.html', form=form)

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.')
    return redirect(url_for('main_bp.index'))

# ------------------------------------------------
# Страница со списком товаров, фильтры
# ------------------------------------------------
@main_bp.route('/products')
def product_list():
    category = request.args.get('category')
    sort_by = request.args.get('sort_by')
    
    query = Product.query
    if category:
        query = query.filter_by(category=category)
    if sort_by == 'price':
        query = query.order_by(Product.price)
    elif sort_by == 'rating':
        query = query.order_by(Product.rating.desc())
    elif sort_by == 'created':
        query = query.order_by(Product.created_at.desc())
    
    products = query.all()
    return render_template('product_list.html', products=products)

@main_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).all()
    return render_template('product_detail.html', product=product, reviews=reviews)

# ------------------------------------------------
# Корзина покупок (Cart)
# ------------------------------------------------
@main_bp.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@main_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    existing_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing_item:
        existing_item.quantity += quantity
    else:
        new_cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(new_cart_item)
    db.session.commit()
    flash('Товар добавлен в корзину.')
    return redirect(url_for('main_bp.cart'))

@main_bp.route('/cart/remove/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    item = CartItem.query.get_or_404(cart_item_id)
    if item.user_id != current_user.id:
        flash('Невозможно удалить чужой товар из корзины.')
        return redirect(url_for('main_bp.cart'))
    
    db.session.delete(item)
    db.session.commit()
    flash('Товар удалён из корзины.')
    return redirect(url_for('main_bp.cart'))

# ------------------------------------------------
# Избранное (Favorites)
# ------------------------------------------------
@main_bp.route('/favorite/<int:product_id>', methods=['POST'])
@login_required
def add_favorite(product_id):
    product = Product.query.get_or_404(product_id)
    # Проверяем, нет ли уже в избранном
    stmt = favorites.insert().values(user_id=current_user.id, product_id=product.id)
    try:
        db.session.execute(stmt)
        db.session.commit()
        flash('Добавлено в избранное.')
    except:
        flash('Этот товар уже в избранном.')
    return redirect(url_for('main_bp.index'))

@main_bp.route('/favorites')
@login_required
def favorites_list():
    user = User.query.get(current_user.id)
    # relation "favorites" через secondary таблицу
    # Но у нас таблица без модели, поэтому сделаем ручной запрос
    user_favorites = Product.query.join(favorites, Product.id == favorites.c.product_id).filter(favorites.c.user_id == user.id).all()
    return render_template('product_list.html', products=user_favorites)

# ------------------------------------------------
# Отзывы (Reviews)
# ------------------------------------------------
@main_bp.route('/review/<int:product_id>', methods=['POST'])
@login_required
def add_review(product_id):
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment', '')
    new_review = Review(product_id=product_id, user_id=current_user.id, rating=rating, comment=comment)
    db.session.add(new_review)
    db.session.commit()
    flash('Отзыв добавлен.')
    return redirect(url_for('main_bp.product_detail', product_id=product_id))
