from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User, Product, CartItem, favorites, Review, Order, OrderItem
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
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_pwd
        )

        # Проверим, есть ли уже админ в системе
        admin_exists = User.query.filter_by(role='admin').first()
        if not admin_exists:
            # Если админов нет, этот пользователь станет админом
            new_user.role = 'admin'
            flash('Так как администраторов не было, вы назначены администратором.')

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
    # Получение всех уникальных категорий, цветов и материалов из базы данных
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]

    colors = db.session.query(Product.color).distinct().all()
    colors = [c[0] for c in colors if c[0]]

    materials = db.session.query(Product.material).distinct().all()
    materials = [m[0] for m in materials if m[0]]

    # Получение параметров фильтра из GET-запроса
    selected_category = request.args.get('category')
    selected_color = request.args.get('color')
    selected_material = request.args.get('material')
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    sort_by = request.args.get('sort_by')

    query = Product.query

    # Применение фильтров
    if selected_category:
        query = query.filter_by(category=selected_category)
    if selected_color:
        query = query.filter_by(color=selected_color)
    if selected_material:
        query = query.filter_by(material=selected_material)
    if price_min is not None:
        query = query.filter(Product.price >= price_min)
    if price_max is not None:
        query = query.filter(Product.price <= price_max)

    # Применение сортировки
    if sort_by == 'price':
        query = query.order_by(Product.price)
    elif sort_by == 'rating':
        query = query.order_by(Product.rating.desc())
    elif sort_by == 'created':
        query = query.order_by(Product.created_at.desc())

    products = query.all()

    # Передача данных в шаблон
    return render_template('product_list.html', 
                           products=products,
                           categories=categories,
                           colors=colors,
                           materials=materials,
                           selected_category=selected_category,
                           selected_color=selected_color,
                           selected_material=selected_material,
                           price_min=price_min,
                           price_max=price_max,
                           sort_by=sort_by)


@main_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).all()
    # Средний рейтинг
    from sqlalchemy import func
    avg_rating = db.session.query(func.avg(Review.rating)).filter(Review.product_id == product_id).scalar()
    if avg_rating is None:
        avg_rating = 0  # Если нет отзывов, рейтинг 0 или не показывать

    return render_template('product_detail.html', product=product, reviews=reviews, avg_rating=avg_rating)

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
    # Текущий пользователь
    user_favorites = Product.query.join(
        favorites, Product.id == favorites.c.product_id
    ).filter(favorites.c.user_id == current_user.id).all()

    return render_template('favorites.html', products=user_favorites)

# ------------------------------------------------
# Отзывы (Reviews)
# ------------------------------------------------
@main_bp.route('/review/<int:product_id>', methods=['POST'])
@login_required
def add_review(product_id):
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '')
    if rating < 1 or rating > 5:
        flash('Рейтинг должен быть от 1 до 5.')
        return redirect(url_for('main_bp.product_detail', product_id=product_id))

    # Проверим, оставлял ли пользователь уже отзыв (не обязательно, но можно)
    existing_review = Review.query.filter_by(product_id=product_id, user_id=current_user.id).first()
    if existing_review:
        flash('Вы уже оставляли отзыв для этого товара.')
        return redirect(url_for('main_bp.product_detail', product_id=product_id))

    new_review = Review(product_id=product_id, user_id=current_user.id, rating=rating, comment=comment)
    db.session.add(new_review)
    db.session.commit()
    flash('Отзыв добавлен!')
    return redirect(url_for('main_bp.product_detail', product_id=product_id))

@main_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    # Получаем все товары в корзине
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Невозможно оформить пустой заказ.')
        return redirect(url_for('main_bp.cart'))

    # Создаём новый заказ
    new_order = Order(user_id=current_user.id, status='processing')
    db.session.add(new_order)
    db.session.commit()  # Сначала коммитим, чтобы получить ID заказа

    # Добавляем товары в OrderItem
    for item in cart_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.session.add(order_item)

    # Очищаем корзину
    for item in cart_items:
        db.session.delete(item)

    db.session.commit()

    flash(f'Заказ #{new_order.id} оформлен успешно!')
    # Можно перенаправить на страницу с заказами пользователя
    return redirect(url_for('main_bp.my_orders'))
@main_bp.route('/my_orders')
@login_required
def my_orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=user_orders)
@main_bp.route('/cart/update_quantity', methods=['POST'])
@login_required
def update_quantity():
    data = request.get_json()
    cart_item_id = data.get('cart_item_id')
    new_quantity = data.get('quantity')

    cart_item = CartItem.query.filter_by(id=cart_item_id, user_id=current_user.id).first()
    if not cart_item:
        return jsonify({'success': False, 'error': 'Item not found'}), 404

    if new_quantity < 1:
        return jsonify({'success': False, 'error': 'Invalid quantity'}), 400

    cart_item.quantity = new_quantity
    db.session.commit()

    # Пересчитываем стоимость позиции и общей суммы
    item_total = cart_item.product.price * cart_item.quantity
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(i.product.price * i.quantity for i in cart_items)

    return jsonify({'success': True, 'item_total': item_total, 'total': total})


@main_bp.route('/cart/remove_item', methods=['POST'])
@login_required
def remove_item():
    data = request.get_json()
    cart_item_id = data.get('cart_item_id')

    cart_item = CartItem.query.filter_by(id=cart_item_id, user_id=current_user.id).first()
    if not cart_item:
        return jsonify({'success': False, 'error': 'Item not found'}), 404

    db.session.delete(cart_item)
    db.session.commit()

    # Пересчитываем общую сумму
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(i.product.price * i.quantity for i in cart_items)

    return jsonify({'success': True, 'total': total})

@main_bp.route('/remove_favorite/<int:product_id>', methods=['POST'])
@login_required
def remove_favorite(product_id):
    # Проверяем, существует ли продукт
    product = Product.query.get_or_404(product_id)

    # Проверяем, есть ли продукт в избранном
    user_favorites = Product.query.join(
        favorites, Product.id == favorites.c.product_id
    ).filter(favorites.c.user_id == current_user.id, Product.id == product_id).first()

    if user_favorites:
        # Удаляем из избранного
        db.session.execute(
            favorites.delete().where(
                (favorites.c.user_id == current_user.id) & 
                (favorites.c.product_id == product_id)
            )
        )
        db.session.commit()
        flash(f'Товар "{product.name}" удалён из избранного.')
    else:
        flash('Этот товар не найден в вашем избранном.')

    return redirect(url_for('main_bp.favorites_list'))
