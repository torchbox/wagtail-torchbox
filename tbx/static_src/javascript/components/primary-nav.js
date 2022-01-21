import { enableBodyScroll, disableBodyScroll } from 'body-scroll-lock';

class PrimaryNav {
    static selector() {
        return '[data-primary-nav]';
    }

    constructor(node) {
        this.node = node;
        this.open = false;
        this.button = node.querySelector('[data-subnav-button]');
        this.overlay = node.querySelector('[data-subnav-background-overlay]');
        this.navLinks = node.querySelectorAll('[data-subnav-link]');
        this.badgeLinks = node.querySelectorAll('[data-subnav-badge-link]');
        this.lastNavLink = this.navLinks[this.navLinks.length - 1];
        this.navLinkKeyEvents = [];

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

        // Checking if the user wishes to tab out of the top of the menu
        const tabOutOfTopOfMenu = (event) => {
            this.navLinkKeyEvents.push(event.code);

            if (
                this.navLinkKeyEvents.includes('ShiftLeft') ||
                this.navLinkKeyEvents.includes('ShiftRight')
            ) {
                if (this.navLinkKeyEvents.includes('Tab')) {
                    enableBodyScroll(this.node);
                    this.open = !this.open;

                    // Send a custom event to the alpine component to close the subnav
                    // https://devdojo.com/tnylea/setting-alpine-data-outside-of-the-component
                    this.node.dispatchEvent(
                        new CustomEvent('tab-close', { detail: {} }),
                    );

                    // Reset stored events as we won't receive the shift up event
                    // this is because the focus has left the nav list so there's nothing listening for it
                    this.navLinkKeyEvents = [];
                }
            }
        };

        const tabOutOfBottomOfMenu = (event) => {
            this.navLinkKeyEvents.push(event.code);

            if (
                this.navLinkKeyEvents.includes('ShiftLeft') ||
                this.navLinkKeyEvents.includes('ShiftRight')
            ) {
                return;
            }

            if (this.navLinkKeyEvents.includes('Tab')) {
                enableBodyScroll(this.node);
                this.open = !this.open;

                // Send a custom event to the alpine component to close the subnav
                // https://devdojo.com/tnylea/setting-alpine-data-outside-of-the-component
                this.node.dispatchEvent(
                    new CustomEvent('tab-close', { detail: {} }),
                );
            }
        };

        const navLinkKeyLogger = (event) => {
            const index = this.navLinkKeyEvents.indexOf(event.code);
            if (index === -1) {
                this.navLinkKeyEvents.push(event.code);
            }
        };

        const navLinkKeyRemover = (event) => {
            const index = this.navLinkKeyEvents.indexOf(event.code);
            if (index > -1) {
                this.navLinkKeyEvents.splice(index, 1);
            }
        };

        this.button.addEventListener('click', clickToggleBackgroundScrolling);
        this.overlay.addEventListener('click', clickToggleBackgroundScrolling);
        this.button.addEventListener(
            'keydown',
            keyDownToggleBackgroundScrolling,
        );

        this.navLinks[0].addEventListener('keydown', tabOutOfTopOfMenu);
        this.lastNavLink.addEventListener('keydown', tabOutOfBottomOfMenu);

        for (let i = 0; i < this.navLinks.length; i += 1) {
            this.navLinks[i].addEventListener('keyup', navLinkKeyRemover);

            // Log keydown all throughout the menu items as at any point in the list the user
            // can press and hold shift and start going back up through menu items
            this.navLinks[i].addEventListener('keydown', navLinkKeyLogger);
        }

        // As we can tab to badges, we have to listen for keyboard events on them as well
        // There was a bug of holding shift and tabbing back to the badge, then releasing shift and tabbing forwards
        // as a result, the menu wouldn't close as it thinks the user is still holding shift
        for (let i = 0; i < this.badgeLinks.length; i += 1) {
            this.badgeLinks[i].addEventListener('keyup', navLinkKeyRemover);
            this.badgeLinks[i].addEventListener('keydown', navLinkKeyLogger);
        }
    }
}

export default PrimaryNav;
