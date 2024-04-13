import random
import requests

class PlayMusic:
    def __init__(self):
        self.blink_count = 0
        self.canciones = []
        
    def reproducir_pausar(self):
        if self.blink_count % 2 == 1:
            # pyautogui.press('space')
            print("pausa")
            
    def cambiar_cancion(self):
        if self.blink_count % 3 == 0:
            cancion_actual = random.choice(self.canciones)
            print(cancion_actual)
    
    def incrementar_blink_count(self):
        self.blink_count += 1
        print("Blink count: ", self.blink_count)

    def agregar_canciones_aleatorias_deezer(self, cantidad):
        # Hacer una solicitud a la API de Deezer para obtener una lista de canciones aleatorias
        response = requests.get(f'https://api.deezer.com/chart/0/tracks?limit={cantidad}')
        if response.status_code == 200:
            data = response.json()
            # Extraer los nombres de las canciones aleatorias y añadirlas a la lista de canciones
            for track in data['data']:
                cancion = {
                    'id': track['id'],
                    'titulo': track['title'],
                    'artista': track['artist']['name'],
                    'album': track['album']['title'],
                    'link': track['link'],
                    'preview': track['preview'],
                    'duracion': track['duration'],
                    'rank': track['rank'],
                    'imagen': track['album']['cover_medium']
                }
                self.canciones.append(cancion)
            
            print("Canciones de Deezer agregadas:")
            for song in self.canciones[len(self.canciones)-cantidad:]:
                print(song)
        else:
            print("Error al obtener canciones de Deezer")

# Ejemplo de uso
if __name__ == "__main__":
    reproductor = PlayMusic()
    # Agregar 10 canciones aleatorias de Deezer a la lista de canciones
    reproductor.agregar_canciones_aleatorias_deezer(10)


