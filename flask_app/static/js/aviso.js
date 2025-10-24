window.addEventListener('DOMContentLoaded', function() {

    const regionSelect = document.getElementById('region-select');
    const comunaSelect = document.getElementById('comuna-select');
    const contactoSelect = document.getElementById("contacto");
    const campoExtra = document.getElementById("campo-extra");
    const contenedorFotos = document.getElementById('contenedorFotos');
    const btnAgregar = document.getElementById('agregarFoto');
    const form = document.getElementById('aviso-form');
    const btnAgregarAviso = document.getElementById('btn-agregar-aviso');
    const inputFecha = document.getElementById('fecha');

    // Llenar regiones
    region_comuna.regiones.forEach(region => {
        const option = document.createElement('option');
        option.value = region.numero;
        option.textContent = region.nombre;
        regionSelect.appendChild(option);
    });

    // Llenar comunas cuando cambia la región
    regionSelect.addEventListener('change', function() {
        comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';
        const selectedRegion = region_comuna.regiones.find(r => r.numero == regionSelect.value);
        if (selectedRegion) {
            selectedRegion.comunas.forEach(comuna => {
                const option = document.createElement('option');
                option.value = comuna.id;
                option.textContent = comuna.nombre;
                comunaSelect.appendChild(option);
            });
        }
    });

    // Mostrar campo extra si selecciona un contacto
    contactoSelect.addEventListener("change", () => {
        campoExtra.innerHTML = "";
        if (contactoSelect.value !== "") {
            campoExtra.innerHTML = `
                <label for="idContacto">Ingrese ID:</label>
                <input type="text" id="idContacto" name="idContacto" minlength="4" maxlength="50">
            `;
        }
    });

    // Fecha inicial
    const ahora = new Date();
    ahora.setHours(ahora.getHours() + 3);
    const yyyy = ahora.getFullYear();
    const mm = String(ahora.getMonth() + 1).padStart(2, '0');
    const dd = String(ahora.getDate()).padStart(2, '0');
    const hh = String(ahora.getHours()).padStart(2, '0');
    const min = String(ahora.getMinutes()).padStart(2, '0');
    inputFecha.value = `${yyyy}-${mm}-${dd}T${hh}:${min}`;

    // Agregar fotos
    btnAgregar.addEventListener('click', () => {
        const inputsActuales = contenedorFotos.querySelectorAll('input[type="file"]');
        if (inputsActuales.length >= 5) {
            alert("No puedes agregar más de 5 fotos.");
            return;
        }
        const nuevoInput = document.createElement('input');
        nuevoInput.type = 'file';
        nuevoInput.name = 'fotos[]';
        nuevoInput.accept = 'image/*';
        nuevoInput.required = true;
        contenedorFotos.insertBefore(document.createElement('br'), btnAgregar);
        contenedorFotos.insertBefore(nuevoInput, btnAgregar);
    });

    // Función de validación
    const validarForm = () => {
        let msg = "";
        let isValid = true;

        const sector = document.getElementById('sector');
        const nombre = document.getElementById('nombre');
        const email = document.getElementById('email');
        const celular = document.getElementById('celular');
        const tipo = document.getElementById('tipo');
        const cantidad = document.getElementById('cantidad');
        const edad = document.getElementById('edad');
        const unidad = document.getElementById('unidad');
        const fecha = document.getElementById('fecha');

        if (regionSelect.value === "") { msg += "Seleccione una región.\n"; isValid = false; }
        if (comunaSelect.value === "") { msg += "Seleccione una comuna.\n"; isValid = false; }
        if (sector.value.length > 100) { msg += "Sector máximo 100 caracteres.\n"; isValid = false; }
        if (!nombre.value || nombre.value.length < 3 || nombre.value.length > 200) { msg += "Nombre inválido.\n"; isValid = false; }
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email.value || !emailPattern.test(email.value) || email.value.length > 100) { msg += "Email inválido.\n"; isValid = false; }
        if (celular.value) {
            const celularPattern = /^\+\d{3}\.\d{8,9}$/;
            if (!celularPattern.test(celular.value)) { msg += "Celular inválido.\n"; isValid = false; }
        }
        if (!tipo.value) { msg += "Seleccione tipo.\n"; isValid = false; }
        if (cantidad.value < 1 || !Number.isInteger(Number(cantidad.value))) { msg += "Cantidad inválida.\n"; isValid = false; }
        if (edad.value < 1 || !Number.isInteger(Number(edad.value))) { msg += "Edad inválida.\n"; isValid = false; }
        if (!unidad.value) { msg += "Seleccione unidad.\n"; isValid = false; }

        const fechaInput = new Date(fecha.value);
        if (fechaInput < new Date()) { msg += "Fecha no puede ser en el pasado.\n"; isValid = false; }

        if (contactoSelect.value !== "") {
            const idContacto = document.getElementById("idContacto");
            if (!idContacto || idContacto.value.length < 4 || idContacto.value.length > 50) { msg += "ID contacto inválido.\n"; isValid = false; }
        }

        if (!isValid) alert(msg);
        return isValid;
    };
/*
    // Botón agregar aviso
    btnAgregarAviso.addEventListener('click', () => {
        if (!validarForm()) return;

        const confirmacion = confirm("¿Está seguro que desea agregar este aviso de adopción?");
        if (confirmacion) {
            form.style.display = 'none';
            const mensajeFinal = document.createElement('div');
            mensajeFinal.innerHTML = `
                <p>Hemos recibido la información de adopción, muchas gracias y suerte!</p>
                <button id="btn-volver-portada">Volver a la portada</button>
            `;
            document.body.appendChild(mensajeFinal);

            document.getElementById('btn-volver-portada').addEventListener('click', () => {
                window.location.href = 'index.html';
            });
        } else {
            form.style.display = 'block';
        }
    });
*/
});
