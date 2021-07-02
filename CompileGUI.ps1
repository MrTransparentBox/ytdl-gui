.\.venv\Scripts\Activate.ps1
$release="2021.07.01.f2"
Write-Output "Removing dist/DownloaderGUI folder..."
if (Test-Path .\dist\DownloaderGUI) {Remove-Item .\dist\DownloaderGUI -Recurse}
.\.venv\Scripts\pyinstaller.exe --specpath ".\build" --console -i 'C:\Users\alexj\OneDrive\Pictures\Icons\TransparentBox_1-1.ico' --add-data '../ffmpeg-20200115-0dc0837-win64-static;ffmpeg-20200115-0dc0837-win64-static' --add-data '../appConfig.json;.' --add-data '../Resources;Resources' --add-data '../AtomicParsley-win32-0.9.0;AtomicParsley-win32-0.9.0' --add-data '../tksvg0.7;tksvg0.7' --add-data '../awthemes-10.3.0;awthemes-10.3.0' --add-data '../Logs;Logs' --add-data '../ToDownload.bat;.' .\DownloaderGUI.py
Write-Output "Writing version to release.txt"
Write-Output $release > .\dist\release.txt