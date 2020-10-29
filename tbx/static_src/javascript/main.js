import '@babel/polyfill';

import CookieWarning from './components/cookie-message';
import './components/sticky-point';

import '../sass/main.scss';

document.addEventListener('DOMContentLoaded', () => {
    /* eslint-disable no-new */
    const cookie = document.querySelector(CookieWarning.selector());
    new CookieWarning(cookie);
});
