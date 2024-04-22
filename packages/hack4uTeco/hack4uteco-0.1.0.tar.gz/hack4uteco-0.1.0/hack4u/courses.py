#!/usr/bin/env python3

class Course:
    def __init__ (self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link

    # Sirve para que transforme los objetos en cadena de texto y el for los pueda mostrar
    def __repr__ (self):
        return f"{self.name}, {self.duration}, {self.link}"

# Creamos 3 instancias temporales que no se guardan en variables
courses = [
    Course("introduccion a linux", 15, "www.hola.com"),
    Course("personalizacion de linux", 3, "www.hola.com"),
    Course("introduccion al hacking", 53, "www.hola.com")
]

# Funcion que itera por cada objeto y junto a str muestra cada curso
def list_courses():
    for course in courses:
        print(course)

def search_course_by_name(name):
    for course in courses:
        if course.name == name:
            return course
    return None