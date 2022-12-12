from pytube import YouTube
from pytube import Playlist

my_playlist = input('URL of Playlist: ')
# convert url to playlist object
my_playlist = Playlist(my_playlist)
save_path = input('Install Folder Path: ')
total_videos = my_playlist.length
actual_length = 0
url_list = []
unavailable_videos = []

# Create a list containing URLs of every video in the playlist
try:
    print('\nChecking videos in playlist...')
    x = 0
    for i in range(total_videos):
        url_list.append(my_playlist.video_urls[x])
        actual_length += 1
        x += 1
# This error will occur if there are privated / removed videos present in the playlist
except IndexError or StopIteration:
    print(f'\nWarning: removed videos exist in playlist.\n{actual_length} of {total_videos} available.')
    total_videos = actual_length


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
    try:
        # convert list item to an object
        video = YouTube(url_list[0])
        # create file name
        file_name = get_file_type(video)
        # download the video
        print(f'Downloading: {file_name}')
        video.streams.filter(type='audio').order_by('abr').last().download(save_path, file_name)
        url_list.remove(url_list[0])
    # If a video is unable to download, it will be skipped, then reported when the program is finished
    except KeyError:
        print(f'Error: A video is unable to download')
        unavailable_videos.append(url_list[0])
        url_list.remove(url_list[0])


print('\n--------------------------')
print('| All Downloads Complete |')
print('--------------------------')

# notifies user of any videos that were unable to download
if len(unavailable_videos) > 0:
    print('\nSome videos were not able to be downloaded.\nVideos in question:')
    for i in unavailable_videos:
        print(i)
