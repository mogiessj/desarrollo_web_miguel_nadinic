package tarea4.tarea4.services;

import tarea4.tarea4.models.FotoRepository;
import tarea4.tarea4.models.AdminFotosDTO;
import org.springframework.stereotype.Service;
import tarea4.tarea4.models.Log;
import tarea4.tarea4.models.LogRepository;

import jakarta.transaction.Transactional;

import java.util.List;

@Service
public class FotoService {

    private final FotoRepository fotoRepository;
    private final LogRepository logRepository;

    public FotoService(FotoRepository fotoRepository, LogRepository logRepository) {
        this.fotoRepository = fotoRepository;
        this.logRepository = logRepository;
    }

    public List<AdminFotosDTO> obtenerFotosParaAdmin() {
        return fotoRepository.findAllFotosParaAdmin(); 
    }

    @Transactional // Asegura que ambas operaciones
    public void marcarFotoComoEliminada(Integer idFoto, String motivo) {
        
        fotoRepository.updateEliminadaById(idFoto, 1); 

        String mensajeLog = String.format("eliminado foto %d por usuario cc5002, motivo: %s", idFoto, motivo);
        
        Log log = new Log(mensajeLog);
        logRepository.save(log);
    }
}