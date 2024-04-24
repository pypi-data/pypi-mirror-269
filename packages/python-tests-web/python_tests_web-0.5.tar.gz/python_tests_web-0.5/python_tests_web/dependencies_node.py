import subprocess

def get_npm_path():
    try:
        npm_path = subprocess.check_output('powershell "Get-Command npm | %{$_.Source}"', shell=True).decode().strip()
        return npm_path
    except subprocess.CalledProcessError as e:
        print("No se pudo encontrar la ruta a npm.")
        print(str(e))
        return None

def install_and_check(package, npm_path):
    if npm_path is None:
        print("No se puede instalar el paquete sin una ruta válida a npm.")
        return
    try:
        print(f"Instalando {package}...")
        subprocess.check_call([npm_path, "install", "-g", package])
        print(f"Verificando la instalación de {package}...")
        subprocess.check_call([package, "--version"])
        print(f"{package} instalado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Hubo un error al instalar {package}.")
        print(str(e))

if __name__ == "__main__":
    npm_path = get_npm_path()
    # install_and_check("allure", npm_path)
    install_and_check("cucumber", npm_path)