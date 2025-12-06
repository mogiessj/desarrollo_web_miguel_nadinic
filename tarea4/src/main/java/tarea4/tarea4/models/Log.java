package tarea4.tarea4.models;

import java.time.LocalDateTime;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table
public class Log {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String mensaje;
    private LocalDateTime fechaCreacion;
    
    public Log(String mensaje) {
        this.mensaje = mensaje;
        this.fechaCreacion = LocalDateTime.now();
    }
    
    public Log() {}
    
    //getters
    public Integer getId() { return id; }
    public String getMensaje() { return mensaje; }
    public LocalDateTime getFechaCreacion() { return fechaCreacion; }
    
}
