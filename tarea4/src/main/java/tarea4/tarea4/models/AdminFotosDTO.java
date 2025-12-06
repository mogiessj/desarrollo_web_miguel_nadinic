package tarea4.tarea4.models;

import java.time.LocalDateTime;

public class AdminFotosDTO {
    
    private Integer idFoto;
    private String rutaArchivo;
    private LocalDateTime fechaIngresoAviso;
    private String nombreComuna;
    private String emailContacto;

    public AdminFotosDTO(Integer idFoto, String rutaArchivo, LocalDateTime fechaIngresoAviso, String nombreComuna, String emailContacto) {
        this.idFoto = idFoto;
        this.rutaArchivo = rutaArchivo;
        this.fechaIngresoAviso = fechaIngresoAviso;
        this.nombreComuna = nombreComuna;
        this.emailContacto = emailContacto;
    }
    
    //getters
    public Integer getIdFoto() { return idFoto; }
    public String getRutaArchivo() { return rutaArchivo; }
    public LocalDateTime getFechaIngresoAviso() { return fechaIngresoAviso; }
    public String getNombreComuna() { return nombreComuna; }
    public String getEmailContacto() { return emailContacto; }
}