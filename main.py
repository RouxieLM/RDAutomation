from config import get_rd_api, get_media_root
from media import create_season_directory, create_show_directory, get_media_type
from scraper import scraper
from download import download
from checkAvailability import check_availability

def main():
    
    print("\nThis application allows automatic downloading and importing of movies, TV shows, and anime into a media library (Plex, Jellyfin...) or a simple folder. It utilizes the Real Debrid API and torrent magnet links.\nThe primary objective of this project is to facilitate the swift and automated importation of entire seasons of TV shows or anime into Plex, Jellyfin or others.\n\n")
    
    input("Press Enter to continue...")

    rd_api = get_rd_api()
    root_path = get_media_root()
    media_type = get_media_type()

    show_path = create_show_directory(root_path, media_type)

    if media_type == "TV Shows" or media_type == "Anime":
        show_path = create_season_directory(show_path)

    magnet, selected_thash = scraper()
    
    check_availability(rd_api, selected_thash)

    download(rd_api, magnet, show_path)

if __name__ == "__main__":
    main()