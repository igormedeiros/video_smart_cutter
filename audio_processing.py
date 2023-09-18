import ffmpeg

def optimize_audio(stream):
    # Otimiza qualidade do áudio
    stream = stream.filter("atrim", start_second=0, duration=None)
    stream = stream.filter("atempo", duration=1.5)
    stream = stream.filter("asetrate", rate=48000)
    return stream


def remove_silences(stream):
    # Remove os silêncios
    return stream.filter("silenceremove", threshold=-30, length=1000)

def insert_bg_music(stream):
    # Insere trilha de fundo com volume baixo
    return stream.concat(ffmpeg.input("bg_music.mp3"), start_second=0, duration=None,
                           afade= in = 1000, afadeout = 1000, avolume = 0.2)

