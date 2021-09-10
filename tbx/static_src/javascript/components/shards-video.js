class ShardsVideo {
    static selector() {
        return '[data-shards-video-wrap]';
    }

    constructor(node) {
        this.node = node;
        this.button = this.node.querySelector('[data-shards-video-button]');
        this.video = this.node.querySelector('[data-shards-video]');
        this.bindEvents();
    }

    bindEvents() {
        this.node.addEventListener('click', () => {
            if (this.video.paused) {
                this.video.play();
            } else {
                this.video.pause();
            }
        });
    }
}

export default ShardsVideo;
