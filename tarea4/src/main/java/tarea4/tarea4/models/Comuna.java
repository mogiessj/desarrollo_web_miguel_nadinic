package tarea4.tarea4.models;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table
public class Comuna {
    @Id
    private Integer id;

    private String nombre;

    private Integer regionId;

    // getters
    public Integer getId() {
        return id;
    }
    public String getNombre() {
        return nombre;
    }
    public Integer getRegion_id() {
        return regionId;
    }
}
