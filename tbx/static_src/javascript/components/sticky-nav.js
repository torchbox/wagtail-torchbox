import 'intersection-observer';
import scrollama from 'scrollama';

function scrollamaInit() {
    // instantiate the scrollama
    const scroller = scrollama();

    // setup the instance, pass callback functions
    scroller
        .setup({
            step: '[data-sticky-nav]',
            offset: '20px',
        })
        .onStepEnter((response) => {
            if (response.direction === 'down') {
                document.body.classList.add('nav-stuck');
            }
        })
        .onStepExit((response) => {
            if (response.direction === 'up') {
                document.body.classList.remove('nav-stuck');
            }
        });

    // setup resize event
    window.addEventListener('resize', scroller.resize);
}

if (document.body.contains(document.querySelector('[data-sticky-nav]'))) {
    scrollamaInit();
}
