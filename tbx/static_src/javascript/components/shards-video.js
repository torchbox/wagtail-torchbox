class ShardsVideo {
    static selector() {
        return '[data-shards-video-wrap]';
    }

    constructor(node) {
        this.node = node;
        this.button = this.node.querySelector('[data-shards-video-button]');
        this.video = this.node.querySelector('[data-shards-video]');
        this.videoSource = this.video.querySelector('source');
        this.shouldLoadVideo();
        this.bindEvents();
    }

    shouldLoadVideo() {
        // only load the video above the large breakpoint
        if (window.matchMedia('(min-width: 1023px)').matches) {
            this.videoSource.src = this.videoSource.getAttribute('data-src');
            this.video.load();
            this.node.classList.add('video-loaded');
        }
    }

    bindEvents() {
        this.node.addEventListener('click', () => {
            if (this.video.paused) {
                this.video.play();
            } else {
                this.video.pause();
            }
        });

        // Show a fallback image if the video fails to load
        this.videoSource.addEventListener('error', () => {
            this.node.classList.add('video-error');
        });
    }
}

export default ShardsVideo;
