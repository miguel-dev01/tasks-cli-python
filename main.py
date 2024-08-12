#!/usr/bin/env python

import argparse
import datetime
import json
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(prog='Task Tracker',
                                     description='Aplicación para realizar un seguimiento de sus tareas y administrar '
                                                 'su lista de tareas pendientes. ',
                                     epilog='¡Gracias por usar Task Tracker!')

    # Crear subcomandos usando subparsers
    subparsers = parser.add_subparsers(dest='command')
    # Subcomando para agregar una nueva tarea
    add_parser = subparsers.add_parser('add', help='Add a new task')
    # Subcomando para actualizar una tarea existente
    update_parser = subparsers.add_parser('update', help='Update an existing task')
    update_parser.add_argument('task_to_upgrade', type=int, help='The id of the task to update')

    # TODO
    # Argumentos de las tareas, se deberia refactorizar
    add_parser.add_argument('task', type=str, help='The info of task to add, update and delete')
    update_parser.add_argument('task', type=str, help='The info of task to add, update and delete')

    # Parsear los argumentos de la línea de comandos
    args = parser.parse_args()

    # Llamamos a la funcion correspondiente
    if args.command == 'add':
        add_task(args.task)
    elif args.command == 'update':
        update_task(args.task_to_upgrade, args.task)
    else:
        print("Comando no reconocido")


def add_task(task):
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    to_save = {
        "id": 0,
        "description": task,
        "status": "todo",
        "createdAt": now,
        "updatedAt": ""
    }

    try:
        # TODO Debuguear el siguiente try-catch
        try:
            with open("db.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("Archivo JSON no encontrado")
            data = []
        except json.decoder.JSONDecodeError:
            print("Error al leer el fichero JSON")
            data = []

        if data:
            last_id = max(item["id"] for item in data)
            to_save["id"] = last_id + 1
        else:
            to_save["id"] = 1

        data.append(to_save)

        with open("db.json", "w") as file:
            json.dump(data, file, indent=4)

        print(f"Tarea '{task}' guardada correctamente")
    except Exception as e:
        print("Error al guardar la tarea", str(e))


def update_task(task_id, task_to_upgrade):
    # TODO Contemplar try-catch
    with open("db.json", "r") as file:
        tasks = json.load(file)

    if not tasks:
        print("No hay tareas disponibles para actualizar")
        return

    for task in tasks:
        if task["id"] == task_id:
            task["description"] = task_to_upgrade
            break
        else:
            print("No se ha encontrado la tarea indicada para actualizarla")

    with open("db.json", "w") as file:
        json.dump(tasks, file, indent=4)
    print("Tarea actualizada correctamente")


def get_data():
    # Cargar el archivo JSON
    with open("db.json", "r") as file:
        data = json.load(file)

    # Recorrer la lista de personas
    for persona in data["data"]:
        nombre = persona["nombre"]
        edad = persona["edad"]
        print(f"Nombre: {nombre}, Edad: {edad}")


if __name__ == "__main__":
    main()
