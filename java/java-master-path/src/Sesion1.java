import java.util.*;
import java.util.function.*;
import java.util.stream.*;

public class Sesion1 {

    public static void main(String[] args) {
        List<Empleado> empleados = Arrays.asList(
                new Empleado("Ana", "IT", 28, 4500),
                new Empleado("Luis", "Ventas", 35, 3000),
                new Empleado("Marta", "IT", 40, 5000),
                new Empleado("Pedro", null, 25, 3200)
        );

        // 1. Filtrar empleados de IT con salario > 4000
        List<Empleado> itSalarioAlto = empleados.stream()
                .filter(e -> "IT".equals(e.departamento()))
                .filter(e -> e.salario() > 4000)
                .toList();

        // 2. Calcular promedio de edad por departamento
        Map<String, Double> avgEdadPorDepto = empleados.stream()
                .filter(e -> e.departamento() != null)
                .collect(Collectors.groupingBy(
                        Empleado::departamento,
                        Collectors.averagingInt(Empleado::edad)
                ));

        // 3. Encontrar el salario máximo usando Optional
        OptionalInt maxSalario = empleados.stream()
                .mapToInt(Empleado::salario)
                .max();


        List<Integer> numeros = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12);

        // Instrucciones:
        // 1. Filtrar números pares mayores a 5
        // 2. Elevar al cuadrado
        // 3. Calcular el promedio
        OptionalDouble resultado = numeros.stream()
                .filter(n -> n % 2 == 0)
                .filter(n -> n > 5)
                .mapToDouble(n -> Math.pow(n, 2))
                .average();
    }
}

record Empleado(String nombre, String departamento, int edad, int salario) {
}