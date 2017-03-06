#!/usr/bin/env python

#from moviepy.editor import *
import subprocess

sample_clips_data = [
{
    'src_filename': "GOPR0214.MP4",
    'output_filename': "test1.mp4",
    'clip_in': 6,
    'clip_out': 8}]


# GOPRO189.MP4|worm_burner_save 1:59 2:17|ninja_stick_save 2:12 2:15 |flow_to_crash 2:23 3:00| crash 2:52 3:00
def get_timecode(input_str):
    contains_dot=False
    if ( '.' in input_str):
        contains_dot=True

    new_toks=[]
    toks = input_str.split(':')
    for tok in toks:
        tok = tok.zfill(2)
        new_toks.append(tok)

    new_string = ':'.join(new_toks)

    if contains_dot:
        return "00:" + new_string
    else:
        return "00:" + new_string + ".0"

def read_in_clips_data(file):
    data = []
    with open(file) as fh:
        lines = fh.read().splitlines()

    for line in lines:
        #print line
        if ( line[0] == '#'):
            continue
        elems = line.split('|')
        raw_filename = elems[0].split('|')[0]
        raw_filename_sub = elems[0].split('|')[0].split(".")[0]
        subclips = elems[1:]
        for clip in subclips:
            elem = {}
            try:
                elem['src_filename']=raw_filename
                start_time = get_timecode(clip.split()[1])
                end_time = get_timecode(clip.split()[2])
                elem['output_filename']=raw_filename_sub + "_%s_%s_%s.MP4" % ( clip.split()[0], start_time.replace(':','.'), end_time.replace(':','.') )
                elem['clip_in']="%s" % ( start_time )
                elem['clip_out']="%s" % ( end_time )
                data.append(elem)
            except:
                pass

    return data

if __name__ == '__main__':
    raw_dir="raw"
    clips_dir="clips"

    # print get_timecode("0:29")
    # print get_timecode("29")
    # print get_timecode("56")
    # print get_timecode("1:22.30")

    video_file = "videos.txt"
    clips = read_in_clips_data(video_file)

    for clip in clips:
        print "%s %s %s" % ( raw_dir + "/" + clip['src_filename'], clip['clip_in'], clip['clip_out'])
        print "%s" % ( clips_dir + "/" + clip['output_filename'])

        # mpy_clip = VideoFileClip(raw_dir +"/" + clip['src_filename']).subclip(clip['clip_in'], clip['clip_out'])
        # #print (clip.fps)
        # mpy_clip.write_videofile(clips_dir + "/" + clip['output_filename']) # codec='libx264')#, audio_codec='fdkaac') #, write_logfile=True) 
        #
        #ffmpeg -i raw/GOPR0184.MP4 -c copy -ss 00:01:24 -to 00:01:30 newfile.mp4
        subprocess.call(['ffmpeg', '-i', '%s' % (raw_dir + "/" + clip['src_filename']), '-c', 'copy', '-ss',  '%s' % (clip['clip_in']), '-to', '%s' % (clip['clip_out']),  
            '%s' % (clips_dir + "/" + clip['output_filename'])])
