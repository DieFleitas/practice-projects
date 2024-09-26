package com.practice.cursos_api.repository;

import com.practice.cursos_api.model.Auto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AutoRepository extends JpaRepository<Auto, Long> {
    public List<Auto> findByMarca(String marca);
    public List<Auto> findByColor(String color);
    public List<Auto> findByModelo(String modelo);
    public List<Auto> findByAnio(Long anio);

}
