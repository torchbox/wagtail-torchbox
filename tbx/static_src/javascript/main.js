import '@babel/polyfill';
import Alpine from 'alpinejs';

import CookieWarning from './components/cookie-message';
import ConsoleMessage from './components/console-message';
import SeeMorePosts from './components/see-more-posts';
import Carousel from './components/carousel';
import MobileMenuToggle from './components/mobile-menu-toggle';
import './components/sticky-point';
import './components/sticky-nav';
import InPageNav from './components/in-page-nav';
import ActiveNavItem from './components/active-nav-item';
import ShardsImages from './components/shards-images';
import PrimaryNav from './components/primary-nav';

import '../sass/main.scss';

window.Alpine = Alpine;
Alpine.start();

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then((registrations) => {
        registrations.forEach((registration) => {
            registration.unregister();
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    /* eslint-disable no-new, no-restricted-syntax */

    for (const cookie of document.querySelectorAll(CookieWarning.selector())) {
        new CookieWarning(cookie);
    }
    for (const seeMore of document.querySelectorAll(SeeMorePosts.selector())) {
        new SeeMorePosts(seeMore);
    }
    for (const carousel of document.querySelectorAll(Carousel.selector())) {
        new Carousel(carousel);
    }

    for (const mobilemenutoggle of document.querySelectorAll(
        MobileMenuToggle.selector(),
    )) {
        new MobileMenuToggle(mobilemenutoggle);
    }

    for (const inpagenav of document.querySelectorAll(InPageNav.selector())) {
        new InPageNav(inpagenav);
    }

    for (const primarynav of document.querySelectorAll(PrimaryNav.selector())) {
        new PrimaryNav(primarynav);
    }

    for (const activenavitem of document.querySelectorAll(
        ActiveNavItem.selector(),
    )) {
        new ActiveNavItem(activenavitem);
    }

    for (const shardsimages of document.querySelectorAll(
        ShardsImages.selector(),
    )) {
        new ShardsImages(shardsimages);
    }

    ConsoleMessage();
});
