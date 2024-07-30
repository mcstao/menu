from django import template
from menu_app.models import Menu, MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path
    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        return ''

    items = MenuItem.objects.filter(menu=menu).select_related('main_item')

    def build_tree(main_item=None):
        nodes = []
        for item in items:
            if item.main_item == main_item:
                sub_items = build_tree(item)
                nodes.append({
                    'item': item,
                    'sub_items': sub_items,
                    'is_active': current_url.startswith(item.get_url()),
                    'is_expanded': current_url.startswith(item.get_url()) or any(
                        current_url.startswith(sub_item['item'].get_url()) for sub_item in sub_items)
                })
        return nodes

    menu_tree = build_tree()
    context['menu'] = menu_tree
    return ''
