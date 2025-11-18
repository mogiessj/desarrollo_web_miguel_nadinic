package tarea4.tarea4.controllers;

import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import tarea4.tarea4.models.AvisoAdopcion;
import tarea4.tarea4.services.AppService;

@Controller
public class AppController {
    
    @Autowired
    private AppService appService;

    @GetMapping("/avisos")
    public String verAvisos(Model model) {
        Map<AvisoAdopcion, Double> avisos = appService.obtenerAvisosConPromedio();
        model.addAttribute("avisos", avisos);
        return "avisos";
    }

    @PostMapping("/evaluar/{id}")
    public String evaluarAviso(@PathVariable Integer id, @RequestParam Integer nota) {

        appService.agregarNota(id, nota);

        return "redirect:/avisos";
}

}
