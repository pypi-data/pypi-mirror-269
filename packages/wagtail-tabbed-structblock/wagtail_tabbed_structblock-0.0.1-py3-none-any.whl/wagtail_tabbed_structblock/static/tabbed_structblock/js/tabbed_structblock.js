class TabbedStructBlockDefinition extends window.wagtailStreamField.blocks.StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(
            placeholder,
            prefix,
            initialState,
            initialError,
        );

        this.initializeBlock(prefix);

        return block;
    }

    initializeBlock(prefix) {
        const tabsContainer = document.querySelector(`div[data-prefix=${prefix}].tabs`)
        tabsContainer.addEventListener('click', this.handleTabClick.bind(this))
        this.showTabGroup(prefix, tabsContainer.firstElementChild.dataset.group);
    }

    handleTabClick(e) {
        e.preventDefault();
        const { prefix, group } = e.target.dataset
        this.showTabGroup(prefix, group);
    }

    showTabGroup(prefix, group) {
        const fields = document.querySelectorAll(`div[data-prefix=${prefix}].w-field`)
        const tabs = document.querySelectorAll(`.tabs a[data-prefix=${prefix}]`)

        fields.forEach((field) => {
            if (field.dataset.group === group) {
                field.style.display = "block"
            } else {
                field.style.display = "none"
            }
        })

        tabs.forEach((tab) => {
            if (tab.dataset.group === group) {
                tab.classList.add('active')
            } else {
                tab.classList.remove('active')
            }
        })
    }
}

window.telepath.register('website.blocks.TabbedStructBlock', TabbedStructBlockDefinition);