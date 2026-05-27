import psycopg2
from psycopg2 import Error

def conectar_db():
    try:
        # CConexion a postgresql
        conexion = psycopg2.connect(
            user="postgres",
            password="seli1234",
            host="localhost",
            port="5432",
            database="tarea1"
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def crear_tabla():
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS alumno (
                id SERIAL PRIMARY KEY,
                carnet VARCHAR(15) UNIQUE NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                carrera VARCHAR(150),
                email VARCHAR(150),
                telefono VARCHAR(20),
                fecha_registro DATE DEFAULT CURRENT_DATE
            );
            """
            cursor.execute(query)
            conexion.commit()
            cursor.close()
            conexion.close()
        except Error as e:
            print(f"Error al crear la tabla: {e}")

def agregar_alumno():
    print("\n--- AGREGAR ALUMNO ---")
    carnet = input("Carnet: ")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    carrera = input("Carrera: ")
    email = input("Email: ")
    telefono = input("Teléfono: ")

    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
            INSERT INTO alumno (carnet, nombre, apellido, carrera, email, telefono)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(query, (carnet, nombre, apellido, carrera, email, telefono))
            conexion.commit()
            print("Alumno agregado exitosamente.")
            cursor.close()
            conexion.close()
        except Error as e:
            print(f"Error al agregar alumno: {e}")

def modificar_alumno():
    print("\n--- MODIFICAR ALUMNO ---")
    carnet = input("Ingrese el carnet del alumno a modificar: ")
    
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            # Verificar si existe
            cursor.execute("SELECT * FROM alumno WHERE carnet = %s;", (carnet,))
            if not cursor.fetchone():
                print("No se encontró ningún alumno con ese carnet.")
                return

            print("Ingrese los nuevos datos:")
            nombre = input("Nuevo Nombre: ")
            apellido = input("Nuevo Apellido: ")
            carrera = input("Nueva Carrera: ")
            email = input("Nuevo Email: ")
            telefono = input("Nuevo Teléfono: ")

            query = """
            UPDATE alumno 
            SET nombre = %s, apellido = %s, carrera = %s, email = %s, telefono = %s
            WHERE carnet = %s;
            """
            cursor.execute(query, (nombre, apellido, carrera, email, telefono, carnet))
            conexion.commit()
            print("Datos actualizados correctamente.")
            cursor.close()
            conexion.close()
        except Error as e:
            print(f"Error al modificar: {e}")

def listar_alumnos():
    print("\n--- LISTA DE ALUMNOS ---")
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT carnet, nombre, apellido, carrera, email, telefono, fecha_registro FROM alumno;")
            alumnos = cursor.fetchall()
            
            if not alumnos:
                print("No hay alumnos registrados.")
            else:
                for alu in alumnos:
                    print(f"Carnet: {alu[0]} | {alu[1]} {alu[2]} | Carrera: {alu[3]} | Email: {alu[4]} | Tel: {alu[5]} | Registro: {alu[6]}")
            
            cursor.close()
            conexion.close()
        except Error as e:
            print(f"Error al listar: {e}")

def eliminar_alumno():
    print("\n--- ELIMINAR ALUMNO ---")
    carnet = input("Ingrese el carnet del alumno a eliminar: ")
    
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "DELETE FROM alumno WHERE carnet = %s;"
            cursor.execute(query, (carnet,))
            conexion.commit()
            
            if cursor.rowcount > 0:
                print("Alumno eliminado exitosamente.")
            else:
                print("No se encontró ningún alumno con ese carnet.")
                
            cursor.close()
            conexion.close()
        except Error as e:
            print(f"Error al eliminar: {e}")

def menu():
    crear_tabla()
    while True:
        print("\n=========================")
        print("     MENÚ DE OPCIONES    ")
        print("=========================")
        print("1. Agregar alumno")
        print("2. Modificar alumno")
        print("3. Listar alumnos")
        print("4. Eliminar alumno")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            agregar_alumno()
        elif opcion == "2":
            modificar_alumno()
        elif opcion == "3":
            listar_alumnos()
        elif opcion == "4":
            eliminar_alumno()
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()