package tarea4.tarea4.services;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import tarea4.tarea4.models.AvisoAdopcion;
import tarea4.tarea4.models.AvisoAdopcionRepository;
import tarea4.tarea4.models.Nota;
import tarea4.tarea4.models.NotaRepository;

@Service
public class AppService {
    @Autowired
    private AvisoAdopcionRepository avisoRepo;

    @Autowired
    private NotaRepository notaRepo;

    public Map<AvisoAdopcion, Double> obtenerAvisosConPromedio() {
        List<AvisoAdopcion> avisos = avisoRepo.findAll();
        Map<AvisoAdopcion, Double> resultado = new LinkedHashMap<>();

        for (AvisoAdopcion aviso : avisos) {
            Double promedio = notaRepo.promedioPorAviso(aviso.getId());
            resultado.put(aviso, promedio);
        }

        return resultado;
    }

    public void agregarNota(Integer avisoId, Integer notaValor) {

    if (notaValor < 1 || notaValor > 7) {
        throw new IllegalArgumentException("La nota debe ser entre 1 y 7");
    }

    AvisoAdopcion aviso = avisoRepo.findById(avisoId)
        .orElseThrow(() -> new RuntimeException("Aviso no encontrado"));

    Nota nota = new Nota();
    nota.setNota(notaValor);
    nota.setAviso(aviso);

    notaRepo.save(nota);
}

}
