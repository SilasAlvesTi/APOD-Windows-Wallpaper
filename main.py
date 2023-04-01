import ctypes, os

import requests
import dotenv
from PIL import Image, ImageOps


def pegar_imagem():
    response = requests.get('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY')
    response_json = response.json()
    url_imagem = response_json['url']
    
    with open('temp.jpg', 'wb') as handler:
        handler.write(requests.get(url_imagem).content)

def definir_imagem_como_wallpaper():
    path = os.getcwd() + '\\temp.jpg'

   
    if not (os.path.exists(os.getcwd()+'\\.env')):
        pegar_resolucao_usuario()

    dotenv.load_dotenv()
    tupla_em_string = f'({os.getenv("RESOLUCAO_X")}, {os.getenv("RESOLUCAO_Y")})'
    resolucao = eval(tupla_em_string)
    redimensionar_imagem('temp.jpg', resolucao)
    
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)

def pegar_resolucao_usuario():
    imagem_resolucao_x = input("Qual o maior valor da resolução do seu monitor(Ex.: 1280): ")
    imagem_resolucao_y = input("Qual o menor valor da resolução do seu monitor(Ex.: 720): ")

    path_dotenv = os.getcwd()+'\\.env'
    dotenv.set_key(path_dotenv, "RESOLUCAO_X", imagem_resolucao_x)
    dotenv.set_key(path_dotenv, "RESOLUCAO_Y", imagem_resolucao_y)
    
def redimensionar_imagem(image_path, target_size=(1920, 1080)):
    # Abrir a imagem original
    image = Image.open(image_path)

    # Obter as dimensões da imagem original
    original_size = image.size

    # Calcular a quantidade de espaço extra necessário
    extra_width = target_size[0] - original_size[0]
    extra_height = target_size[1] - original_size[1]

    # Adicionar bordas pretas à imagem
    padding_left = extra_width // 2
    padding_right = extra_width - padding_left
    padding_top = extra_height // 2
    padding_bottom = extra_height - padding_top
    image = ImageOps.expand(image, (padding_left, padding_top, padding_right, padding_bottom), fill='black')

    image.save('temp.jpg')

if __name__ == '__main__':
    pegar_imagem()
    definir_imagem_como_wallpaper()
    
