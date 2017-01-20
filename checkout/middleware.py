from checkout.models import CartItem


def cart_item_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        session_key = request.session.session_key
        response = get_response(request)
        if session_key != request.session.session_key and request.session.session_key:
            CartItem.objects.filter(cart_key=session_key).update(cart_key=request.session.session_key)and request.session.session_key

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
