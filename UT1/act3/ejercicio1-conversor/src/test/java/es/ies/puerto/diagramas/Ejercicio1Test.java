
package es.ies.puerto.diagramas;

import static org.junit.jupiter.api.Assertions.*;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.nio.charset.StandardCharsets;

import org.junit.jupiter.api.Test;

class Ejercicio1Test {

    private String ejecutar(String entrada) {
        var inOriginal = System.in;
        var outOriginal = System.out;

        try {
            System.setIn(new ByteArrayInputStream(entrada.getBytes(StandardCharsets.UTF_8)));
            ByteArrayOutputStream salida = new ByteArrayOutputStream();
            System.setOut(new PrintStream(salida, true, StandardCharsets.UTF_8));
            Ejercicio1.main(new String[0]);
            return salida.toString(StandardCharsets.UTF_8);
        } finally {
            System.setIn(inOriginal);
            System.setOut(outOriginal);
        }
    }

    @Test
    void kmAMetrosCorrecto() {
        assertEquals(4500.0, Ejercicio1.kmAMetros(4.5), 0.0001);
    }

    @Test
    void metrosACentimetrosCorrecto() {
        assertEquals(325.0, Ejercicio1.metrosACentimetros(3.25), 0.0001);
    }

    @Test
    void horasAMinutosCorrecto() {
        assertEquals(90.0, Ejercicio1.horasAMinutos(1.5), 0.0001);
    }

    @Test
    void celsiusAFahrenheitCorrecto() {
        assertEquals(68.0, Ejercicio1.celsiusAFahrenheit(20), 0.0001);
    }

    @Test
    void consolaOpcion1() {
        assertTrue(ejecutar("1\n4.5\n").contains("4500"));
    }

    @Test
    void consolaOpcion2() {
        assertTrue(ejecutar("2\n3.25\n").contains("325"));
    }

    @Test
    void consolaOpcion3() {
        assertTrue(ejecutar("3\n1.5\n").contains("90"));
    }

    @Test
    void consolaOpcion4() {
        assertTrue(ejecutar("4\n20\n").contains("68"));
    }

    @Test
    void opcionInvalida() {
        String salida = ejecutar("9\n1\n").toLowerCase();
        assertTrue(salida.contains("no válida") || salida.contains("no valida"));
    }

    @Test
    void funcionesSonEstaticas() throws Exception {
        String[] nombres = {
            "kmAMetros",
            "metrosACentimetros",
            "horasAMinutos",
            "celsiusAFahrenheit"
        };

        for (String nombre : nombres) {
            Method metodo = Ejercicio1.class.getDeclaredMethod(nombre, double.class);
            assertTrue(Modifier.isStatic(metodo.getModifiers()),
                    "La función " + nombre + " debe ser static");
        }
    }
}
