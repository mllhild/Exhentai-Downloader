# Exhentai-Downloader
Light weight downloader for exhentai.org

## Install

0. Install Python, Pythong Request Package, Python BeautifulSoup4 Package (ask chatgpt for help with that if you need)

1. download the files and put them where you want your exhentai downloads to go

2. go to exhentai.org and get your cookies

2.5 if you dont have a cookie extension, this is the one I use https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?hl=en-US

3. open "downloadScript.py" with notepad and replace the values of your cookies

COOKIES = {
        'ipb_member_id': 'XXXXXX',
        'ipb_pass_hash': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        'igneous': 'XXXXXXXXXXXXXX'
    }

4. Add your links to "GalleriesToDownload.txt"

5. Run "Run.bat"

## Do do List
- make an updater that checks for updates of galleries you already downloaded
