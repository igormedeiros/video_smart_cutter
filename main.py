import ffmpeg
import nltk
import transformers
import openai
import os


# [OK] 1 - recebe o vídeo mp4 completo
# [OK] 2 - transcreve com openai whisper
# [OK] 2 - identifica os pontos de cortes de até 1 min
# 3 - realiza os cortes, gerando vídeos mp4 salvando todos numa pasta videos_processed
# 4 - itera na pasta videos_processed e processa cada video
# 5 -   otimiza qualidade do áudio
# 6 -   remove os silêncios
# 7 -   insere vídeos auxiliares (inserts - sem som)
# 8 -   insere trilha de fundo com volume baixo
# 9 -   concatena com video de end card final
# 10 -  gera a legenda .str
# 11 -  insere a legenda animada
# 12 -  renderiza
# 13 -  coloca na planilha excel

def identify_cuts(video):
    """
    Identifica cortes inteligentes no vídeo com base no conteúdo textual.

    Args:
    - video: Caminho para o vídeo original.

    Returns:
    - cuts: Lista de pontos de corte identificados.
    """

    # Carrega o vídeo MP4
    stream = ffmpeg.input(video)

    # Separa o áudio
    audio = stream.audio

    # Transcreve o áudio com OpenAI Whisper
    transcript = openai.engine("davinci").text.generate(prompt="Transcrever o áudio do vídeo:", audio=audio)

    # Analisa com módulo de processamento de linguagem natural gratuito, os trechos que fazem sentido e que tenha menos de 1 minuto de duração
    sentences = nltk.sent_tokenize(transcript)
    cuts = []
    for i in range(len(sentences)):
        if i == 0 or i == len(sentences) - 1:
            continue

        # Verifica se o trecho tem menos de 1 minuto de duração
        if len(sentences[i - 1]) + len(sentences[i]) + len(sentences[i + 1]) < 60:
            # Usa um modelo de linguagem para avaliar o texto
            model = transformers.AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
            outputs = model(sentences[i - 1] + " " + sentences[i] + " " + sentences[i + 1])
            score = outputs[0]["logits"][0]

            if score > 0.5:
                cuts.append((sentences[i - 1], sentences[i + 1]))

    # Retorna uma coleção de inícios e fins
    return [
        (audio.start_second + sentence[0].start_time, audio.start_second + sentence[1].start_time)
        for sentence in cuts
    ]

def main():
    # Recebe o vídeo mp4 completo
    video_path = input("Informe o caminho do vídeo mp4 completo: ")

    # Identifica os pontos de cortes de até 1 min
    cuts = identify_cuts(video_path)

    output_folder = 'videos_processed'

    cut_video(video_path, cuts)
    proccess_short_videos(output_folder)

if __name__ == "__main__":
    main()




