document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("modalEvaluar");
    const form = document.getElementById("formEvaluar");

    modal.addEventListener("show.bs.modal", function (event) {
        let button = event.relatedTarget;        // el botón que abrió el modal
        let avisoId = button.getAttribute("data-id");

        // configurar el action dinámicamente
        form.action = "/evaluar/" + avisoId;
    });
});