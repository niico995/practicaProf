const btnBorrar = document.querySelectorAll('.Borrar')

if (btnBorrar) {
    const btnArray = Array.from(btnBorrar);
    btnArray.forEach((btn) => {
        btn.addEventListener('click',(e) => {
            if(!confirm('¿Estas seguro de eliminar este negocio?')) {
                e.preventDefault();
            }
        });
    });
}
