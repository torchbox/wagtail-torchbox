import '@babel/polyfill';

import CookieWarning from './components/cookie-message';
import Carousel from './components/carousel';
import MobileMenuToggle from './components/mobile-menu-toggle';
import './components/sticky-point';
import './components/in-page-nav';

import '../sass/main.scss';

document.addEventListener('DOMContentLoaded', () => {
    /* eslint-disable no-new, no-restricted-syntax */

    for (const cookie of document.querySelectorAll(CookieWarning.selector())) {
        new CookieWarning(cookie);
    }

    for (const carousel of document.querySelectorAll(Carousel.selector())) {
        new Carousel(carousel);
    }

    for (const mobilemenutoggle of document.querySelectorAll(
        MobileMenuToggle.selector(),
    )) {
        new MobileMenuToggle(mobilemenutoggle);
    }
});
