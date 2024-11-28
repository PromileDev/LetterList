import os 

directorio_actual = os.path.dirname(os.path.abspath(__file__))
directorio_padre = os.path.abspath(os.path.join(directorio_actual, os.pardir))

def new_client(name):
     
    ruta_final = os.path.join(directorio_padre, "frontend", "src", "pages", "clients", str(name))
    if not os.path.exists(ruta_final):
        os.mkdir(ruta_final)


def new_page(name, client):
    ruta_final = os.path.join(directorio_padre, "frontend", "src", "pages", "clients", str(client), str(name))
    os.mkdir(ruta_final)