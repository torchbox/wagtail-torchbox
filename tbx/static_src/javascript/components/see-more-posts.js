class SeeMorePosts {
    static selector() {
        return '[data-posts-destination]';
    }

    constructor(node) {
        this.seeMoreButton = document.querySelector('[data-posts-see-more]');
        this.url= new URL('{{request.build_absolute_uri}}');
        this.page = parseInt('{{request.GET.page}}') || 1;
        this. filter = '{{request.GET.filter}}';
        console.log(this.url);
        this.messageContainer = node;

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

    loadMorePostsAjax(){

    }

    bindEvents() {
        if (!this.seeMoreButton) {
            return;
        }

        this.seeMoreButton.addEventListener('click', (event) =>
            this.loadMorePostsAjax(event),
        );
    }
}

export default SeeMorePosts;
