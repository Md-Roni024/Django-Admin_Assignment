from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Location
from django.template import loader

def hello(request):
    template = loader.get_template('hello.html')
    return HttpResponse(template.render())


@csrf_exempt
def location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            type_ = data.get('type')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            location = Location.objects.create(
                name=name,
                type=type_,
                latitude=latitude,
                longitude=longitude
            )
            location.save()

            response_data = {
                'name': name,
                'type': type_,
                'latitude': latitude,
                'longitude':longitude,
                'status': 'Location created successfully!'
            }
            return JsonResponse(response_data, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    if request.method == 'GET':
        locations = Location.objects.all()
        data = list(locations.values('id', 'name', 'type', 'latitude', 'longitude')) 
        return JsonResponse(data, safe=False, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def get_location_by_id(request, location_id):
    try:
        location = Location.objects.get(id=location_id)
        data = {
            'name': location.name,
            'type': location.type,
            'latitude': location.latitude,
            'longitude': location.longitude
        }
        return JsonResponse(data, status=200)
    except Location.DoesNotExist:
        return JsonResponse({'error': 'Location not found'}, status=404)


@csrf_exempt 
def update_location_by_id(request, location_id):
    try:
        location = Location.objects.get(id=location_id)
        data = json.loads(request.body)
        location.name = data.get('name', location.name)
        location.type = data.get('type', location.type)
        location.latitude = data.get('latitude', location.latitude)
        location.longitude = data.get('longitude', location.longitude)
        location.save()
        response_data = {
            'name': location.name,
            'type': location.type,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'status': 'Location updated successfully!'
        }
        return JsonResponse(response_data, status=200)
    except Location.DoesNotExist:
        return JsonResponse({'error': 'Location not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)


@csrf_exempt
def delete_location_by_id(request, location_id):
    try:
        location = Location.objects.get(id=location_id)
        location.delete()
        return JsonResponse({'status': 'Location deleted successfully!'}, status=204)
    except Location.DoesNotExist:
        return JsonResponse({'error': 'Location not found'}, status=404)