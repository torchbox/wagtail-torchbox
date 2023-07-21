class ShardsImages {
    static selector() {
        return '[data-shards-hero]';
    }

    constructor(node) {
        this.node = node;
        this.imageTotal = node.dataset.imagetotal;
        this.images = node.querySelectorAll('[data-shards-image]');
        this.showRandomImage();
    }

    showRandomImage() {
        const randomNumber = Math.floor(Math.random() * this.imageTotal);
        const image = this.images[randomNumber];
        image.classList.add('shards__image--visible');
    }
}

export default ShardsImages;
