package tarea4.tarea4.models;


import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;


public interface FotoRepository extends JpaRepository<Foto, Integer> {

    @Query("SELECT new tarea4.tarea4.models.AdminFotosDTO(" +
           " f.id, f.rutaArchivo, a.fechaIngreso, c.nombre, a.email) " + 
           " FROM Foto f " +
           " LEFT JOIN AvisoAdopcion a ON f.actividadId = a.id " 
           + " LEFT JOIN a.comuna c " 
           + " WHERE f.eliminada = 0 " + 
           " ORDER BY a.fechaIngreso DESC")
    List<AdminFotosDTO> findAllFotosParaAdmin();

    @Modifying
    @Query("UPDATE Foto f SET f.eliminada = :estado WHERE f.id = :idFoto")
    void updateEliminadaById(@Param("idFoto") Integer idFoto, @Param("estado") Integer estado);
}