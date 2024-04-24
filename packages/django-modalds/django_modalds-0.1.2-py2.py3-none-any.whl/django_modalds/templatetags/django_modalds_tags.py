from django.template import Library
from ..models import Type5, Type4, Type3, Type2, Type1


register = Library()

# https://localcoder.org/django-inclusion-tag-with-configurable-template


@register.inclusion_tag(f"django_modalds/modalds.html")
def show_modal():
    popup = None
    try:
        # 활성화된 type5에서 하나(제일 처음 것)을 선택함.
        popup = Type5.objects.filter(activate__exact=True)[0]
        print(f"Activated {Type5.__name__} objects : {popup}")
    except IndexError:
        pass

    try:
        # 활성화된 type4에서 하나(제일 처음 것)을 선택함.
        popup = Type4.objects.filter(activate__exact=True)[0]
        print(f"Activated {Type4.__name__} objects : {popup}")
    except IndexError:
        pass

    try:
        # 활성화된 type3에서 하나(제일 처음 것)을 선택함.
        popup = Type3.objects.filter(activate__exact=True)[0]
        print(f"Activated {Type3.__name__} objects : {popup}")
    except IndexError:
        pass

    try:
        # 활성화된 type2에서 하나(제일 처음 것)을 선택함.
        popup = Type2.objects.filter(activate__exact=True)[0]
        print(f"Activated {Type2.__name__} objects : {popup}")
    except IndexError:
        pass

    try:
        # 활성화된 type1에서 하나(제일 처음 것)을 선택함.
        popup = Type1.objects.filter(activate__exact=True)[0]
        print(f"Activated {Type1.__name__} objects : {popup}")
    except IndexError:
        pass

    context = {
        "dont_show_again": "다시보지않기",
        "type": popup.__class__.__name__,
        "popup": popup,
    }
    print("popup context: ", context)
    return context
