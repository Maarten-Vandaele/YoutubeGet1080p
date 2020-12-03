import pytube
import ffmpy
import os
import PySimpleGUI as sg

sg.theme('Dark')

layout = [  [sg.Text('Kopiëer het webadres vanuit Youtube hieronder')],
            [sg.Text('Plak webadres (ctrl-v):'), sg.InputText()],
            [sg.Text('Kies een naam voor de video:'), sg.InputText()],
            [sg.Text('Status:'), sg.Text("Downloading...",key='-OUT-',visible=False)],
            [sg.Button('Download video'), sg.Button('Annuleer')] ]

window = sg.Window('Download HD Youtube video', layout, keep_on_top=True)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Annuleer': # if user closes window or clicks cancel
        break
    elif event == 'Download video':

        window['-OUT-'].update(visible=True)
        window.Refresh()

        url = values[0]
        vidname = values[1]

        video = pytube.YouTube(url)

        for stream in video.streams:   #get itag for video
            if 'video/mp4' in str(stream) and '1080p' in str(stream):
#               print(stream)
                vtag = str(stream)[15:18]
#               print(vtag)

        vstream = video.streams.get_by_itag(vtag)
        astream = video.streams.get_by_itag(140)

        vstream.download(filename="vstream")
        astream.download(filename="astream")

        ff = ffmpy.FFmpeg(
                inputs={"vstream.mp4": None, "astream.mp4" : None},
                outputs={f'{vidname}.mp4': '-c:v copy -c:a copy -pix_fmt yuv420p'}
            )
        ff.run()

        os.remove("vstream.mp4")
        os.remove('astream.mp4')

        window.close()

        sg.popup(f"Klaar!\nCheck de folder voor je video met filenaam:\n{vidname}.mp4", auto_close=True, auto_close_duration=30, keep_on_top=True)