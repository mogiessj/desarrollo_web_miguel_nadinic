let avisoBtn = document.getElementById("aviso-adopcion-btn");
let verListadoBtn = document.getElementById("ver-adopciones-btn"); 
let estadisticasBtn = document.getElementById("estadisticas-btn");

const aviso = () => {
    window.location.href = 'aviso.html';
};

const listado = () => {
    window.location.href = 'listado.html';
};

const estadisticas = () => {
    window.location.href = 'estadisticas.html';
};

avisoBtn.addEventListener("click", aviso);
verListadoBtn.addEventListener("click", listado);
estadisticasBtn.addEventListener("click", estadisticas);