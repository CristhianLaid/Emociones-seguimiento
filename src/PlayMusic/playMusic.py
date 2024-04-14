import random
import requests
import librosa
import tempfile
import vlc


class PlayMusic:
    def __init__(self):
        self.blink_count = 0
        self.canciones = []
        self.reproductor = vlc.MediaPlayer()
    
    def play_music(self, emotion):
        """
        Reproduce música asociada con la emoción especificada.
        """
        song_to_play = self._get_random_song_by_emotion(emotion)
        
        if song_to_play:
            print(f"Reproduciendo música para la emoción '{emotion}': {song_to_play['titulo']}")
            # Reproducir la canción utilizando el enlace de Deezer
            self.reproductor.set_mrl(song_to_play['preview'])
            self.reproductor.play()  # Iniciar la reproducción
        else:
            print(f"No se encontraron canciones para la emoción '{emotion}'")

        
    
    def reproducir_pausar(self):
        if self.blink_count % 2 == 1:
            # pyautogui.press('space')
            print("pausa")
            
    def cambiar_cancion(self, emotion):
        if self.blink_count % 3 == 0:
            song_to_play = self._get_random_song_by_emotion(emotion)
            if song_to_play:
                print(f"Reproduciendo música para la emoción '{emotion}': {song_to_play['titulo']}")
                self.reproductor.set_mrl(song_to_play['preview'])
                self.reproductor.play()
            else:
                print(f"No se encontraron canciones para la emoción '{emotion}'")
                
            
    
    def incrementar_blink_count(self):
        self.blink_count += 1
        print("Blink count: ", self.blink_count)

    def agregar_canciones_aleatorias_deezer(self, cantidad):
        response = requests.get(f'https://api.deezer.com/chart/0/tracks?limit={cantidad}')
        if response.status_code == 200:
            data = response.json()
            for track in data['data']:
                # Obtener características de la canción
                duracion = track['duration']
                
                # Supongamos que el tempo de una canción rápida es > 120 y lenta es <= 120
                tempo = 120  # Valor predeterminado para canciones de 30 segundos
                
                # Si Deezer proporciona una vista previa, intentamos estimar el tempo
                if 'preview' in track:
                    # Descargar el archivo de audio desde la URL
                    audio_response = requests.get(track['preview'])
                    if audio_response.status_code == 200:
                        # Crear un archivo temporal en disco
                        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
                            tmp_file.write(audio_response.content)
                            tmp_file.seek(0)
                            # Cargar el audio desde el archivo temporal
                            y, sr = librosa.load(tmp_file.name, duration=30)
                            # Calcular el tempo aproximado del fragmento de 30 segundos
                            tempo = librosa.beat.tempo(y=y, sr=sr)[0]  # Estimar el tempo
                    
                # Asignar emoción basada en el tempo (tempo lento = triste, tempo rápido = feliz)
                emocion = self.assign_emotion(tempo)
                
                # Agregar la canción a la lista de canciones con su emoción
                cancion = {
                    'id': track['id'],
                    'titulo': track['title'],
                    'artista': track['artist']['name'],
                    'album': track['album']['title'],
                    'link': track['link'],
                    'preview': track['preview'] if 'preview' in track else None,
                    'duracion': duracion,
                    'tempo': tempo,
                    'emotion': emocion,
                    'imagen': track['album']['cover_medium']
                }
                self.canciones.append(cancion)
            
            print("Canciones de Deezer agregadas:")
            for song in self.canciones:
                print(song)
        else:
            print("Error al obtener canciones de Deezer")
            
    def assign_emotion(self, tempo):
        
        if tempo <= 60:
            return 'disgust'
        elif 60 < tempo <= 80:
            return 'sad'
        elif 80 < tempo <= 100:
            return 'angry'
        elif 100 < tempo <= 120:
            return 'fear'
        elif 120 < tempo <= 140:
            return 'neutral'
        elif 140 < tempo <= 160:
            return 'happy'
        else:
            return 'surprise'
            
    def _get_random_song_by_emotion(self, emotion):
        songs_emotion = [cancion for cancion in self.canciones if cancion['emotion'] == emotion]
        if songs_emotion:
            return random.choice(songs_emotion)
        return None
                
        
# Ejemplo de uso
# if __name__ == "__main__":
#     reproductor = PlayMusic()
#     # Agregar 10 canciones aleatorias de Deezer a la lista de canciones
#     reproductor.agregar_canciones_aleatorias_deezer(10)


