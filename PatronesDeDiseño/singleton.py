"""
    Fecha: 08-09-2021
    Tecnologíco Nacional de México
    Instituto Tecnologíco de Colima
    Maestría en Sistemas Computacionales
    Tecnologías de Programación
    Tema I : Programación con patrones de diseño
    Alumno: Ernesto Velasco González (g2046019)
    Profesora: Patricia Elizabeth Figueroa Millan

    Ejemplo del patrón de diseño Singleton
"""

class Singleton:
    _singleton = None
    value_object = 0
    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._singleton

    def show_value(self):
        print(self.value_object)

def main():
    print("Ejemplo del patrón Singleton")
    objeto1 = Singleton()
    objeto2 = Singleton()

    print(objeto1)
    print(objeto2)

if __name__ == "__main__":
    main()