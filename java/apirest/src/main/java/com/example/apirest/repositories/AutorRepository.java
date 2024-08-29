package com.example.apirest.repositories;

import com.example.apirest.entities.Autor;
import org.springframework.stereotype.Repository;

@Repository
public interface AutorRepository extends BaseRepository<Autor, Long> {
}
