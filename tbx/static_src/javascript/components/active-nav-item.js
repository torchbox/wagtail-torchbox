class ActiveNavItem {
    static selector() {
        return '[data-menu-item]';
    }

    constructor(node) {
        this.node = node;
        this.pathname = window.location.pathname;
        this.pageUrl = this.node.getAttribute('href');
        this.addCurrentClass();
    }

    addCurrentClass() {
        if (this.pathname.includes(this.pageUrl)) {
            this.node.classList.add('nav-item__link--active');
        }
    }
}

export default ActiveNavItem;
