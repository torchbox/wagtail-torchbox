## Using Unsplash Source for placeholder images

Images can be queried using the url `https://source.unsplash.com` followed by the endpoints `/random`, `/featured`, `/user/{USERNAME}`, `/collection/{COLLECTION ID}` and `/{PHOTO ID}`.

Image sizes can be specified by appending to the end of the url, `https://source.unsplash.com/random/1080x720`.

Search terms can be also be applied to all endpoints with the exception of `{PHOTO ID}` by providing a comma separated list after a question mark, `https://source.unsplash.com/random/?mountain,forest`.

For more information about each endpoint see https://source.unsplash.com/.

Source is built for "small, low-traffic applications". If you want to use Unsplash in production, outside of the pattern-library, use the official Unsplash API. By creating a developer account you will also have access to more features such as lists, pagination, statistics and authentication. For more information look at the Unsplash API [documentation](https://unsplash.com/documentation) and consider using [wagtail-unsplash](https://github.com/jafacakes2011/wagtail-unsplash).
