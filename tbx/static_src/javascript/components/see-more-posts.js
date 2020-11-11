class SeeMorePosts {
  static selector() {
    return "[data-fetch-destination]";
  }

  constructor(node) {
    this.node = node;
    this.target = this.node.dataset.fetchDestination;
    this.seeMoreButton = document.querySelector(`[data-fetch-target="${this.target}"]`);
    this.targetNode = document.querySelector(
      `[data-fetch-destination="${this.target}"]`
    );

    this.url = new URL(this.node.baseURI);
    this.params = new URLSearchParams(this.url.search);
    this.nextPage = 2;
    this.filter = this.params.get("filter");

    this.bindEvents();
  }

  loadMorePostsAjax() {
    //set parameters
    this.params = new URLSearchParams();
    if (this.filter != null) {
      this.params.set('filter', this.filter);
    }
    this.params.set('page', this.nextPage);
    this.url.search = this.params.toString();

    // build request object
    const request = new Request(this.url, {
      method: "GET",
      headers: new Headers({
        "X-Requested-With": "XMLHttpRequest",
      }),
    });

    fetch(request)
      .then((response) => {
        if (response.ok) {
          // parse to html
          return response.text();
        }
        throw new Error(response.status + ": " + response.statusText);
      })
      .then((html) => {
        if (html.trim().length > 0) {
          this.targetNode.lastElementChild.insertAdjacentHTML('afterend', html);
          this.nextPage += 1;
        } else {
          // handle empty response
          this.seeMoreButton.parentNode.removeChild(this.seeMoreButton);
        }
      })
  }

  bindEvents() {
    this.seeMoreButton.addEventListener("click", (event) =>
      this.loadMorePostsAjax(event)
    );
  }
}

export default SeeMorePosts;
