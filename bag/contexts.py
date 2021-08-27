from shop.models import Album, Product
from django.conf import settings


def bag_details(request):
    bag = request.session.get('bag', {})
    bag_items = []
    total = 0

    for item in bag:
        if type(bag[item]) is int:
            product = Product.objects.get(name=item)
            quantity = bag[item]
            item_total = product.price * quantity
            total += item_total

            bag_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
            })

        elif bag[item]['type'] == 'album':
            product = Album.objects.get(title=item)
            cd_count = bag[item]['items_by_format'].get('cd', 0)
            vinyl_count = bag[item]['items_by_format'].get('vinyl', 0)
            cd_total = cd_count * product.cd_price
            vinyl_total = vinyl_count * product.vinyl_price
            item_total = cd_total + vinyl_total
            total += item_total
            bag_items.append({
                'type': 'album',
                'product': product,
                'cd_count': cd_count,
                'vinyl_count': vinyl_count,
                'item_total': item_total,
            })

        elif bag[item]['type'] == 'sized':
            product = Product.objects.get(name=item)
            small_count = bag[item]['items_by_size'].get('S', 0)
            medium_count = bag[item]['items_by_size'].get('M', 0)
            large_count = bag[item]['items_by_size'].get('L', 0)
            count_total = small_count + medium_count + large_count
            item_total = count_total * product.price
            total += item_total
            bag_items.append({
                'type': 'sized',
                'product': product,
                'small_count': small_count,
                'medium_count': medium_count,
                'large_count': large_count,
                'item_total': item_total,
            })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery_cost = settings.STANDARD_DELIVERY_COST
        delivery_shortfall = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery_cost = 0
        delivery_shortfall = 0

    grand_total = total + delivery_cost

    context = {
        'bag_items': bag_items,
        'num_of_items': len(bag_items),
        'total': total,
        'delivery_cost': delivery_cost,
        'delivery_shortfall': delivery_shortfall,
        'grand_total': grand_total,
    }

    return context
