from django.http import JsonResponse


def success_response(mensaje, data=None, status=200):
    return JsonResponse({
        "ok": True,
        "mensaje": mensaje,
        "data": data,
        "errores": None,
    }, status=status)


def validation_error_response(errores, mensaje="Hay errores en el formulario", status=422):
    return JsonResponse({
        "ok": False,
        "mensaje": mensaje,
        "data": None,
        "errores": errores,
    }, status=status)


def error_response(mensaje, errores=None, status=400):
    return JsonResponse({
        "ok": False,
        "mensaje": mensaje,
        "data": None,
        "errores": errores,
    }, status=status)
