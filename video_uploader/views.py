from django.shortcuts import render
from django.db import IntegrityError
from .forms import VideoUploadForm
from .models import UserProfile
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
def is_valid_data(value, expected_type):
    if value is None or value == "":
        return False
    try:
        expected_type(value)
    except ValueError:
        return False
    return True

@csrf_exempt
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



@csrf_exempt
def save_profile_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        hr = data.get('result', {}).get('hr')
        hrv = data.get('result', {}).get('hrv')
        stress = data.get('result', {}).get('stress')

        if None in [hr, hrv, stress]:
            return JsonResponse({'status': 'error', 'message': '누락된 데이터가 있습니다.'})

        try:
            UserProfile.objects.create(
                user=request.user,
                heart_rate=str(hr),
                respiration_rate=str(hrv),
                stress_score=str(stress),
            )
        except IntegrityError as e:
            print(f"데이터베이스 오류: {e}")
            return JsonResponse({'status': 'error', 'message': '데이터베이스 오류가 발생했습니다.'})
        except Exception as e:
            print(f"예외 발생: {e}")
            return JsonResponse({'status': 'error', 'message': '알 수 없는 오류가 발생했습니다.'})

        return JsonResponse({'status': 'success', 'message': 'UserProfile이 성공적으로 생성되었습니다.'})

    else:
        return JsonResponse({'status': 'error', 'message': 'POST 요청만 허용됩니다.'})
