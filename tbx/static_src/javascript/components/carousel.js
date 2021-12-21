import Glide from '@glidejs/glide';

class Carousel {
    static selector() {
        return '[data-carousel]';
    }

    constructor(node) {
        this.node = node;

        this.createSlideshow();
        this.slideTotal = this.node.dataset.slidetotal;
        this.slideshow.mount();
        this.bindEvents();
        this.setLiveRegion();
    }

    bindEvents() {
        this.updateAriaRoles();

        // Rerun after each slide move
        this.slideshow.on('run.after', () => {
            this.updateAriaRoles();
            this.updateLiveRegion();
        });
    }

    createSlideshow() {
        this.slideshow = new Glide(this.node, {
            type: 'slider',
            startAt: 0,
            gap: 0,
            keyboard: true,
            perTouch: 1,
            touchRatio: 0.5,
            perView: 1,
            rewind: false,
            autoplay: false,
        });
    }

    // sets aria-hidden on inactive slides
    updateAriaRoles() {
        // eslint-disable-next-line no-restricted-syntax
        for (const slide of this.node.querySelectorAll(
            '.glide__slide:not(.glide__slide--active)',
        )) {
            const inactiveSlideAnchors = slide.querySelectorAll('a');
            slide.setAttribute('aria-hidden', 'true');
            inactiveSlideAnchors.forEach((el) => {
                el.setAttribute('tabindex', -1);
            });
        }
        const activeSlide = this.node.querySelector('.glide__slide--active');
        const activeSlideAnchors = activeSlide.querySelectorAll('a');
        activeSlide.removeAttribute('aria-hidden');
        activeSlideAnchors.forEach((el) => {
            el.removeAttribute('tabindex');
        });
    }

    // Sets a live region. This will announce which slide is showing to screen readers when previous / next buttons clicked
    setLiveRegion() {
        const controls = this.node.querySelector('[data-glide-el="controls"]');
        const liveregion = document.createElement('div');
        liveregion.setAttribute('aria-live', 'polite');
        liveregion.setAttribute('aria-atomic', 'true');
        liveregion.setAttribute('class', 'slideshow__liveregion');
        liveregion.setAttribute('data-liveregion', true);
        controls.appendChild(liveregion);
    }

    // Update the live region that announces the next slide.
    updateLiveRegion() {
        this.node.querySelector(
            '[data-liveregion]',
        ).textContent = `Item ${this.slideshow.index} of ${this.slideTotal}`;
    }
}

export default Carousel;
