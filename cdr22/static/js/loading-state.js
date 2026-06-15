const LoadingState = {
    setButtonLoading(button, isLoading, options = {}) {
        if (!button) {
            return;
        }

        if (isLoading) {
            if (!button.dataset.originalHtml) {
                button.dataset.originalHtml = button.innerHTML;
            }

            const label = options.label || 'Procesando...';
            button.disabled = true;
            button.setAttribute('aria-busy', 'true');
            button.classList.add('opacity-75', 'cursor-not-allowed');
            button.innerHTML = `
                <span class="inline-flex items-center gap-2">
                    <span class="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></span>
                    <span>${label}</span>
                </span>
            `;
            return;
        }

        button.disabled = false;
        button.removeAttribute('aria-busy');
        button.classList.remove('opacity-75', 'cursor-not-allowed');

        if (button.dataset.originalHtml) {
            button.innerHTML = button.dataset.originalHtml;
            delete button.dataset.originalHtml;
        }
    },

    setDisabled(elements, isDisabled) {
        elements.forEach((element) => {
            if (element) {
                element.disabled = isDisabled;
            }
        });
    },
};
