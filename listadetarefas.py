import PySimpleGUI as sg
import psycopg2

# Função para conectar ao banco de dados PostgreSQL


def connect_to_database():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="thallestodo",
            user="postgres",
            password="cicada3301"

        )
        return connection
    except Exception as e:
        sg.popup_error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para buscar todas as tarefas da tabela


def fetch_tasks(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tarefas;")
        return cursor.fetchall()

# Função para adicionar uma nova tarefa à tabela


def add_task(connection, description):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO tarefas (descricao) VALUES (%s);", (description,))
        connection.commit()

# Função para remover uma tarefa da tabela


def remove_task(connection, task_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM tarefas WHERE id=%s;", (task_id,))
        connection.commit()


def load_all_tasks(connection):
    tasks = fetch_tasks(connection)
    return [f"{task[0]} - {task[1]}" for task in tasks]


# Layout da GUI
layout = [
    [sg.Text("Tarefa:"), sg.InputText(key="-TASK-"), sg.Button("Adicionar")],
    [sg.Listbox(values=[], size=(60, 20), key="-TASKS-"),
     sg.Button("Remover")],
    [sg.Button("Sair"), sg.Button("Carregar Tarefas")]
]

# Criar a janela
window = sg.Window("T00ru To-Do", layout)

# Conectar ao banco de dados
connection = connect_to_database()

# Loop principal do aplicativo
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Sair":
        break

    if event == "Adicionar" and values["-TASK-"]:
        add_task(connection, values["-TASK-"])
        tasks = fetch_tasks(connection)
        window["-TASKS-"].update(values=[task[1] for task in tasks])

    if event == "Remover" and values["-TASKS-"]:
        selected_task = values["-TASKS-"][0]
        tasks = fetch_tasks(connection)
        for task in tasks:
            if task[1] == selected_task:
                remove_task(connection, task[0])
                break

        tasks = fetch_tasks(connection)
        window["-TASKS-"].update(values=[task[1] for task in tasks])

    if event == "Atualizar":
        tasks = load_all_tasks(connection)
        window["-TASKS-"].update(values=tasks)

# Fechar a janela e a conexão com o banco de dados
window.close()
if connection:
    connection.close()
