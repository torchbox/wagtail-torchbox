import Cookies from 'js-cookie';

class CookieWarning {
    static selector() {
        return '[data-cookie-message]';
    }

    constructor(node) {
        this.dismissButton = document.querySelector('[data-cookie-dismiss]');
        this.messageContainer = node;
        this.cookieName = 'torchbox-cookie';
        this.cookieValue = 'agree to cookies';
        this.cookieDuration = 365;
        this.activeClass = 'active';
        this.inactiveClass = 'inactive';

        this.checkCookie();
        this.bindEvents();
    }

    checkCookie() {
        if (!this.messageContainer) {
            return;
        }

        // If cookie doesn't exists
        if (!Cookies.get(this.cookieName)) {
            this.messageContainer.classList.add(this.activeClass);
        }
    }

    applyCookie(event) {
        // prevent default link action
        event.preventDefault();
        // Add classes
        this.messageContainer.classList.remove(this.activeClass);
        this.messageContainer.classList.add(this.inactiveClass);
        // Set cookie
        Cookies.set(this.cookieName, this.cookieValue, {
            expires: this.cookieDuration,
        });
    }

    bindEvents() {
        if (!this.dismissButton) {
            return;
        }

        this.dismissButton.addEventListener('click', (event) =>
            this.applyCookie(event),
        );
    }
}

export default CookieWarning;
