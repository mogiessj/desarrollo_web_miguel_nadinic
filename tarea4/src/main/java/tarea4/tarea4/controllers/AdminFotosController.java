package tarea4.tarea4.controllers;

import tarea4.tarea4.models.AdminFotosDTO;
import tarea4.tarea4.services.FotoService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.List;

@Controller
public class AdminFotosController {

    private final FotoService fotoService;

    public AdminFotosController(FotoService fotoService) {
        this.fotoService = fotoService;
    }

    //ruta de la galería (necesitará autenticación)
    @GetMapping("/t5-admin-fotos")
    public String mostrarGaleria(Model model) {
        List<AdminFotosDTO> fotos = fotoService.obtenerFotosParaAdmin();
        model.addAttribute("fotos", fotos);
        return "t5-admin-fotos";
    }

    @PostMapping("/t5-admin-fotos/eliminar/{idFoto}")
    public String eliminarFoto(
            @PathVariable Integer idFoto,
            @RequestParam String motivo,
            RedirectAttributes redirectAttributes) {
        
        //validación del Motivo
        if (motivo == null || motivo.trim().length() < 5 || motivo.trim().length() > 200) {
            redirectAttributes.addFlashAttribute("error", "Error: El motivo de eliminación debe tener entre 5 y 200 caracteres.");
            return "redirect:/t5-admin-fotos";
        }
        
        try {
            fotoService.marcarFotoComoEliminada(idFoto, motivo);
            redirectAttributes.addFlashAttribute("success", "Foto ID " + idFoto + " marcada como eliminada.");
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("error", "Error al eliminar la foto. " + e.getMessage());
        }
        
        return "redirect:/t5-admin-fotos";
    }
}