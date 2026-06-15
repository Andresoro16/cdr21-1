/**
 * Notificaciones globales para el dashboard
 * Archivo: cdr22/static/js/notifications.js
 * 
 * Uso:
 * - Notify.success('Producto guardado correctamente')
 * - Notify.error('Error al guardar el producto')
 * - Notify.warning('Por favor complete todos los campos')
 * - Notify.info('Operación en proceso...')
 */

const Notify = {
    /**
     * Muestra una notificación de éxito
     * @param {string} message - Mensaje a mostrar
     * @param {number} duration - Duración en ms (0 = sin cierre automático)
     */
    success: (message, duration = 3000) => {
        Toastify({
            text: message,
            duration: duration,
            gravity: "top",
            position: "right",
            className: 'toastify-success',
            style: {
                background: "linear-gradient(135deg, #10b981 0%, #059669 100%)",
                borderRadius: "8px",
                boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
                color: "white",
                fontWeight: "500",
            }
        }).showToast();
    },

    /**
     * Muestra una notificación de error
     * @param {string} message - Mensaje a mostrar
     * @param {number} duration - Duración en ms
     */
    error: (message, duration = 4000) => {
        Toastify({
            text: message,
            duration: duration,
            gravity: "top",
            position: "right",
            className: 'toastify-error',
            style: {
                background: "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
                borderRadius: "8px",
                boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
                color: "white",
                fontWeight: "500",
            }
        }).showToast();
    },

    /**
     * Muestra una notificación de advertencia
     * @param {string} message - Mensaje a mostrar
     * @param {number} duration - Duración en ms
     */
    warning: (message, duration = 3500) => {
        Toastify({
            text: message,
            duration: duration,
            gravity: "top",
            position: "right",
            className: 'toastify-warning',
            style: {
                background: "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
                borderRadius: "8px",
                boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
                color: "white",
                fontWeight: "500",
            }
        }).showToast();
    },

    /**
     * Muestra una notificación informativa
     * @param {string} message - Mensaje a mostrar
     * @param {number} duration - Duración en ms
     */
    info: (message, duration = 3000) => {
        Toastify({
            text: message,
            duration: duration,
            gravity: "top",
            position: "right",
            className: 'toastify-info',
            style: {
                background: "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
                borderRadius: "8px",
                boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
                color: "white",
                fontWeight: "500",
            }
        }).showToast();
    },

    /**
     * Muestra un diálogo de confirmación
     * @param {string} message - Mensaje a mostrar
     * @param {function} onConfirm - Callback al confirmar
     * @param {function} onCancel - Callback al cancelar
     */
    confirm: (message, onConfirm, onCancel) => {
        // Usamos el confirm nativo del navegador por compatibilidad
        // Esto se puede mejorar con un modal personalizado en el futuro
        if (confirm(message)) {
            if (onConfirm) onConfirm();
        } else {
            if (onCancel) onCancel();
        }
    },

    /**
     * Muestra una notificación de carga
     * @param {string} message - Mensaje a mostrar
     * @returns {object} Toast object para poder cerrarlo después
     */
    loading: (message = 'Procesando...') => {
        return Toastify({
            text: message,
            duration: 0,
            gravity: "top",
            position: "right",
            className: 'toastify-info',
            style: {
                background: "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
                borderRadius: "8px",
                boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
                color: "white",
                fontWeight: "500",
            }
        }).showToast();
    },

    /**
     * Muestra una notificación con formatos especiales
     * @param {string} type - Tipo: 'success', 'error', 'warning', 'info'
     * @param {string} title - Título
     * @param {string} message - Mensaje adicional
     * @param {number} duration - Duración
     */
    custom: (type = 'info', title = '', message = '', duration = 3000) => {
        const fullMessage = title ? `${title}${message ? '\n' + message : ''}` : message;
        
        const colors = {
            success: {
                bg: "linear-gradient(135deg, #10b981 0%, #059669 100%)",
                className: 'toastify-success'
            },
            error: {
                bg: "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
                className: 'toastify-error'
            },
            warning: {
                bg: "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
                className: 'toastify-warning'
            },
            info: {
                bg: "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
                className: 'toastify-info'
            }
        };

        const config = colors[type] || colors.info;

        Toastify({
            text: fullMessage,
            duration: duration,
            gravity: "top",
            position: "right",
            className: config.className,
            style: {
                background: config.bg,
                borderRadius: "8px",
                boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
                color: "white",
                fontWeight: "500",
                whiteSpace: "pre-wrap",
            }
        }).showToast();
    }
};

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Notify;
}
