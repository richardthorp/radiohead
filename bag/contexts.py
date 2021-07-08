from shop.models import Album, Product


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
            cd_count = bag[item].get('cd', 0)
            vinyl_count = bag[item].get('vinyl', 0)
            cd_total = cd_count * product.cd_price
            vinyl_total = vinyl_count * product.vinyl_price
            item_total = cd_total + vinyl_total
            total += item_total
            bag_items.append({
                'type': 'album',
                'product': product,
                'cd_count': cd_count,
                # 'cd_total': cd_total,
                'vinyl_count': vinyl_count,
                'item_total': item_total,
                # 'vinyl_total': vinyl_total,
            })

        elif bag[item]['type'] == 'sized':
            product = Product.objects.get(name=item)
            small_count = bag[item].get('S', 0)
            medium_count = bag[item].get('M', 0)
            large_count = bag[item].get('L', 0)
            count_total = small_count + medium_count + large_count
            item_total = count_total * product.price
            total += item_total
            bag_items.append({
                'type': 'sized',
                'product': product,
                'small_count': small_count,
                # 'small_total': small_count * product.price,
                'medium_count': medium_count,
                # 'medium_total': medium_count * product.price,
                'large_count': large_count,
                # 'large_total': large_count * product.price,
                'item_total': item_total,
            })

    context = {
        'bag_items': bag_items,
        'num_of_items': len(bag_items),
        'total': total,
    }

    return context
