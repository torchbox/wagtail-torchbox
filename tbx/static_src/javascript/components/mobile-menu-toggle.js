class MobileMenuToggle {
    static selector() {
        return '[data-menu-toggle]';
    }

    constructor(node) {
        this.node = node;
        this.body = document.querySelector('body');
        this.noScrollClass = 'no-scroll';
        this.activeClass = `${this.node.dataset.active}-active`;

        this.bindEventListeners();
    }

    bindEventListeners() {
        this.node.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggle();
        });
    }

    toggle() {
        // if the menu is open
        if (this.body.classList.contains(this.activeClass)) {
            if (this.node.dataset.active === 'menu') {
                this.node.setAttribute('aria-expanded', false);
                this.close();
            }
        } else {
            // open the menu
            this.node.setAttribute('aria-expanded', true);
            this.open();
        }
    }

    open() {
        this.body.classList.add(this.activeClass, this.noScrollClass);
    }

    close() {
        this.body.classList.remove(this.activeClass, this.noScrollClass);
    }
}

export default MobileMenuToggle;
