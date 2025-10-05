package main.java.Week1;

import java.util.Scanner;

public class Day2 {
    public class Main {
        public static void main(String[] args) {
            // Ejercicio 1: Verificar si un número es par o impar
            int numero = 7;

            if (numero % 2 == 0) {
                System.out.println(numero + " es PAR");
            } else {
                System.out.println(numero + " es IMPAR");
            }

            // Ejercicio 2: Clasificar edades
            int edad = 16;

            if (edad < 13) {
                System.out.println("Niño");
            } else if (edad < 18) {
                System.out.println("Adolescente");
            } else {
                System.out.println("Adulto");
            }

            // Ejercicio 3: Contador del 1 al 10
            for (int i = 1; i <= 10; i++) {
                System.out.println("Número: " + i);
            }

            // Ejercicio 4: Sumar los primeros N números
            int suma = 0;
            int n = 5;

            for (int i = 1; i <= n; i++) {
                suma = suma + i;
                System.out.println("Sumando " + i + ", suma parcial: " + suma);
            }

            System.out.println("Suma total: " + suma);

            // Ejercicio 5: Contador regresivo
            int contador = 5;

            while (contador > 0) {
                System.out.println("Cuenta: " + contador);
                contador--;  // Disminuye contador en 1
            }
            System.out.println("¡Despegue!");

            // Problema: Encuentra todos los números pares entre 1 y 20
            System.out.println("Números pares del 1 al 20:");

            for (int i = 1; i <= 20; i++) {
                if (i % 2 == 0) {
                    System.out.print(i + " ");
                }
            }

            // Problema: Calcula el factorial de un número
            int num = 5;
            int factorial = 1;

            for (int i = 1; i <= num; i++) {
                factorial = factorial * i;
            }

            System.out.println("Factorial de " + num + " es: " + factorial);

            /*
            * Escribe un programa que:
            * Pida un número al usuario (puedes definirlo como variable)
            * Diga si es positivo, negativo o cero
            * Si es positivo, muestre todos los números desde 1 hasta ese número
            * */
            Scanner sc = new Scanner(System.in);
            System.out.println("Ingrese un número: ");
            int numer = sc.nextInt();
            if(numer > 0) {
                for (int i = 1; i <= numer ; i++) {
                    System.out.print(i + " ");
                }
            }
        }
    }
}
