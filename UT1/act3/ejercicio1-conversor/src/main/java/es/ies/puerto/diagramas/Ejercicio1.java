package es.ies.puerto.diagramas;

import java.util.Scanner;

/**
 * Actividad: Conversor de unidades.
 *
 * Completa esta clase siguiendo el enunciado del README.
 */
public class Ejercicio1 {

    /**
     * Funcion que convierte de kilometros a metros
     * @param valor numero de kilometros a convertir
     * @return numero de metros
     */
    public static double kmAMetros(double valor) {
        double resultadoValor = valor * 1000;
        return resultadoValor;
    }

    /**
     * Funcion que convierte de metros a centimetros
     * @param valor numero de metros a convertir
     * @return numero de centimetros
     */
    public static double metrosACentimetros(double valor) {
        double resultadoValor = valor * 100;
        return resultadoValor;
    }

    /**
     * Funcion que convierte de horas a minutos
     * @param valor numero de horas a convertir
     * @return numero de minutos
     */
    public static double horasAMinutos(double valor) {
        double resultadoValor = valor * 60;
        return resultadoValor;
    }

    /**
     * Funcion que convierte de celsius a fahrenheit
     * @param valor numero de celsius a convertir
     * @return numero de fahrenheit
     */
    public static double celsiusAFahrenheit(double valor) {
        double resultadoValor = ((valor * 9/5) +32);
        return resultadoValor;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int opcion = 0;
        double resultado = 0;
        while (opcion < 6) {
            System.out.println("=== MENU ===");
            System.out.println("1. Km ---> Metros");
            System.out.println("2. Metros ---> Centimetros");
            System.out.println("3. Horas ---> Minutos");
            System.out.println("4. Fahrenheit ---> Celcius");
            System.out.println("5. Finalizar");
            System.out.println("ELija una opcion");
            opcion = scanner.nextInt();

            if (opcion < 0 || opcion > 5) {
                System.out.println("Opción no valida");
            }

            if (opcion == 1) {
                System.out.println("Km ---> metros: ");
                double valor = scanner.nextDouble();

                resultado = kmAMetros(valor);
                System.out.println(+resultado+" metros");
                
            }

            if (opcion == 2) {
                System.out.println("metros ---> centimetros: ");
                double valor = scanner.nextDouble();

                resultado = metrosACentimetros(valor);
                System.out.println(+resultado+" centimetros");
            }
            if (opcion == 3) {
                System.out.println("horas ---> minutos: ");
                double valor = scanner.nextDouble();

                resultado = horasAMinutos(valor);
                System.out.println(+resultado+" minutos");
            }
            if (opcion == 4) {
                System.out.println("Celsius ---> fahrenheit: ");
                double valor = scanner.nextDouble();

                resultado = celsiusAFahrenheit(valor);
                System.out.println(+resultado+" fahrenheit");
            }
            if (opcion == 5) {
                return;
            }
            return ;

        }




    }
}
