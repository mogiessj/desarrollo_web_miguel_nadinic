
function pedirMotivoEliminacion(idFoto) {
    let motivo = prompt("Ingrese el motivo de eliminación (5-200 caracteres):");
    
    if (motivo === null || motivo.length < 5 || motivo.length > 200) {
        alert("Eliminación cancelada. El motivo debe tener entre 5 y 200 caracteres.");
        return;
    }
    
    enviarFormularioEliminacion(idFoto, motivo);
}

function enviarFormularioEliminacion(idFoto, motivo) {
    let form = document.createElement('form');
    form.method = 'POST';
    form.action = '/t5-admin-fotos/eliminar/' + idFoto;
    
    let motivoInput = document.createElement('input');
    motivoInput.type = 'hidden';
    motivoInput.name = 'motivo';
    motivoInput.value = motivo;
    form.appendChild(motivoInput);

    let csrfToken = document.querySelector('meta[name="_csrf"]').content;
    
    let csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = '_csrf';
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);
    
    document.body.appendChild(form);
    form.submit();
}