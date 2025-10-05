package main.java.Week1;

public class Day3 {

    public static void main(String[] args) {
        // Ejercicio: Encontrar el número mayor en un array
        int[] numeros = {45, 12, 89, 34, 67, 23};
        int mayor = numeros[0];  // Empezamos con el primer elemento

        for (int i = 1; i < numeros.length; i++) {
            if (numeros[i] > mayor) {
                mayor = numeros[i];
            }
        }

        System.out.println("El número mayor es: " + mayor);
    }

    // Ejercicio: Función para verificar si un número es primo
    public static boolean esPrimo(int numero) {
        if (numero <= 1) return false;

        for (int i = 2; i <= numero / 2; i++) {
            if (numero % i == 0) {
                return false;  // Encontró un divisor, no es primo
            }
        }
        return true;  // No encontró divisores, es primo
    }

    // Problema: Sistema de gestión de notas de estudiantes
    // Función para calcular la nota más alta
    public static int notaMaxima(int[] notas) {
        int maxima = notas[0];
        for (int nota : notas) {
            if (nota > maxima) maxima = nota;
        }
        return maxima;
    }

    // Función para contar estudiantes aprobados (nota >= 70)
    public static int contarAprobados(int[] notas) {
        int count = 0;
        for (int nota : notas) {
            if (nota >= 70) count++;
        }
        return count;
    }

    // Función para mostrar todas las notas
    public static void mostrarNotas(int[] notas) {
        System.out.println("Lista de notas:");
        for (int i = 0; i < notas.length; i++) {
            System.out.println("Estudiante " + (i+1) + ": " + notas[i]);
        }
    }

    /*Crea un programa que:
    Tenga un array con 10 números
    Use funciones para:
    Encontrar el número menor
    Calcular la suma de todos los elementos
    Contar números pares e impares
    * */
    public int buscarMenor(int[] num) {
        int menor = num[0];
        for (int i = 0; i < num.length; i++) {
            if (num[i] < menor) {
                menor = num[i];
            }
        }
        return menor;
    }

    public int sumaElem(int[] num) {
        int suma = 0;
        for (int i = 0; i < num.length; i++) {
            suma += num[i];
        }
        return suma;
    }

    public int[] contarParesImpares(int[] num) {
        int pares = 0;
        int impares = 0;
        int[] res = new int[2];

        for (int i = 0; i < num.length; i++) {
            if (num[i] % 2 == 0 ) {
                pares += 1;
            } else {
                impares += 1;
            }
        }
        res[0] = pares;
        res[1] = impares;
        return res;
    }
}
