// get the sticky element
const stickyElm = document.querySelector('[data-in-page-nav]');

const observer = new IntersectionObserver(
    ([e]) =>
        e.target.classList.toggle(
            'in-page-nav--stuck',
            e.intersectionRatio < 1,
        ),
    { threshold: [1] },
);

if (document.body.contains(document.querySelector('[data-in-page-nav]'))) {
    observer.observe(stickyElm);
}
