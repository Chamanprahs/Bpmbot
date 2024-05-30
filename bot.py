import os
import librosa
import numpy as np
from pydub import AudioSegment
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Get the bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me an audio file and I will tell you its BPM and key.')

def audio_handler(update: Update, context: CallbackContext) -> None:
    file = update.message.audio.get_file()
    file_path = file.download()

    # Convert to wav format if necessary
    if not file_path.endswith('.wav'):
        audio = AudioSegment.from_file(file_path)
        file_path = file_path + '.wav'
        audio.export(file_path, format='wav')

    # Analyze the audio file
    y, sr = librosa.load(file_path, sr=None)
    bpm = librosa.beat.tempo(y, sr=sr)[0]
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)
    scale = librosa.hz_to_note(librosa.note_to_hz(np.argmax(chroma_mean)))

    # Clean up the downloaded file
    os.remove(file_path)

    update.message.reply_text(f'BPM: {bpm}\nScale: {scale}')

def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.audio, audio_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
