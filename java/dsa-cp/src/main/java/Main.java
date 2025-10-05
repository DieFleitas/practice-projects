public class Main {
    public static void main(String[] args) {
        System.out.println("¡Hola Mundo! Estoy aprendiendo algoritmos con Java");

        int numero1 = 15;
        int numero2 = 7;
        int suma = numero1 + numero2;

        System.out.println(numero1 + " + " + numero2 + " = " + suma);
        /*
        Problema: Calcula el área de un rectángulo
        Fórmula: área = base * altura
         */
        double base = 8.5;
        double altura = 4.2;

        double area = base * altura;
        double perimetro = 2 * (base + altura);

        System.out.println("Área del rectangulo: " + area);
        System.out.println("Perimetro del rectangulo: " + perimetro);

    }
}