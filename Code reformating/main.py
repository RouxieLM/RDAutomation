from config import get_rd_api, get_media_root

def main():
    
    print("\nThis application enables automatic downloading and importing of movies, TV shows, and anime into a Plex media library. It utilizes the Real Debrid API and Torrents magnet links. The primary objective of this project is to facilitate the swift and automated importation of entire seasons of TV shows or anime into Plex.\n\nIf you want to reset your settings, simply delete all the files except for main.py.\n\n")
    
    input("Press Enter to continue...")

    rd_api = get_rd_api()
    root_path = get_media_root()

if __name__ == "__main__":
    main()