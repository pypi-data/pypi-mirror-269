# Tabbed StrucBlock
### A new UI for StrucBlocks

As custom blocks grow in fields it becomes necessary to group and hide some of the block fields. Tabbed StrucBlock allows such grouping into a tabbed UI.


## Installation

1. Install the package with `pip install wagtail-tabbed-strucblock`.
2. Add to `INSTALLED_ADD` as `wagtail_tabbed_structblock`.


## Usage

1. Import the class with `from wagtail_tabbed_structblock.blocks import TabbedStructBlock`.
2. Create your `StructBlock` as usual extending `TabbedStructBlock`.
3. Define the tabs in the `Meta` class of the block as shown in the example below.

```python
from wagtail import blocks

from wagtail_tabbed_structblock.blocks import TabbedStructBlock


class ExampleBlock(TabbedStructBlock):
    title = blocks.CharBlock()
    content = blocks.RichTextBlock()


    class Meta:
        tabs = {
            'Header': ('title',),
            'Body': ('content',)
        }
```

The `tabs` property of the `Meta` class is a dictionary composed of the title of the tab and a tuple of the fields you want to include on that tab.