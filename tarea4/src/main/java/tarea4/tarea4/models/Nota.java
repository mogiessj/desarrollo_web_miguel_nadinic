package tarea4.tarea4.models;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;

@Entity
@Table
public class Nota {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private Integer nota;

    @ManyToOne
    @JoinColumn(name = "aviso_id")
    private AvisoAdopcion aviso;

    //getters
    public Integer getId() {
        return id;
    }
    public Integer getNota() {
        return nota;
    }
    public AvisoAdopcion getAviso() {
        return aviso;
    }

    //setters
    public void setNota(Integer nota) {
        this.nota = nota;
    }
    public void setAviso(AvisoAdopcion aviso) {
        this.aviso = aviso;
    }
}
