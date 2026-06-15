from cdr22.services.configuracion import get_configuracion_sistema


def configuracion_sistema(request):
    return {
        'configuracion_sistema': get_configuracion_sistema()
    }
