import pytube
import ffmpy
import os
import PySimpleGUI as sg

sg.theme('Dark')

layout = [  [sg.Text('Kopiëer het webadres vanuit Youtube hieronder')],
            [sg.Text('Plak webadres (ctrl-v):'), sg.InputText()],
            [sg.Text('Kies een naam voor de video:'), sg.InputText()],
            [sg.Text('Kies een map om in te bewaren:'), sg.In(), sg.FolderBrowse(button_text="Bladeren")],
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
        folder = values[2]+"/"

        try:
            video = pytube.YouTube(url)

        except pytube.exceptions.RegexMatchError:
            window.close()
            sg.popup("De URL wordt niet herkend.", auto_close=False, keep_on_top=True)
            break

        for stream in video.streams:
            if 'video/mp4' in str(stream) and '1080p' in str(stream):
                print(stream)
                vtag = str(stream)[15:18]


        try:
            vstream = video.streams.get_by_itag(vtag)

        except NameError:
            window.close()
            sg.popup("De video lijkt niet in HD (1080p) beschikbaar te zijn.", auto_close=False, keep_on_top=True)
            break

        astream = video.streams.get_by_itag(140)

        vstream.download(filename="vstream")
        astream.download(filename="astream")

        ff = ffmpy.FFmpeg(
                inputs={"vstream.mp4": None, "astream.mp4" : None},
                outputs={f'{folder}{vidname}.mp4': '-c:v copy -c:a copy -pix_fmt yuv420p'}
            )
        ff.run()

        os.remove("vstream.mp4")
        os.remove('astream.mp4')

        window.close()

        sg.popup(f"Klaar!\nCheck de folder voor je video met filenaam:\n{vidname}.mp4", auto_close=False, keep_on_top=True)
