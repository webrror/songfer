# Songfer (album_art_test branch)
##### Tested on Ubuntu 20.04, WSL (Ubuntu 22.04.1 LTS) and macOS 12
A python tool to retrieve album arts and transfer songs from Spotify to YouTube Music.


## Prerequisites

- [Python with pip](https://www.python.org/downloads/)

- [Spotipy](https://spotipy.readthedocs.io/en/master/)

  ```
  pip3 install spotipy
  ```
- [ytmusicapi](https://ytmusicapi.readthedocs.io/en/latest/) (For Spotify to YouTube Music transfer)

  ```
  pip3 install ytmusicapi
  ```
> [!NOTE]
> #### Make sure to also follow [this](https://ytmusicapi.readthedocs.io/en/latest/setup.html#authenticated-requests) part of the ytmusicapi if you want to transfer songs

- [viu](https://github.com/atanunq/viu) (For viewing images from the terminal)

## Usage

Run the following command
```
python3 songfer.py
```

## Some issues you might encounter

- ### Browser not opening for auth while using Songfer on WSL

  #### As of Ubuntu 22.04, `wslu` isn't a default package. This allowed you to open link in default Windows browser.
  
    Setting the BROWSER variable to point to installation path of browser on Windows might help fix this issue: 

    ```
    export BROWSER=/mnt/c/path/to/your/windows/browser
    ```

    Example to set MS Edge 

    ```
    export BROWSER=/mnt/c/Program\ Files\ \(x86\)//Microsoft/Edge/Application/msedge.exe
    ```

- ### If you find any, let me know

## Credit

<a href="https://gist.github.com/iannase/38427b791a860a1f791b5fbba1791592">@iannase</a>
