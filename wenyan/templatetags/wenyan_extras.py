from atexit import register
from django import template
from django.utils.safestring import mark_safe

register=template.Library()

@register.filter
def highlight(example):
    """
    给example所属sentence中的appear部分添加class="highlight"
    """
    cur=0
    all_appears=example.appear_set.all()
    sentence_text=example.sentence.sentence_text
    output=''
    for appear in all_appears:
        output+=sentence_text[cur:appear.appear_begin]
        for i in range(appear.appear_begin,appear.appear_end):
            output+='<span class="highlight">'+sentence_text[i]+'</span>'
        # output+='<span class="highlight">'+sentence_text[appear.appear_begin:appear.appear_end]+'</span>'
        cur=appear.appear_end
    output+=sentence_text[cur:]
    return mark_safe(output)