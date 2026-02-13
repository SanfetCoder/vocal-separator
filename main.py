import demucs.api
import os
import torch

separator = demucs.api.Separator()

def separate_audio_file(filename, original_audio_folder = "original-audios"):
    sources = {}

    origin, separated = separator.separate_audio_file(f"{original_audio_folder}/{filename}")

    for stem, source in separated.items():
        sources[stem] = source

    return sources


def create_song_without_vocal(song_name, sources):
    stem_to_exclude = ['vocals']
    
    # 1. Initialize an empty tensor for the backing track
    # We use the shape of one of the existing stems (e.g., 'drums')
    drum_source = sources['drums']
    backing_track = torch.zeros_like(drum_source)

    # 2. Integrate all stems to the backing_track 
    source_stems = sources.keys()
    stems_to_include = [stem for stem in source_stems if stem not in stem_to_exclude]

    for stem in stems_to_include:
        if stem in sources:
            backing_track += sources[stem]

    # 3. Save the final Backing Track
    output_dir = "backing-tracks"
    os.makedirs(name = output_dir, exist_ok=True)

    output_path = os.path.join(output_dir,f"{song_name}.wav")
    demucs.api.save_audio(backing_track, output_path, samplerate=separator.samplerate)

def make_karaoke_song(filename : str, song_name : str):
    separated_sources = separate_audio_file(filename=filename)

    print("Separated source!!")

    create_song_without_vocal(song_name, separated_sources)

    print("Created the song without vocals!!")


filename = input("Please provide file name : ")
song_name = input("Please provide song name : ")

make_karaoke_song(filename, song_name)