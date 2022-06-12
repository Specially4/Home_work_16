from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(20))


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(50))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# db.drop_all()
# db.create_all()
@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'POST':
        data_users = request.get_json()
        for item in data_users:
            user = User(id=item['id'],
                        first_name=item['first_name'],
                        last_name=item['last_name'],
                        age=item['age'],
                        email=item['email'],
                        role=item['role'],
                        phone=item['phone'])
            db.session.add(user)
        db.session.commit()
    all_users = []
    for user in User.query.all():
        all_users.append({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'email': user.email,
            'role': user.role,
            'phone': user.phone
        })
    return jsonify(all_users)


@app.route('/user/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def get_user(pk):
    one_user = User.query.get(pk)
    if request.method == 'PUT':
        data_user = request.get_json()
        for item in data_user:
            one_user.id = item['id']
            one_user.first_name = item['first_name']
            one_user.last_name = item['last_name']
            one_user.age = item['age']
            one_user.email = item['email']
            one_user.role = item['role']
            one_user.phone = item['phone']
            db.session.add(one_user)
        db.session.commit()
    elif request.method == 'DELETE':
        db.session.delete(one_user)
        db.session.commit()
        return 'Удаление прошло успешно'

    one_user = User.query.get(pk)
    result = {'id': one_user.id,
              'first_name': one_user.first_name,
              'last_name': one_user.last_name,
              'age': one_user.age,
              'email': one_user.email,
              'role': one_user.role,
              'phone': one_user.phone
              }
    return jsonify(result)


@app.route('/orders', methods=['GET', 'POST'])
def get_orders():
    if request.method == 'POST':
        data_orders = request.get_json()
        for item in data_orders:
            month_start, day_start, year_start = [int(x) for x in item['start_date'].split('/')]
            month_end, day_end, year_end = [int(x) for x in item['end_date'].split('/')]
            order = Order(id=item['id'],
                          name=item['name'],
                          description=item['description'],
                          start_date=datetime.date(year=year_start, month=month_start, day=day_start),
                          end_date=datetime.date(year=year_end, month=month_end, day=day_end),
                          address=item['address'],
                          price=item['price'],
                          customer_id=item['customer_id'],
                          executor_id=item['executor_id'])
            db.session.add(order)
        db.session.commit()
    all_orders = []
    for one_order in Order.query.all():
        all_orders.append({
            'id': one_order.id,
            'name': one_order.name,
            'description': one_order.description,
            'start_date': one_order.start_date,
            'end_date': one_order.end_date,
            'address': one_order.address,
            'price': one_order.price,
            'customer_id': one_order.customer_id,
            'executor_id': one_order.executor_id
        })
    return jsonify(all_orders)


@app.route('/order/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def get_order(pk):
    one_order = Order.query.get(pk)
    if request.method == 'PUT':
        data_order = request.get_json()
        for item in data_order:
            month_start, day_start, year_start = [int(x) for x in item['start_date'].split('/')]
            month_end, day_end, year_end = [int(x) for x in item['end_date'].split('/')]
            one_order.id = item['id']
            one_order.name = item['name']
            one_order.description = item['description']
            one_order.start_date = datetime.date(year=year_start, month=month_start, day=day_start)
            one_order.end_date = datetime.date(year=year_end, month=month_end, day=day_end)
            one_order.address = item['address']
            one_order.price = item['price']
            one_order.customer_id = item['customer_id']
            one_order.executor_id = item['customer_id']
            db.session.add(one_order)
        db.session.commit()
    elif request.method == 'DELETE':
        db.session.delete(one_order)
        db.session.commit()
        return 'Удаление прошло успешно'
    one_order = Order.query.get(pk)
    result = {
        'id': one_order.id,
        'name': one_order.name,
        'description': one_order.description,
        'start_date': one_order.start_date,
        'end_date': one_order.end_date,
        'address': one_order.address,
        'price': one_order.price,
        'customer_id': one_order.customer_id,
        'executor_id': one_order.executor_id
    }
    return jsonify(result)


@app.route('/offers', methods=['GET', 'POST'])
def get_offers():
    if request.method == 'POST':
        data_offers = request.get_json()
        for item in data_offers:
            offer = Offer(id=item['id'],
                          order_id=item['order_id'],
                          executor_id=item['executor_id'])
            db.session.add(offer)
        db.session.commit()

    all_offer = []
    for one_offer in Offer.query.all():
        all_offer.append({
            'id': one_offer.id,
            'order_id': one_offer.order_id,
            'executor_id': one_offer.executor_id
        })
    return jsonify(all_offer)


@app.route('/offer/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def get_offer(pk):
    one_offer = Offer.query.get(pk)
    if request.method == 'PUT':
        data_offer = request.get_json()
        for item in data_offer:
            one_offer.id = item['id']
            one_offer.order_id = item['order_id']
            one_offer.executor_id = item['executor_id']
            db.session.add(one_offer)
        db.session.commit()
    elif request.method == 'DELETE':
        db.session.delete(one_offer)
        db.session.commit()
        return 'Удаление прошло успешно'

    one_offer = Offer.query.get(pk)
    result = {
        'id': one_offer.id,
        'order_id': one_offer.order_id,
        'executor_id': one_offer.executor_id
    }
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
