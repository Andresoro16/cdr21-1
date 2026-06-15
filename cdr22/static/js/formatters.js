const Formatters = {
    money: (value, options = {}) => {
        const amount = Number(value || 0);
        const locale = options.locale || 'es-CO';
        const currency = options.currency || window.AppConfig?.currency || 'COP';

        return new Intl.NumberFormat(locale, {
            style: 'currency',
            currency,
            minimumFractionDigits: options.minimumFractionDigits ?? 2,
            maximumFractionDigits: options.maximumFractionDigits ?? 2,
        }).format(amount);
    },
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = Formatters;
}
