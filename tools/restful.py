from flask import jsonify

ok = 200
unautherror = 401
paramserror = 400
servererror = 500


def restful_result(code, message, data):
    return jsonify({
        'code': code,
        'message': message,
        'data': data or {}
    })


def success(message="", data=None):
    return restful_result(ok, message, data)


def unauth_error(message=""):
    return restful_result(unautherror, message, None)


def params_error(message=""):
    return restful_result(paramserror, message, None)


def server_error(message=""):
    return restful_result(servererror, message, None)
