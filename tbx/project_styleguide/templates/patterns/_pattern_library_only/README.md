# Pattern library only templates

This directory contains templates that we are going to use
only in the pattern library.

For example, we can have a pattern template for evry Wagtail streamfield
block and one pattern that contains wrapper layout for
all streamfield blocks.

It doesn't make much sense to render wrapper layout separately,
because it's not visible for a user. Instead we want to render it
with all possible streamfield blocks. To do that we need a temporary
template that will include all possible streamfield blocks.
But we don't want this template to be shown in the pattern listing.
So we put this template here.
