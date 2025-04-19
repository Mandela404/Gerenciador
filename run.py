import os
import sys

if __name__ == "__main__":
    print("Iniciando o Gerenciador de Tarefas...")

    try:
        os.system("python Tasks-Manager.py")
    except Exception as e:
        print("Erro ao iniciar a aplicacao:", e)
        sys.exit(1)
