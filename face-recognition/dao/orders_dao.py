from db.models import Order, Product
from statistics import mode


def get_orders():
    all_orders = Order.objects.all()
    return all_orders


def get_order(user_id):
    try:
        order = Order.objects.get(user_id = user_id)
    except:
        return "No products!"
    product_ids = order.product_ids
    product_id = mode(product_ids)
    product = Product.objects.get(id = product_id)
    return product.name

