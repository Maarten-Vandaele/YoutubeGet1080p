#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pytube
import ffmpy
import os


# In[2]:


url = input("Input URL: ")


# In[3]:


vidname = input("Input videoname: ")


# In[4]:


video = pytube.YouTube(url)


# In[5]:


for stream in video.streams:   #get itag for video
     if 'video/mp4' in str(stream) and '1080p' in str(stream):
#             print(stream)
            vtag = str(stream)[15:18]
#             print(vtag)


# In[6]:


vstream = video.streams.get_by_itag(vtag)
astream = video.streams.get_by_itag(140)


# In[7]:


print('downloading...')


# In[8]:


vstream.download(filename="vstream")
astream.download(filename="astream")


# In[9]:


ff = ffmpy.FFmpeg(
         inputs={"vstream.mp4": None, "astream.mp4" : None},
         outputs={f'{vidname}.mp4': '-c:v copy -c:a copy -pix_fmt yuv420p'}
     )
ff.run()


# In[10]:


os.remove("vstream.mp4")
os.remove('astream.mp4')


# In[11]:


print('done')


# In[ ]:




