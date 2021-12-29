/* 
    Fecha: 08-09-2021
    Tecnologíco Nacional de México
    Instituto Tecnologíco de Colima
    Maestría en Sistemas Computacionales
    Tecnologías de Programación
    Tema I : Programación con patrones de diseño
    Alumno: Ernesto Velasco González (g2046019)
    Profesora: Patricia Elizabeth Figueroa Millan

    Ejemplo del patrón de diseño Singleton en Java
*/

public class Singleton {
    private static Singleton instance;
    public Integer value;

    // Establecer el constructor como privado
    private Singleton(Integer value) {
        this.value = value;
    }

    // Establecer un método de cracion estatico
    public static Singleton getInstance(Integer value) {
        // Crear una instancia nueva solo si no existe ya
        if (instance == null) instance = new Singleton(value);
        return instance;
    }

    public static void main(String[] args) {
        // Instanciar la clase Singleton en dos objetos
        Singleton objeto1 = Singleton.getInstance(0);
        Singleton objeto2 = Singleton.getInstance(1);
        
        // Imprimir las innstancias en el formato class@HEX(hashcode) value
        System.out.println("Ejemplo del patrón Singleton");
        System.out.println(String.valueOf(objeto1) + "\t" + objeto1.value);
        System.out.println(String.valueOf(objeto2) + "\t" + objeto2.value);
    }
}