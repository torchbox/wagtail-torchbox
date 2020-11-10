class SeeMorePosts {
  static selector() {
    return "[data-posts-destination]";
  }

  constructor(node) {
    this.node = node;
    this.seeMoreButton = document.querySelector("[data-posts-fetch-target]");
    this.target = this.node.dataset.postsDestination;
    this.targetNode = document.querySelector(
      `[data-posts-destination="${this.target}"]`
    );
    console.log(this.targetNode);
    this.url = new URL(this.node.baseURI);
    this.params = new URLSearchParams(this.url.search);
    this.page = parseInt(this.params.get("page")) || 1;
    this.filter = this.params.get("filter");

    this.bindEvents();
  }

  loadMorePostsAjax() {
    const targetNode = this.targetNode;
    // page counter
    let pageCtr = this.page;
    ++pageCtr;

    //set parameters
    this.params = new URLSearchParams();
    if (this.filter !=null){
        this.params.set('filter', this.filter);
    }
    this.params.set('page', pageCtr);
    this.url.search = this.params.toString();

    // build request object
    const request = new Request(this.url, {
      method: "GET",
      headers: new Headers({
        "X-Requested-With": "XMLHttpRequest",
      }),
    });

    fetch(request)
      .then(function (response) {
        // parse to html
        return response.text();
      })
      .then(function (html) {
        // Here you get the data to modify as you please
        targetNode.lastElementChild.insertAdjacentHTML('afterend', html);

      })
      .catch(function (error) {
        // If there is any error you will catch them here
        console.log(error);
        --pageCtr;
      });

    // update counter
    if (pageCtr != this.page) {
      this.page = pageCtr;
    }
  }

  bindEvents() {
    if (!this.seeMoreButton) {
      return;
    }

    this.seeMoreButton.addEventListener("click", (event) =>
      this.loadMorePostsAjax(event)
    );
  }
}

export default SeeMorePosts;
