import java.util.*;

public class Day1 {
    public static void main(String[] args) {
        List<String> tecnologias = Arrays.asList("Java", "", "Spring", "MongoDB", null, "Docker");

        // Ejercicio: Filtrar no vacíos, convertir a mayúsculas y unir con "|"
        String resultado = tecnologias.stream()
                .filter(tech -> tech != null && !tech.isEmpty())
                .map(String::toUpperCase)
                .reduce((a, b) -> a + "|" + b)
                .orElse("N/A");

        System.out.println("Resultado: " + resultado);

        // Transformar una lista de números: filtrar pares > 10 y sumar
        List<Integer> numbers = Arrays.asList(11, 12, 13, 14, 15, 16, 17, 18, 19, 20);
        Integer result = numbers.stream()
                .filter(n -> n > 10 && n % 2 == 0)
                .reduce((x, y) -> x + y)
                .orElse(0);

        System.out.println("Resultado: " + result);
    }
}