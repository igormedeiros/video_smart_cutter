import os

import ffmpeg

from audio_processing import optimize_audio
from audio_processing import remove_silences
from config import config

output_folder = config['output_folder']

def cut_video(video_path, cuts):
    # Realiza os cortes, gerando vídeos mp4 salvando todos numa pasta
    for start, end in cuts:
        output_path = os.path.join(output_folder, f"short_{start}_{end}.mp4")
        ffmpeg.output(
            input=video_path,
            output=output_path,
            start_second=start,
            end_second=end,
        )


def insert_video_inserts(stream):
    # Insere vídeos auxiliares (inserts - sem som)
    for insert_path in os.listdir("inserts"):
        stream = stream.concat(ffmpeg.input("inserts/" + insert_path))


def process_videos(folder):
    # Itera na pasta videos_processed e processa cada video
    for video_path in os.listdir(folder):
        # Carrega o vídeo
        stream = ffmpeg.input(f"{output_folder}/" + video_path)

        stream = optimize_audio(stream)

        stream = remove_silences(stream)

        stream = insert_video_inserts(stream)

        stream = insert_bg_music(stream)

        # Concatena com video de end card final
        stream = stream.concat(ffmpeg.input("end_card.mp4"), start_second=0, duration=None)

        # Gera a legenda .str
        transcript = transcript.split("\n")
        subtitles = generate_subtitles(transcript, start, end)
        with open("subtitles.str", "w") as f:
            f.write(subtitles)

        # Insere a legenda animada
        stream = insert_subtitles(stream, "subtitles.str")

        # Renderiza
        output_path = os.path.splitext(video_path)[0] + ".mp4"
        ffmpeg.output(
            input=stream,
            output=output_path,
        )

        # Coloca na planilha excel
        add_video_to_excel(output_path)
