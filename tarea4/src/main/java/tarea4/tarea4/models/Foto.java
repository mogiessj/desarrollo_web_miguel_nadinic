package tarea4.tarea4.models;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table
public class Foto {
    @Id
    private Integer id;

    @Column(name = "ruta_archivo")
    private String rutaArchivo;
    @Column(name = "nombre_archivo")
    private String nombreArchivo;
    @Column(name = "actividad_id")
    private Integer actividadId;
    @Column(name = "eliminada")
    private Integer eliminada;

    //getters
    public Integer getId() {
        return id;
    }
    public String getRutaArchivo() {
        return rutaArchivo;
    }
    public String getNombreArchivo() {
        return nombreArchivo;
    }
    public Integer getActividadId() {
        return actividadId;
    }
    public Integer getEliminada() {
        return eliminada;
    }
}
