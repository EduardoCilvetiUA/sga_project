function delete_pop_up(buttonSelector, confirmText) {
    const delete_buttons = document.querySelectorAll(buttonSelector);

    delete_buttons.forEach((boton) => {
        boton.addEventListener("click", function () {
            const form = this.closest("form");

            Swal.fire({
                title: '¿Estás seguro?',
                text: confirmText,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Sí, eliminar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    form.submit();
                }
            });
        });
    });
}
