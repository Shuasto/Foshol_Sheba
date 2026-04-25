from django import template

register = template.Library()

@register.filter(name='bn_number')
def bn_number(value):
    bn_digits = {
        '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪',
        '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'
    }
    return ''.join(bn_digits.get(d, d) for d in str(value))

register.filter('bn_numbers', bn_number)
