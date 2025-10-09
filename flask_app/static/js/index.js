document.addEventListener("DOMContentLoaded", () => {
    const avisoBtn = document.getElementById("aviso-adopcion-btn");
    const verListadoBtn = document.getElementById("ver-adopciones-btn");
    const estadisticasBtn = document.getElementById("estadisticas-btn");

    // Las URLs se inyectan desde Flask usando atributos data-
    const urlAviso = avisoBtn.dataset.url;
    const urlListado = verListadoBtn.dataset.url;
    const urlEstadisticas = estadisticasBtn.dataset.url;

    avisoBtn.addEventListener("click", () => {
        window.location.href = urlAviso;
    });

    verListadoBtn.addEventListener("click", () => {
        window.location.href = urlListado;
    });

    estadisticasBtn.addEventListener("click", () => {
        window.location.href = urlEstadisticas;
    });
});
