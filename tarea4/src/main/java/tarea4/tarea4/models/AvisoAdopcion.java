package tarea4.tarea4.models;

import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Table;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import java.time.LocalDateTime;
import java.util.List;


@Entity
@Table
public class AvisoAdopcion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private LocalDateTime fechaIngreso;

    private String sector;

    private String nombre;
    private String email;
    private String celular;

    private String tipo; 

    private Integer cantidad;
    private Integer edad;

    private String unidadMedida;

    private LocalDateTime fechaEntrega;

    private String descripcion;

    // getters
    public Integer getId() {
        return id;
    }
    public String getNombre() {
        return nombre;
    }
    public LocalDateTime getFechaIngreso() {
        return fechaIngreso;
    }
    public String getSector() {
        return sector;
    }
    public String getEmail() {
        return email;
    }
    public String getCelular() {
        return celular;
    }
    public String getTipo() {
        return tipo;
    }
    public Integer getCantidad() {
        return cantidad;
    }
    public Integer getEdad() {
        return edad;
    }
    public String getUnidadMedida() {
        return unidadMedida;
    }
    public LocalDateTime getFechaEntrega() {
        return fechaEntrega;
    }
    public String getDescripcion() {
        return descripcion;
    }

    //relations
    @OneToMany(mappedBy = "aviso", fetch = FetchType.LAZY)
    private List<Nota> notas;

    @ManyToOne
    @JoinColumn(name = "comuna_id")
    private Comuna comuna;

    public Comuna getComuna() {
        return comuna;
    }


}
