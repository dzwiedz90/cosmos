import os

from django.contrib.auth import authenticate, login, logout
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import InterstellarObject, SolarSystemObject, MoonObject, Favourites, Plan


@login_required
def index(request):
    if request.method == 'GET':
        i = InterstellarObject.objects.all()
        s = SolarSystemObject.objects.all()
        m = MoonObject.objects.all()
        data = i, s, m
        return TemplateResponse(request, 'interstellar_app' + os.sep + 'index.html', {'data': data, 'is_post': False})
    elif request.method == 'POST':
        data = request.POST
        chosen_object = None
        all_objects = False
        object_type = ''
        if data['filter_by_type'] == 'deep_space':
            chosen_object = InterstellarObject.objects.all()
            object_type = 'interstellar'
        elif data['filter_by_type'] == 'solar':
            chosen_object = SolarSystemObject.objects.all()
            object_type = 'solar'
        elif data['filter_by_type'] == 'moon':
            chosen_object = MoonObject.objects.all()
            object_type = 'moon'
        elif data['filter_by_type'] == 'none':
            i = InterstellarObject.objects.all()
            s = SolarSystemObject.objects.all()
            m = MoonObject.objects.all()
            all_objects = True
            chosen_object = []
            for o in i, s, m:
                for x in o:
                    chosen_object.append(x)

        chosen_object = list(chosen_object)

        if data['sort_by'] == 'magnitude_asc':
            chosen_object.sort(key=lambda x: x.apparent_magnitude, reverse=True)
        elif data['sort_by'] == 'magnitude_desc':
            chosen_object.sort(key=lambda x: x.apparent_magnitude)
        return TemplateResponse(request, 'interstellar_app' + os.sep + 'index.html',
                                {'data': chosen_object, 'is_post': True, 'type': object_type,
                                 'all_objects': all_objects})


@login_required
def units(request):
    return TemplateResponse(request, 'interstellar_app' + os.sep + 'unit_details.html')


@login_required
def solar_system_tab(request):
    if request.method == 'GET':
        s = SolarSystemObject.objects.all()
        return TemplateResponse(request, 'interstellar_app' + os.sep + 'solar.html', {'data': s, 'is_post': False})
    elif request.method == 'POST':
        data = request.POST

        if data['sort_by'] == 'magnitude_asc':
            s = SolarSystemObject.objects.all().order_by('apparent_magnitude').reverse()
        elif data['sort_by'] == 'magnitude_desc':
            s = SolarSystemObject.objects.all().order_by('apparent_magnitude')
        elif data['sort_by'] == 'distance_desc':
            s = SolarSystemObject.objects.all().order_by('aphelion')
        elif data['sort_by'] == 'distance_asc':
            s = SolarSystemObject.objects.all().order_by('aphelion').reverse()
        elif data['sort_by'] == 'size_desc':
            s = SolarSystemObject.objects.all().order_by('radius').reverse()
        elif data['sort_by'] == 'size_asc':
            s = SolarSystemObject.objects.all().order_by('radius')
        elif data['sort_by'] == 'moons_desc':
            s = SolarSystemObject.objects.all().order_by('natural_satellites').reverse()
        elif data['sort_by'] == 'moons_asc':
            s = SolarSystemObject.objects.all().order_by('natural_satellites')

        return TemplateResponse(request, 'interstellar_app' + os.sep + 'solar.html', {'data': s, 'is_post': True})


@login_required
def solar_system_detail(request, id):
    solar_object = SolarSystemObject.objects.get(id=id)
    files = os.listdir(
        os.getcwd() + os.sep + 'interstellar_app' + os.sep + 'static' + os.sep + 'interstellar_app' + os.sep + 'solar' +
        os.sep + str(id))
    path = 'interstellar_app' + os.sep + 'solar' + os.sep + id + os.sep
    return TemplateResponse(request, 'interstellar_app' + os.sep + 'solar_detail.html',
                            {'data': solar_object, 'id': id, 'path': path, 'files': files})


@login_required
def moons_tab(request):
    planet_list = SolarSystemObject.objects.values_list('name').exclude(natural_satellites=0)
    planet_list = list(planet_list)
    planet_list = [item[0] for item in planet_list]
    if request.method == 'GET':
        m = MoonObject.objects.all()
        return TemplateResponse(request, 'interstellar_app' + os.sep + 'moon.html',
                                {'data': m, 'is_post': False, 'planet_list': planet_list})
    elif request.method == 'POST':
        data = request.POST
        planet = SolarSystemObject.objects.get(name=data['filter_by_type'])
        m = MoonObject.objects.all().filter(satellite_of=planet.id)
        chosen_object = list(m)

        if data['sort_by'] == 'magnitude_asc':
            chosen_object.sort(key=lambda x: x.apparent_magnitude, reverse=True)
        elif data['sort_by'] == 'magnitude_desc':
            chosen_object.sort(key=lambda x: x.apparent_magnitude)
        elif data['sort_by'] == 'size_desc':
            chosen_object.sort(key=lambda x: x.diameter, reverse=True)
        elif data['sort_by'] == 'size_asc':
            chosen_object.sort(key=lambda x: x.diameter)

        return TemplateResponse(request, 'interstellar_app' + os.sep + 'moon.html',
                                {'data': chosen_object, 'is_post': True, 'planet_list': planet_list})


@login_required
def moons_detail(request, id):
    moon_object = MoonObject.objects.get(id=id)
    files = os.listdir(
        os.getcwd() + os.sep + 'interstellar_app' + os.sep + 'static' + os.sep + 'interstellar_app' + os.sep + 'moon' +
        os.sep + str(id))
    path = 'interstellar_app' + os.sep + 'moon' + os.sep + id + os.sep
    return TemplateResponse(request, 'interstellar_app' + os.sep + 'moon_detail.html',
                            {'data': moon_object, 'id': id, 'path': path, 'files': files})


@login_required
def interstellar_tab(request):
    if request.method == 'GET':
        i = InterstellarObject.objects.all()
        return TemplateResponse(request, 'interstellar_app' + os.sep + 'interstellar.html',
                                {'data': i, 'is_post': False})
    elif request.method == 'POST':
        data = request.POST
        chosen_object = None

        if data['filter_by_type'] == 'galaktyka':
            chosen_object = InterstellarObject.objects.all().filter(type__contains='galaktyka')
        elif data['filter_by_type'] == 'mgławica':
            chosen_object = InterstellarObject.objects.all().filter(type__contains='mgławica')
        elif data['filter_by_type'] == 'gromada':
            chosen_object = InterstellarObject.objects.all().filter(type__contains='gromada')
        elif data['filter_by_type'] == 'gwiazda':
            chosen_object = InterstellarObject.objects.all().filter(type__contains='gwiazda')
        elif data['filter_by_type'] == 'messier':
            chosen_object = InterstellarObject.objects.all().exclude(messier_catalogue=None)
        elif data['filter_by_type'] == 'none':
            chosen_object = InterstellarObject.objects.all()

        chosen_object = list(chosen_object)

        if data['sort_by'] == 'magnitude_asc':
            chosen_object.sort(key=lambda x: x.apparent_magnitude, reverse=True)
        elif data['sort_by'] == 'magnitude_desc':
            chosen_object.sort(key=lambda x: x.apparent_magnitude)
        elif data['sort_by'] == 'size_desc':
            chosen_object.sort(key=lambda x: x.diameter, reverse=True)
        elif data['sort_by'] == 'size_asc':
            chosen_object.sort(key=lambda x: x.diameter)

        return TemplateResponse(request, 'interstellar_app' + os.sep + 'interstellar.html',
                                {'data': chosen_object, 'is_post': True})


@login_required
def interstellar_detail(request, id):
    interstellar_object = InterstellarObject.objects.get(id=id)
    try:
        files = os.listdir(
            os.getcwd() + os.sep + 'interstellar_app' + os.sep + 'static' + os.sep + 'interstellar_app' + os.sep + 'interstellar' +
            os.sep + str(id))
    except FileNotFoundError:
        files = None
    path = 'interstellar_app' + os.sep + 'interstellar' + os.sep + id + os.sep
    return TemplateResponse(request, 'interstellar_app' + os.sep + 'interstellar_detail.html',
                            {'data': interstellar_object, 'id': id, 'path': path, 'files': files})


@login_required
def copyright(request):
    return TemplateResponse(request, 'interstellar_app' + os.sep + 'copyright.html')


@login_required
def favourites(request):
    data = Favourites.objects.all().filter(user=request.user)
    return TemplateResponse(request, 'interstellar_app' + os.sep + 'favourites.html', {'data': data})


@login_required
def plan(request):
    data = Plan.objects.all().filter(user=request.user)
    return TemplateResponse(request, 'interstellar_app' + os.sep + 'plan.html', {'data': data})


@login_required
def delete_fav_or_plan(request):
    if 'favourite' in request.POST:
        fav = Favourites.objects.get(id=int(request.POST['favourite']))
        fav.delete()

        data = Favourites.objects.all().filter(user=request.user)
        return TemplateResponse(request, 'interstellar_app' + os.sep + 'favourites.html', {'data': data})
    elif 'plan' in request.POST:
        plan = Plan.objects.get(id=int(request.POST['plan']))
        plan.delete()

        data = Plan.objects.all().filter(user=request.user)
        return TemplateResponse(request, 'interstellar_app' + os.sep + 'plan.html', {'data': data})


@login_required
def parse_fav_and_plan(request):
    if 'favourite' in request.POST:
        if request.POST['type'] == 'interstellar':
            try:
                if Favourites.objects.get(interstellar=int(request.POST['favourite'])):
                    return TemplateResponse(request, 'interstellar_app' + os.sep + 'added.html', {'data': 'exists'})
            except Favourites.DoesNotExist:
                pass
            user = User.objects.get(username=request.user)
            object_to_add = InterstellarObject.objects.get(id=int(request.POST['favourite']))
            favourite = Favourites(user=user, interstellar=object_to_add)
            favourite.save()
        elif request.POST['type'] == 'solar':
            try:
                if Favourites.objects.get(solar=int(request.POST['favourite'])):
                    return TemplateResponse(request, 'interstellar_app' + os.sep + 'added.html', {'data': 'exists'})
            except Favourites.DoesNotExist:
                pass
            user = User.objects.get(username=request.user)
            object_to_add = SolarSystemObject.objects.get(id=int(request.POST['favourite']))
            favourite = Favourites(user=user, solar=object_to_add)
            favourite.save()
        elif request.POST['type'] == 'moon':
            try:
                if Favourites.objects.get(moon=int(request.POST['favourite'])):
                    return TemplateResponse(request, 'interstellar_app' + os.sep + 'added.html', {'data': 'exists'})
            except Favourites.DoesNotExist:
                pass
            user = User.objects.get(username=request.user)
            object_to_add = MoonObject.objects.get(id=int(request.POST['favourite']))
            favourite = Favourites(user=user, moon=object_to_add)
            favourite.save()
    if 'plan' in request.POST:
        if request.POST['type'] == 'interstellar':
            try:
                if Plan.objects.get(interstellar=int(request.POST['plan'])):
                    return TemplateResponse(request, 'interstellar_app' + os.sep + 'added.html', {'data': 'exists'})
            except Plan.DoesNotExist:
                pass
            user = User.objects.get(username=request.user)
            object_to_add = InterstellarObject.objects.get(id=int(request.POST['plan']))
            plan = Plan(user=user, interstellar=object_to_add)
            plan.save()
        elif request.POST['type'] == 'solar':
            try:
                if Plan.objects.get(solar=int(request.POST['plan'])):
                    return TemplateResponse(request, 'interstellar_app' + os.sep + 'added.html', {'data': 'exists'})
            except Plan.DoesNotExist:
                pass
            user = User.objects.get(username=request.user)
            object_to_add = SolarSystemObject.objects.get(id=int(request.POST['plan']))
            plan = Plan(user=user, solar=object_to_add)
            plan.save()
        elif request.POST['type'] == 'moon':
            try:
                if Plan.objects.get(moon=int(request.POST['plan'])):
                    return TemplateResponse(request, 'interstellar_app' + os.sep + 'added.html', {'data': 'exists'})
            except Plan.DoesNotExist:
                pass
            user = User.objects.get(username=request.user)
            object_to_add = MoonObject.objects.get(id=int(request.POST['plan']))
            plan = Plan(user=user, moon=object_to_add)
            plan.save()

    return TemplateResponse(request, 'interstellar_app' + os.sep + 'added.html', {'data': 'added'})


def log_in(request):
    if request.method == 'GET':
        return TemplateResponse(request, 'interstellar_app' + os.sep + 'login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return TemplateResponse(request, 'interstellar_app' + os.sep + 'index.html')
        else:
            return HttpResponse('Wrong credentials')


def log_out(request):
    logout(request)
    return TemplateResponse(request, 'interstellar_app' + os.sep + 'login.html')
