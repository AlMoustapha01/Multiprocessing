from django import template

register = template.Library()
@register.filter(name='total')
def total(prix,quantity):
    montant = int(prix.replace(' ',''))
    return montant*quantity

def somme(prix1,prix2):
    return int(prix1.replace(' ',''))+ int(prix2.replace(' ',''))