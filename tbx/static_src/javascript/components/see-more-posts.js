class SeeMorePosts {
    static selector() {
        return '[data-posts-destination]';
    }

    constructor(node) {
        this.seeMoreButton = document.querySelector('[data-fetch-target]');
        this.url= new URL(window.location);
        this.params=new URLSearchParams(this.url.search);
        this.page=parseInt(this.params.get('page')) || 1;
        this.filter=this.params.get('filter');
        this.xmlhttp=null;

        this.bindEvents();
    }

    loadMorePostsAjax(){
        this.page+=1;
        this.xmlhttp = new XMLHttpRequest();
        this.xmlhttp.onreadystatechange = this.loadMorePostsAjaxCallBack;

        //set parameters
        this.params = new URLSearchParams();
        this.params.set('filter', this.filter);
        this.params.set('page', this.page);
        this.url.search = this.params.toString();


        this.xmlhttp.open("GET", this.url, true);
        // set header to make it AjaxRequest
        this.xmlhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        this.xmlhttp.send();
    }

    loadMorePostsAjaxCallBack(){
      if (this.readyState == 4 && this.status == 200) {
      // if success
        console.log(this.responseText);
        }else if(this.readyState == 4){
        // if error
        this.page-=1;
        }
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
