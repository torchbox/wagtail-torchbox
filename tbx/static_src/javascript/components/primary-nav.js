import { enableBodyScroll, disableBodyScroll } from 'body-scroll-lock';

class PrimaryNav {
    static selector() {
        return '[data-primary-nav]';
    }

    constructor(node) {
        this.node = node;
        this.open = false;
        this.button = node.querySelector('.nav-item__button');
        this.overlay = node.querySelector('.nav-item__background-overlay');
        this.navLinks = node.querySelectorAll('.subnav__link');
        this.lastNavLink = this.navLinks[this.navLinks.length - 1];
        this.lastNavLinkKeyEvents = [];

        this.addEventListeners();
    }

    addEventListeners() {
        const clickToggleBackgroundScrolling = () => {
            if (this.open) {
                enableBodyScroll(this.node);
            } else {
                disableBodyScroll(this.node);
            }
            this.open = !this.open;
        };

        const keyDownToggleBackgroundScrolling = (event) => {
            if (event.code === 'Enter') {
                if (this.open) {
                    enableBodyScroll(this.node);
                } else {
                    disableBodyScroll(this.node);
                }
                this.open = !this.open;
            }
        };

        // Used to check if the user wishes to tab out of the menu.
        const lastNavLinkKeyLogger = (event) => {
            this.lastNavLinkKeyEvents.push(event.code);

            if (
                this.lastNavLinkKeyEvents.includes('ShiftLeft') ||
                this.lastNavLinkKeyEvents.includes('ShiftRight')
            ) {
                return;
            }

            if (this.lastNavLinkKeyEvents.includes('Tab')) {
                enableBodyScroll(this.node);
                this.open = !this.open;
                this.node.setAttribute('x-data', '{ isOpen: false }');
            }
        };

        const lastNavLinkKeyRemover = (event) => {
            const index = this.lastNavLinkKeyEvents.indexOf(event.code);
            if (index > -1) {
                this.lastNavLinkKeyEvents.splice(index, 1);
            }
        };

        this.button.addEventListener('click', clickToggleBackgroundScrolling);
        this.overlay.addEventListener('click', clickToggleBackgroundScrolling);
        this.button.addEventListener(
            'keydown',
            keyDownToggleBackgroundScrolling,
        );
        this.lastNavLink.addEventListener('keydown', lastNavLinkKeyLogger);
        this.lastNavLink.addEventListener('keyup', lastNavLinkKeyRemover);
    }
}

export default PrimaryNav;
