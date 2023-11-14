from datetime import datetime, timedelta # baraye tanzim zaman bandi 
import re # baraye regular expression 


# bakhsh bandi va tajzye zamanbandi subtitle ha
def parse_subtitle_time(time_str):
    match = re.match(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', time_str) # dar in bakh avalin string ha check mishavand 
    if match: # agar hamsan va motaadel bod 
        hours, minutes, seconds, milliseconds = map(int, match.groups()) # az zaman bandi haye moshakhas yek list koli ijad mishavad ta tatbig dade shavand
        return timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds) # timedelta baraye mohasebe tafavot tarikh ha estefade mishavad 
    else:
        return None

def sync_subtitles(subtitle_file1, subtitle_file2, output_file):
    '''
    da in function say mishavad ta 2 file subtitle khande shavad va da akharin line 
    az variable ke ijad kardim yek khoroji(output) moshakhasi begirim
    '''
    with open(subtitle_file1, 'r', encoding='utf-8') as file1, \
         open(subtitle_file2, 'r', encoding='utf-8') as file2, \
         open(output_file, 'w', encoding='utf-8') as output:
        
        subtitles1 = file1.read().split('\n\n') # khandan data haye hardo subtitle
        subtitles2 = file2.read().split('\n\n') # "
        
        # estefade az halge baraye tekrar zir nevis ha baraye sync kardan ya timebandi hamzamn timestamp(bakhsh) haye zamani 
        for sub1, sub2 in zip(subtitles1, subtitles2): # zip (jam bandi bakhsh haye mokhtalef va map kardan index haye moshabeh)
            lines1 = sub1.split('\n')
            lines2 = sub2.split('\n')
            
            if len(lines1) >= 2 and len(lines2) >= 2: # tagsim bandi va megdar bandi baraye line haye 1 va 2
                time_str1 = lines1[1]
                time_str2 = lines2[1]
                
                # tajzye zaman bandi subtitle ha
                start_time1 = parse_subtitle_time(time_str1.split(' --> ')[0])
                start_time2 = parse_subtitle_time(time_str2.split(' --> ')[0])
                
                if start_time1 is not None and start_time2 is not None:
                    time_difference = start_time2 - start_time1
                    '''
                     tanzim zaman bandi subtitle aval ba subtitle dovom baraye bakhsh haye zamani hamsan
                    (-->) baraye hashye nevisi tabe estefade mishavad baraye peyvash argument ha ya bray return tavabe estefade mishavad  
                    '''
                    for i in range(2, len(lines2)):
                        time_range = re.split(' --> ', lines2[i]) 
                        if len(time_range) == 2:
                            start_time = parse_subtitle_time(time_range[0]) + time_difference
                            end_time = parse_subtitle_time(time_range[1]) + time_difference
                            lines2[i] = f'{start_time.strftime("%H:%M:%S,%f")[:-3]} --> {end_time.strftime("%H:%M:%S,%f")[:-3]}'
                
            # neveshtane file khoroji va output subtitle haye hamsan sazi shoode
            output.write('\n'.join(lines2) + '\n\n')

# File haye subtitle va khoroji an 
SF1 = "de_70105212.vtt"
SF1 = "en_70105212.vtt"
output_file = "Sobhansanati(SyncedSubtitles).vtt"
    
sync_subtitles(SF1,SF1,output_file)
print(f"Synced subtitles written to {output_file}")
