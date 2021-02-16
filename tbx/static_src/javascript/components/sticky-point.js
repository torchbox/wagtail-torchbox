import 'intersection-observer';
import scrollama from 'scrollama';

function scrollamaInit() {
    // instantiate the scrollama
    const scroller = scrollama();

    // setup the instance, pass callback functions
    scroller
        .setup({
            step: '[data-sticky-point]',
            offset: 0,
        })
        .onStepEnter(() => {
            document.body.classList.add('sticky');
        })
        .onStepExit(() => {
            document.body.classList.remove('sticky');
        });

    // setup resize event
    window.addEventListener('resize', scroller.resize);
}

if (document.body.contains(document.querySelector('[data-sticky-point]'))) {
    scrollamaInit();
}
