class SeeMorePosts {
    static selector() {
        return '[data-fetch-target]';
    }

    constructor(node) {
        this.nextPage = 2;
        this.seeMoreButton = node;
        this.targetNode = document.querySelector(
            `[data-fetch-destination="${node.dataset.fetchTarget}"]`,
        );
        this.MAX_PAGES = parseInt(
            this.targetNode.getAttribute('data-fetch-max-pages'),
            10,
        );
        this.url = new URL(node.baseURI);
        this.filter = new URLSearchParams(this.url.search).get('filter');

        this.bindEvents();
    }

    loadMorePostsAjax() {
        // set parameters
        const params = new URLSearchParams();
        if (this.filter != null) {
            params.set('filter', this.filter);
        }
        params.set('page', this.nextPage);
        this.url.search = params.toString();

        // build request object
        const request = new Request(this.url, {
            method: 'GET',
            headers: new Headers({
                'X-Requested-With': 'XMLHttpRequest',
            }),
        });

        fetch(request)
            .then((response) => {
                if (response.ok) {
                    // parse to html
                    return response.text();
                }
                throw new Error(`${response.status}: ${response.statusText}`);
            })
            .then((html) => {
                // update list
                this.targetNode.lastElementChild.insertAdjacentHTML(
                    'afterend',
                    html,
                );
                this.nextPage += 1;
                if (this.nextPage > this.MAX_PAGES) {
                    this.seeMoreButton.classList.add('see-more--hidden');
                }
            });
    }

    bindEvents() {
        this.seeMoreButton.addEventListener('click', (event) =>
            this.loadMorePostsAjax(event),
        );
    }
}

export default SeeMorePosts;
