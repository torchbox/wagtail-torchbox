addEventListener('fetch', (event) => {
    event.respondWith(main(event));
});

async function main(event) {
    const newRequest = stripSessionCookie(event.request);
    return fetch(newRequest);
}

/**
 * Strip session cookies from the front-end.
 *
 * It's important that you disable this script from:
 *  - /admin/*
 *  - /review/*
 *  - /contact/*
 *
 * Otherwise CSRF won't work.
 *
 */
function stripSessionCookie(request) {
    const newHeaders = new Headers(request.headers);
    const url = new URL(request.url);
    const cookieString = newHeaders.get('Cookie');
    if (
        cookieString !== null &&
        (cookieString.includes('csrftoken') ||
            cookieString.includes('sessionid'))
    ) {
        const newValue = stripCookie(
            stripCookie(newHeaders.get('Cookie'), 'sessionid'),
            'csrftoken',
        );
        newHeaders.set('Cookie', newValue);
        return new Request(request.url, {
            headers: newHeaders,
            method: request.method,
            body: request.body,
            redirect: request.redirect,
        });
    }

    return request;
}

/**
 * Strip a cookie from the cookie string and return a new cookie string.
 */
function stripCookie(cookiesString, cookieName) {
    return cookiesString
        .split(';')
        .filter((v) => {
            return v.split('=')[0].trim() !== cookieName;
        })
        .join(';');
}
