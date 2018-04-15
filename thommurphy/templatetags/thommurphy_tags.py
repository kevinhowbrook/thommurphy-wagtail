import random

from django import template
from django.conf import settings
from django.template import TemplateSyntaxError

from wagtail.core.utils import camelcase_to_underscore


register = template.Library()

@register.assignment_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page


def has_menu_children(page):
    if page.get_children().live().in_menu():
        return True
    else:
        return False


# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the bootstrap menu requires
# a dropdown class to be applied to a parent
@register.inclusion_tag('thommurphy/tags/menu_primary.html', takes_context=True)
def menu_primary(context, parent=None):
    menuitems = parent.get_children().live().in_menu()

    # Use get_navigation_menu_items() ?

    for menuitem in menuitems:
        menuitem.has_children = has_menu_children(menuitem)
        menuitem.is_active = False
        if context['request'].path.startswith(menuitem.url):
            menuitem.is_active = True

    return {
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag('thommurphy/tags/menu_children.html', takes_context=True)
def menu_children(context, parent):
    menuitems_children = parent.get_children().live().in_menu()

    for menuitem in menuitems_children:
        menuitem.is_active = False
        if context['request'].path.startswith(menuitem.url):
            menuitem.is_active = True

    return {
        'parent': parent,
        'menuitems_children': menuitems_children,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }

