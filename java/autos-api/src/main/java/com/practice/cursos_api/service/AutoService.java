package com.practice.cursos_api.service;

import com.practice.cursos_api.model.Auto;
import com.practice.cursos_api.repository.AutoRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class AutoService {

    private final AutoRepository autoRepository;

    public AutoService(AutoRepository autoRepository) {
        this.autoRepository = autoRepository;
    }

    public void crearAuto(Auto auto) {
        autoRepository.save(auto);
    }

    public List<Auto> listarAuto() {
        return autoRepository.findAll();
    }

    public Optional<Auto> buscarPorId(Long id) {
        return autoRepository.findById(id);
    }

    public void actualizarAuto(Auto auto) {
        autoRepository.save(auto);
    }

    public void eliminarAuto(Long id) {
        autoRepository.deleteById(id);
    }

    public List<Auto> buscarPorMarca(String marca) {
        return autoRepository.findByMarca(marca);
    }

    public List<Auto> buscarPorModelo(String modelo) {
        return autoRepository.findByModelo(modelo);
    }

    public List<Auto> buscarPorColor(String color) {
        return autoRepository.findByColor(color);
    }

    public List<Auto> buscarPorAnio(Long anio) {
        return autoRepository.findByAnio(anio);
    }
}
