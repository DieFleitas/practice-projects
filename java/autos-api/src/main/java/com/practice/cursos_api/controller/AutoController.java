package com.practice.cursos_api.controller;

import com.practice.cursos_api.model.Auto;
import com.practice.cursos_api.service.AutoService;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/autos/")
public class AutoController {

    private final AutoService autoService;

    public AutoController(AutoService autoService) {
        this.autoService = autoService;
    }

    @PostMapping(value = "crear", headers = "Accept=application/json")
    public void crearAuto(@RequestBody Auto auto) {
        autoService.crearAuto(auto);
    }

    @GetMapping(value = "listar", headers = "Accept=application/json")
    public List<Auto> listarAuto() {
        return autoService.listarAuto();
    }

    @GetMapping(value = "listarPorId/{id}", headers = "Accept=application/json")
    public Optional<Auto> buscarPorId(@PathVariable Long id) {
        return autoService.buscarPorId(id);
    }

    @PutMapping(value = "actualizar", headers = "Accept=application/json")
    public void actualizarAuto(@RequestBody Auto auto) {
        autoService.actualizarAuto(auto);
    }

    @DeleteMapping(value = "eliminar/{id}", headers = "Accept=application/json")
    public void eliminarAuto(@PathVariable Long id) {
        autoService.eliminarAuto(id);
    }

    @GetMapping(value = "listarPorId/{marca}", headers = "Accept=application/json")
    public List<Auto> buscarPorMarca(@PathVariable String marca) {
        return autoService.buscarPorMarca(marca);
    }

    @GetMapping(value = "listarPorId/{modelo}", headers = "Accept=application/json")
    public List<Auto> buscarPorModelo(@PathVariable String id) {
        return autoService.buscarPorModelo(id);
    }

    @GetMapping(value = "listarPorId/{color}", headers = "Accept=application/json")
    public List<Auto> buscarPorColor(@PathVariable String id) {
        return autoService.buscarPorColor(id);
    }

    @GetMapping(value = "listarPorId/{anio}", headers = "Accept=application/json")
    public List<Auto> buscarPorAnio(@PathVariable Long anio) {
        return autoService.buscarPorAnio(anio);
    }
}
