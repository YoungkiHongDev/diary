'''
이 파일은 템플릿 필터 파일입니다.
templatetags 디렉터리는 반드시 앱 디렉터리 아래에 생성해야 합니다.
장고에는 빼기 필터가 없습니다. 그래서 빼기 필터를 만들었습니다.
'''

from django import template

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg