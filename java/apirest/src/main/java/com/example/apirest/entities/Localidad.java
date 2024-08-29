package com.example.apirest.entities;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;


@Entity
@Table(name="localidad")
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class Localidad extends Base{

    @Column(name="denominaciob")
    private String denominacion;

}
