import os
from pick import pick

def get_media_type():
    title = "Please choose the type of media you want to import: "
    media_type = ['TV Shows', 'Anime']

    media_type, index = pick(media_type, title, indicator='->')

    return media_type

def create_show_directory(root_path, media_type):
    show_name = input(f"Please provide the name of the {media_type}. This will be the name of the show's folder: ")
    if os.path.exists(root_path):
        show_path = os.path.join(root_path, media_type, show_name)
        print(show_path)
    else:
        print("Error, plex path not found.")
        exit(1)

    if not os.path.exists(show_path):
        os.makedirs(show_path)
    else:
        print(f"{show_path} folder already exists.")

    return show_name, show_path

def create_season_directory(show_path):
    season = input("Please provide which season you are importing, only type a number. This will be the season's folder: ")
    season_path = os.path.join(show_path, f'Season {season}')

    if not os.path.exists(season_path):
        os.makedirs(season_path)
        print(f"successfully created {season_path} folder.")
    else:
        print(f'{season_path} folder already exists.')

    return season_path, season