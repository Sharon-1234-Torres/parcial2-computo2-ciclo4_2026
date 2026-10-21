document.addEventListener("DOMContentLoaded", () => {
    mnxSistema.addEventListener('click', e => {
        e.preventDefault();
        let form = e.target.dataset.form;
        if (form) cargarForm(form);
    });
    fetch('/sesion').then(r => r.json()).then(u => lblSesion.textContent = `Usuario: ${u.nombre}`);
    btnLogout.addEventListener('click', async e => {
        e.preventDefault();
        await fetch('/logout', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({modulo: 'logout'})
        });
        location.href = '/';
    });
});
function cargarForm(form, callback) {
    if ($(`#${form} > form`).length <= 0) {
        fetch(`/vistas?form=${form}`)
            .then(response => response.text())
            .then(ventana => {
                $(`#${form}`).html(ventana).draggable();
                cerrarVentana();
                if (callback) callback();
            })
            .catch(error => console.error('Error al cargar el formulario:', error));
    } else {
        $(`#${form}`).show();
        if (callback) callback();
    }
}
function cerrarVentana() {
    $('.btn-close').off('click').on('click', e => {
        e.preventDefault();
        $(`#${e.target.dataset.form}`).hide();
    });
}
function escapar(t) {
    return String(t).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
}
