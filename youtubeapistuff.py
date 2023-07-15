from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from dotenv import load_dotenv
import os
import openai
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

partitionWidth = 2 # minutes of transcript analyzed at a time
tailForgiveness = 30 # if the last partition is <= this many seconds, it is included in the previous partition

def partition(transcript:list[dict[str, str|float]], totalDuration):
    if totalDuration < (partitionWidth * 60 + tailForgiveness):
        return [transcript]
    partitioned : list[list[dict[str, str|float]]]= []
    currPart = 0
    for group in transcript:
        while group["start"] >= (60*currPart*partitionWidth) and not ((60*currPart*partitionWidth + tailForgiveness) > totalDuration):
            partitioned.append([])
            currPart += 1
        partitioned[currPart - 1].append(group)
    return partitioned

def formatPartitions(partitioned: list[list[dict[str, str|float]]], formatter: TextFormatter):
    return list(map(formatter.format_transcript, partitioned))

def shortsAnalysis(formatted):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Analyze a YouTube video for hate speech, disinformation or harmful ideas. If present, provide reasons why they are wrong or harmful. Otherwise, provide a brief summary indicating the absence of any negative messages. Total response length should be 4 sentences or less."},
            {"role": "user", "content": f'Transcript: {formatted}'}
        ],
        temperature = 0.8,
        max_tokens = 120
    )
    return response['choices'][0]['message']['content']


# from Django
@require_http_methods(["GET"])
def getPartitionAnalysis(request, id):
    isShort = (request.GET.get('short', "false") == "true")
    isDev = (request.GET.get('isDev', "false") == "true")
    partitionStr = request.GET.get('partition', '0')

    try:
        partition_idx = int(partitionStr)
    except ValueError:
        return JsonResponse({'error': 'Partition parameter is not an integer'}, status=400)

    try:
        transcript = YouTubeTranscriptApi.get_transcript(id)
        formatter = TextFormatter()
        duration = transcript[-1]["start"] + transcript[-1]["duration"]
        if isShort and duration <= 60:
            return JsonResponse({'error': 'shorts should not use this GET endpoint'}, status=400)
        else:
            formattedList = formatPartitions(partition(transcript, duration), formatter)
            if not isDev:
                analysis = mapAnalysisFunc(partition_idx, formattedList)
            else:
                analysis = formattedList[partition_idx]
            score = localSentiment(analysis)

    except Exception as e:
        print("ERROR:", e)
        analysis = str(e)
        score = None

    return JsonResponse({'analysis': analysis, 'score': score}, status=200)
