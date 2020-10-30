class MobileMenuToggle {
    static selector() {
        return '[data-menu-toggle]';
    }

    constructor(node) {
        this.node = node;
        this.body = document.querySelector('body');
        this.closeIcon = document.querySelector('[data-close-menu]');
        this.drawerOpenClass = 'nav-open';
        this.menuOpenClass = 'menu-active';
        this.searchOpenClass = 'search-active';
        this.noScrollClass = 'no-scroll';
        this.activeClass = `${this.node.dataset.active}-active`;

        this.bindEventListeners();
    }

    bindEventListeners() {
        this.node.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggle();
        });

        this.closeIcon.addEventListener('click', (e) => {
            e.preventDefault();
            this.close();
        });

        // close menu on overlay click
        document.addEventListener('click', (e) => {
            if (
                this.body.classList.contains('nav-open') &&
                e.target.classList.contains('header__menus')
            ) {
                this.close();
            }
        });
    }

    toggle() {
        // if the drawer is open
        if (this.body.classList.contains(this.drawerOpenClass)) {
            // and search is clicked
            if (this.node.dataset.active === 'search') {
                // activate it
                if (!this.body.classList.contains(this.searchOpenClass)) {
                    this.body.classList.remove(this.menuOpenClass);
                    this.body.classList.add(this.searchOpenClass);
                }
                // and menu is clicked
            } else if (this.node.dataset.active === 'menu') {
                // activate it
                if (!this.body.classList.contains(this.menuOpenClass)) {
                    this.body.classList.remove(this.searchOpenClass);
                    this.body.classList.add(this.menuOpenClass);
                }
            }
        } else {
            // open the drawer
            this.open();
        }
    }

    open() {
        this.body.classList.add(
            this.drawerOpenClass,
            this.activeClass,
            this.noScrollClass,
        );
    }

    close() {
        this.body.classList.remove(
            this.drawerOpenClass,
            this.activeClass,
            this.noScrollClass,
        );

        this.resetMenu();
    }

    resetMenu() {
        const visibleItems = document.querySelectorAll(
            '[data-nav-container] .is-visible',
        );

        const activeItems = document.querySelectorAll(
            '[data-nav-container] .is-active',
        );

        visibleItems.forEach((item) => {
            item.classList.remove('is-visible');
        });

        activeItems.forEach((item) => {
            item.classList.remove('is-active');
        });
    }
}

export default MobileMenuToggle;
