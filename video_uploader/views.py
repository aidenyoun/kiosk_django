from django.shortcuts import render
from django.http import JsonResponse
from .forms import VideoUploadForm
import requests

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = request.FILES['video']
            response = requests.post('http://211.185.64.159:9000', files={'video': video})
            if response.status_code == 200:
                data = response.json()
                return JsonResponse({'status': 'success', 'data': data})
            else:
                error_messages = {
                    -200: "심박이 제대로 계산이 안 되어 '0'으로 출력됨",
                    -201: "얼굴이 안 잡혀 계산 불가능",
                    -202: "영상의 길이가 충분하지 않은 상태",
                    -203: "영상의 포맷이 길이가 달라서 계산이 불가능"
                }
                error_code = response.status_code
                error_message = error_messages.get(error_code, "알 수 없는 오류가 발생했습니다.")
                return JsonResponse({'status': 'error', 'error_code': error_code, 'message': error_message})
        else:
            return JsonResponse({'status': 'error', 'message': '유효하지 않은 폼입니다.'})
    else:
        form = VideoUploadForm()
        return render(request, 'video_uploader/upload.html', {'form': form})
