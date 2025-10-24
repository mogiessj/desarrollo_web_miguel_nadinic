document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("volver-inicio-btn");

    // Las URLs se inyectan desde Flask usando atributos data-
    const urlInicio = btn.dataset.url;

    btn.addEventListener("click", () => {
        window.location.href = urlInicio;
    });
});

document.addEventListener("DOMContentLoaded", function() {
    fetch('/avisos_por_dia')
        .then(response => response.json())
        .then(data => {
            if(data.error) {
                console.error("Error al obtener datos:", data.error);
                return;
            }

            //datos para highcharts
            const dias = data.map(item => item.dia);
            const cantidades = data.map(item => item.cantidad);

            Highcharts.chart('grafico1', {
                chart: {
                    type: 'line'
                },
                title: {
                    text: 'Avisos de adopción por día'
                },
                xAxis: {
                    categories: dias,
                    title: { text: 'Día' }
                },
                yAxis: {
                    title: { text: 'Cantidad de avisos' },
                    allowDecimals: false
                },
                series: [{
                    name: 'Avisos',
                    data: cantidades
                }],
                tooltip: {
                    shared: true,
                    valueSuffix: ' avisos'
                }
            });
        })
        .catch(error => console.error('Error fetching API:', error));
});

document.addEventListener("DOMContentLoaded", function() {
    fetch('/avisos_por_tipo')
        .then(response => response.json())
        .then(data => {
            console.log("Datos por tipo:", data); // depuración

            //datos para highcharts
            const seriesData = data.map(item => ({
                name: item.tipo,
                y: item.cantidad
            }));

            Highcharts.chart('grafico2', {
                chart: {
                    type: 'pie'
                },
                title: {
                    text: 'Avisos de adopción por tipo de mascota'
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.y}</b>'
                },
                accessibility: {
                    point: {
                        valueSuffix: ''
                    }
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>: {point.y}'
                        }
                    }
                },
                series: [{
                    name: 'Cantidad',
                    colorByPoint: true,
                    data: seriesData
                }]
            });
        })
        .catch(err => console.error("Error al cargar datos:", err));
});

document.addEventListener("DOMContentLoaded", function() {
    fetch('/avisos_tipo_mes')
        .then(resp => resp.json())
        .then(data => {
            if (data.error) {
                console.error("Error en API:", data.error);
                return;
            }

            //highcharts
            Highcharts.chart('grafico3', {
                chart: { type: 'column' },
                title: { text: 'Avisos de adopción por mes y tipo de mascota' },
                xAxis: { categories: data.categorias, crosshair: true },
                yAxis: {
                    min: 0,
                    title: { text: 'Cantidad de avisos' }
                },
                tooltip: { shared: true, valueSuffix: ' avisos' },
                plotOptions: {
                    column: { pointPadding: 0.2, borderWidth: 0 }
                },
                series: data.series
            });
        })
        .catch(err => console.error("Error al cargar datos:", err));
});
