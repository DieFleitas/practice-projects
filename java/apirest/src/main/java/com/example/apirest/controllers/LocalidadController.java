package com.example.apirest.controllers;

import com.example.apirest.entities.Localidad;
import com.example.apirest.services.LocalidadServiceImpl;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@CrossOrigin(origins = "*")
@RequestMapping(path = "api/v1/localidad")
public class LocalidadController extends BaseControllerImpl<Localidad, LocalidadServiceImpl>{
}
