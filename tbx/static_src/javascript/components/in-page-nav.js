class InPageNav {
    static selector() {
        return '[data-in-page-nav]';
    }

    constructor(node) {
        this.node = node;

        this.allSections = document.querySelectorAll('[data-service-section]');
        this.allMenuLinks = this.node.querySelectorAll('[data-in-page-nav] a');
        this.sentinelEl = document.getElementById('sentinel');

        this.initObserving();
        this.bindEvents();
    }

    initObserving() {
        const config = {
            // A string with values in the same format as for a CSS margin or padding value.
            // This will fire when the section is at the top of the viewport.
            rootMargin: '0px 0px -90%',
        };

        // setup IO and add a callback if the section enters
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    this.handleEntry(entry.target);
                }
            });
        }, config);

        // Observe all the sections
        this.allSections.forEach((section) => {
            observer.observe(section);
        });
    }

    bindEvents() {
        this.allMenuLinks.forEach((link) => {
            link.addEventListener('click', (e) => {
                this.resetMenuLinks();
                e.target.classList.add('is-active');
            });
        });
    }

    handleEntry(sectionInView) {
        this.resetMenuLinks();

        // get the id of the section that is active
        const sectionId = sectionInView.id;

        // use to find the relevant menu item
        const menuItem = this.node.querySelector(`a[href="#${sectionId}"]`);

        // activate it
        menuItem.classList.add('is-active');
    }

    resetMenuLinks() {
        this.allMenuLinks.forEach((menuLink) => {
            menuLink.classList.remove('is-active');
        });
    }
}

export default InPageNav;
