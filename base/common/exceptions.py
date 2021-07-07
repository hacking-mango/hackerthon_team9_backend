from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    incorrect_status_code_list = [400, 401, 403, 404, 405, 429, 500]

    if response is not None:
        if response.status_code in incorrect_status_code_list:
            del response.data["detail"]
            response.data["success"] = 0
            response.data["data"] = {"code": exc.get_codes(), "message": exc.detail}

    return response
