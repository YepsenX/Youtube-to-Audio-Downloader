from pytube import YouTube
from pytube import Playlist

my_playlist = input('URL of Playlist: ')
# convert url to playlist object
my_playlist = Playlist(my_playlist)
save_path = input('Folder Path of Install Folder: ')
total_videos = my_playlist.length
url_list = []

# creates a list of all videos in playlist
print('\n')
x = 0
while x < total_videos:
    url_list.append(my_playlist.video_urls[x])
    x += 1


# Creates a list & function to remove bad characters from file names
def fix_file_name(name):
    bad_chars = ['#', '%', '&', '{', '}', '/', '*', '>', '<', '?', '#', '!', "'", '"', ':', '@', '=', '|', '+', '`', '.']
    for character in bad_chars:
        name = name.replace(character, '')
    return name


# extracts file type from video & creates final file name
def get_file_type(video):
    file_type = video.streams.filter(type='audio').order_by('abr').last()
    file_type = str(file_type)
    x = file_type.find('audio/')
    file_type = (file_type[x+6:x+9])
    # first pass of file name
    file_name = f'{video.title} - {video.author}'
    # sanitize the data
    file_name = fix_file_name(file_name)
    file_type = fix_file_name(file_type)
    # create final file name
    if len(file_name) > 60:
        file_name == file_name[:60]
    if file_type == 'web':
        file_type = 'webm'
    file_name = f'{file_name}.{file_type}'
    return file_name


# Download Videos
while len(url_list) > 0:
    # convert list item to an object
    video = YouTube(url_list[0])
    # create file name
    file_name = get_file_type(video)
    # download the video
    print(f'Starting Download: {file_name}')
    video.streams.filter(type='audio').order_by('abr').last().download(save_path, file_name)
    url_list.remove(url_list[0])

print('\n--------------------------')
print('| All Downloads Complete |')
print('--------------------------')
