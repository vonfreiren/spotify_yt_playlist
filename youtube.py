from pytube import Search

def search_youtube(filename):
    s = Search(filename)
    if len(s.results)>0:
        return s.results[0].watch_url, s.results[0].video_id