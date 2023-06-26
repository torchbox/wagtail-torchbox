class ActiveNavItem {
    static selector() {
        return '[data-menu-item]';
    }

    constructor(node) {
        this.node = node;
        this.pathname = window.location.pathname;
        this.pageUrl = this.node.getAttribute('href');
        this.isSubnav = this.node.hasAttribute('data-subnav-menu-item');
        this.addCurrentClass();
    }

    addCurrentClass() {
        if (this.pathname.includes(this.pageUrl)) {
            if (this.isSubnav) {
                this.node.classList.add('subnav__link--active');
            } else {
                this.node.classList.add('nav-item__link--active');
            }
        }
    }
}

export default ActiveNavItem;
