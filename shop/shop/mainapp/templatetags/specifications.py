from django import template

register = template.Library()


@register.filter
def product_spec(product):
    return str(product.category.slug) + '_specification.html'