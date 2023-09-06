from config import get_rd_api, get_media_root

def main():
    
    print("\nThis application allows automatic downloading and importing of movies (soon), TV shows, and anime into a media library (Plex, Jellyfin...) or a simple folder. It utilizes the Real Debrid API and torrent magnet links.\nThe primary objective of this project is to facilitate the swift and automated importation of entire seasons of TV shows or anime into Plex, Jellyfin or others.\n\n")
    
    input("Press Enter to continue...")

    rd_api = get_rd_api()
    root_path = get_media_root()

if __name__ == "__main__":
    main()