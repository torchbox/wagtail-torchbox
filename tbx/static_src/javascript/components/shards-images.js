class ShardsImages {
    static selector() {
        return '[data-shards-hero]';
    }

    constructor(node) {
        this.node = node;
        this.imageTotal = this.node.dataset.imagetotal;
        this.images = node.querySelector('[data-shards-images]').children;
        this.showRandomImage();
    }

    showRandomImage() {
        const randomNumber = Math.floor(Math.random() * this.imageTotal);
        const image = this.images[randomNumber];
        image.classList.add('shards__image--visible');
    }
}

export default ShardsImages;
