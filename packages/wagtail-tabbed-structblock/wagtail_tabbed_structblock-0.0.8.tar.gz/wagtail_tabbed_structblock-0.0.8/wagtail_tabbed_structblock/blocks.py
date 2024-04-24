from django import forms
from django.utils.functional import cached_property
from wagtail import blocks
from wagtail.admin.staticfiles import versioned_static
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.telepath import register


class TabbedStructBlock(blocks.StructBlock):
    def get_form_context(self, value, prefix="", errors=None):
        context = super().get_form_context(value, prefix, errors)
        return context

    class Meta:
        form_classname = "tabbed-struct-block"
        form_template = "wagtail_tabbed_structblock/tabbed_struct_block.html"
        tabs = {}


class TabbedStructBlockAdapter(StructBlockAdapter):
    js_constructor = "website.blocks.TabbedStructBlock"

    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + [versioned_static("wagtail_tabbed_structblock/js/tabbed_structblock.js")],
            css={"all": (versioned_static("wagtail_tabbed_structblock/css/tabbed_structblock.css"),)},
        )


register(TabbedStructBlockAdapter(), TabbedStructBlock)
