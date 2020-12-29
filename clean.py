import shutil
from datetime import date
import os
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from time import sleep
from watchdog.observers import Observer

extension_paths = {
        # No name
        'noname':  'Others/UnCategorised',
        # audio
        '.cda':    'Media/Audio',
        '.aif':    'Media/Audio',
        '.mid':    'Media/Audio',
        '.midi':   'Media/Audio',
        '.mp3':    'Media/Audio',
        '.mpa':    'Media/Audio',
        '.ogg':    'Media/Audio',
        '.wav':    'Media/Audio',
        '.wma':    'Media/Audio',
        '.wpl':    'Media/Audio',
        '.m3u':    'Media/Audio',
        # text
        '.txt':    'Text/Texts',
        '.doc':    'Work/Word',
        '.docx':   'work/Word',
        '.odt ':   'Text/Texts',
        '.pdf':    'Text/PDF',
        '.rtf':    'Text/Texts',
        '.tex':    'Text/Texts',
        '.wks ':   'Text/Texts',
        '.wps':    'Text/Texts',
        '.wpd':    'Text/Texts',
        # video
        '.3g2':    'Media/Videos',
        '.3gp':    'Media/Videos',
        '.avi':    'Media/Videos',
        '.flv':    'Media/Videos',
        '.h264':   'Media/Videos',
        '.m4v':    'Media/Videos',
        '.mkv':    'Media/Videos',
        '.mov':    'Media/Videos',
        '.mp4':    'Media/Videos',
        '.mpg':    'Media/Videos',
        '.mpeg':   'Media/Videos',
        '.rm':     'Media/Videos',
        '.swf':    'Media/Videos',
        '.vob':    'Media/Videos',
        '.wmv':    'Media/Videos',
        # images
        '.ai':     'Media/Images',
        '.bmp':    'Media/Images',
        '.gif':    'Media/Images',
        '.jpg':    'Media/Images',
        '.jpeg':   'Media/Images',
        '.png':    'Media/Images',
        '.ps':     'Media/Images',
        '.psd':    'Media/Images',
        '.svg':    'Media/Images',
        '.tif':    'Media/Images',
        '.tiff':   'Media/Images',
        '.cr2':    'Media/Images',
        # internet
        '.asp':    'Others/Internet',
        '.aspx':   'Others/Internet',
        '.cer':    'Others/Internet',
        '.cfm':    'Others/Internet',
        '.cgi':    'Others/Internet',
        '.pl':     'Others/Internet',
        '.css':    'Others/Internet',
        '.htm':    'Others/Internet',
        '.js':     'Others/Internet',
        '.jsp':    'Others/Internet',
        '.part':   'Others/Internet',
        '.php':    'Others/Internet',
        '.rss':    'Others/Internet',
        '.xhtml':  'Others/Internet',
        '.html':   'Others/Internet',
        # compressed
        '.7z':     'Others/Compressed',
        '.arj':    'Others/Compressed',
        '.deb':    'Others/Compressed',
        '.pkg':    'Others/Compressed',
        '.rar':    'Others/Compressed',
        '.rpm':    'Others/Compressed',
        '.tar.gz': 'Others/Compressed',
        '.z':      'Others/Compressed',
        '.zip':    'Others/Compressed',
        # disc
        '.bin':    'Others/System-Images',
        '.dmg':    'Others/System-Images',
        '.iso':    'Others/System-Images',
        '.toast':  'Others/System-Images',
        '.vcd':    'Others/System-Images',
        # data
        '.csv':    'Others/Database',
        '.dat':    'Others/Database',
        '.db':     'Others/Database',
        '.dbf':    'Others/Database',
        '.log':    'Others/Database',
        '.mdb':    'Others/Database',
        '.sav':    'Others/Database',
        '.sql':    'Others/Database',
        '.tar':    'Others/Database',
        '.xml':    'Others/Database',
        '.json':   'Others/Database',
        # executables
        '.apk':    'Others/Executables',
        '.bat':    'Others/Executables',
        '.com':    'Others/Executables',
        '.exe':    'Others/Executables',
        '.gadget': 'Others/Executables',
        '.jar':    'Others/Executables',
        '.wsf':    'Others/Executables',
        # fonts
        '.fnt':    'Others/Fonts',
        '.fon':    'Others/Fonts',
        '.otf':    'Others/Fonts',
        '.ttf':    'Others/Fonts',
        # presentations
        '.key':    'Work/Presentations',
        '.odp':    'Work/Presentations',
        '.pps':    'Work/Presentations',
        '.ppt':    'Work/Presentations',
        '.pptx':   'Work/Presentations',
        # programming
        '.c':      'Programming/C,C++',
        '.class':  'Programming/Java',
        '.java':   'Programming/Java',
        '.py':     'Programming/Python',
        '.sh':     'Programming/Shell',
        '.h':      'Programming/C,C++',
        '.rb':     'Programming/SonicPI'
        '.vbs'     'Programming/VisualBasicScript',
        # spreadsheets
        '.ods':    'Work/Excel',
        '.xlr':    'Work/Excel',
        '.xls':    'Work/Excel',
        '.xlsx':   'Work/Excel',
        # system
        '.bak':    'Others/System',
        '.cab':    'Others/System',
        '.cfg':    'Others/System',
        '.cpl':    'Others/System',
        '.cur':    'Others/System',
        '.dll':    'Others/System',
        '.dmp':    'Others/System',
        '.drv':    'Others/System',
        '.icns':   'Others/System',
        '.ico':    'Others/System',
        '.ini':    'Others/System',
        '.lnk':    'Others/System',
        '.msi':    'Others/System',
        '.sys':    'Others/System',
        '.tmp':    'Others/System'
}


def add_date_to_path(path: Path):
    dated_path = path / f'{date.today().year}' / f'{date.today().strftime("%B")}'
    dated_path.mkdir(parents=True, exist_ok=True)
    return dated_path


def rename_file(source: Path, destination_path: Path):
    if Path(destination_path / source.name).exists():
        increment = 0

        while True:
            increment += 1
            new_name = destination_path / f'{source.stem}{increment}{source.suffix}'

            if not new_name.exists():
                return new_name
    else:
        return destination_path / source.name


class EventHandler(FileSystemEventHandler):
    def __init__(self, watch_path: Path, destination_root: Path):
        self.watch_path = watch_path.resolve()
        self.destination_root = destination_root.resolve()

    def on_modified(self, event):
        for child in self.watch_path.iterdir():
            # skips non-specified extensions
            if child.is_file() and child.suffix.lower() in extension_paths:
                destination_path = self.destination_root / extension_paths[child.suffix.lower()]
                destination_path = add_date_to_path(path=destination_path)
                destination_path = rename_file(source=child, destination_path=destination_path)
                shutil.move(src=child, dst=destination_path)
            if child.is_dir():
                destination_path = self.destination_root / os.path.join('/home/vageesh/Documents/Organiser', 'Directories')
                destination_path = add_date_to_path(path=destination_path)
                destination_path = rename_file(source=child, destination_path=destination_path)
                shutil.move(src=child, dst=destination_path)


if __name__ == '__main__':
    watch_path = Path.home() / 'Desktop'
    destination_root = Path.home() / 'Documents/Organiser'
    event_handler = EventHandler(watch_path=watch_path, destination_root=destination_root)

    observer = Observer()
    observer.schedule(event_handler, f'{watch_path}', recursive=True)
    observer.start()

    try:
        while True:
            sleep(60)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()