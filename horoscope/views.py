from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

zodiac_dict = {
    'aries': 'Овен - первый знак зодиака, планета Марс <u>(с 21 марта по 20 апреля)</u>.',
    'taurus': 'Телец - второй знак зодиака, планета Венера <u>(с 21 апреля по 21 мая)</u>.',
    'gemini': 'Близнецы - третий знак зодиака, планета Меркурий <u>(с 22 мая по 21 июня)</u>.',
    'cancer': 'Рак - четвёртый знак зодиака, Луна <u>(с 22 июня по 22 июля)</u>.',
    'leo': ' Лев - пятый знак зодиака, солнце <u>(с 23 июля по 21 августа)</u>.',
    'virgo': 'Дева - шестой знак зодиака, планета Меркурий <u>(с 22 августа по 23 сентября)</u>.',
    'libra': 'Весы - седьмой знак зодиака, планета Венера <u>(с 24 сентября по 23 октября)</u>.',
    'scorpio': 'Скорпион - восьмой знак зодиака, планета Марс <u>(с 24 октября по 22 ноября)</u>.',
    'sagittarius': 'Стрелец - девятый знак зодиака, планета Юпитер <u>(с 23 ноября по 22 декабря)</u>.',
    'capricorn': 'Козерог - десятый знак зодиака, планета Сатурн <u>(с 23 декабря по 20 января)</u>.',
    'aquarius': 'Водолей - одиннадцатый знак зодиака, планеты Уран и Сатурн <u>(с 21 января по 19 февраля)</u>.',
    'pisces': 'Рыбы - двенадцатый знак зодиака, планеты Юпитер <u>(с 20 февраля по 20 марта)</u>.',
}

types = {
    'fire': ['aries', 'leo', 'sagittarius'],
    'earth': ['taurus', 'virgo', 'capricorn'],
    'air': ['gemini', 'libra', 'aquarius'],
    'water': ['cancer', 'scorpio', 'pisces']
}

duration_zodiacs = {
    (1, 19): "capricorn",
    (20, 49): "aquarius",
    (50, 79): "pisces",
    (80, 109): "aries",
    (110, 139): "taurus",
    (140, 169): "gemini",
    (170, 199): "cancer",
    (200, 229): "leo",
    (230, 259): "virgo",
    (260, 289): "libra",
    (290, 319): "scorpio",
    (320, 349): "sagittarius",
    (350, 365): "capricorn"
}


def get_yyyy_converters(request, sign_zodiac):
    print(f'тип - {type(sign_zodiac)}')
    return HttpResponse(f'вы передали число из 4-х цифр - {sign_zodiac}')


def get_my_float_converters(request, sign_zodiac):
    print(f'тип - {type(sign_zodiac)}')
    return HttpResponse(f'вы передали вещественное число - {sign_zodiac}')


def get_my_date_converters(request, sign_zodiac):
    print(f'тип - {type(sign_zodiac)}')
    return HttpResponse(f'вы передали дату - {sign_zodiac}')


def index(request):
    zodiacs = list(zodiac_dict)
    # f"<li> <a href='{redirect_path}'>{sign.title()} </a> </li>"
    context = {
        'zodiacs': zodiacs
    }

    return render(request, 'horoscope/index.html', context=context)


def choose_element(request):
    elements = list(types)
    li_elements = ''
    for element in elements:
        redirect_path = reverse("horoscope_group", args=[element])
        li_elements += f"<li> <a href='{redirect_path}'>{element.title()} </a> </li>"
    response = f"""
    <ul>
        {li_elements}
    </ul>
    """
    return HttpResponse(response)


def get_info_about_element(request, type_element):
    zodiacs_of_element = types[type_element]
    li_element = ''
    for sign in zodiacs_of_element:
        redirect_path = reverse("horoscope_name", args=[sign])
        li_element += f"<li> <a href='{redirect_path}'>{sign.title()} </a> </li>"
    response = f"""
    <ul> 
        {li_element}
    </ul>
    """
    return HttpResponse(response)


def get_info_about_sign_zodiac(request, sign_zodiac: str):
    description = zodiac_dict.get(sign_zodiac)
    data = {
        "description_zodiac": description,
        "sign": sign_zodiac,
        "zodiacs": zodiac_dict,

    }
    return render(request, 'horoscope/info_zodiac.html', context=data)


def get_info_about_sign_zodiac_by_number(request, sign_zodiac: int):
    zodiacs = list(zodiac_dict)
    if sign_zodiac > len(zodiacs):
        return HttpResponseNotFound(f"неизвестный номер зодиака - {sign_zodiac}")
    name = zodiacs[sign_zodiac - 1]
    redirect_url = reverse("horoscope_name", args=[name])
    return HttpResponseRedirect(redirect_url)


def get_info_by_day(request, month, day):
    day_of_years = (month - 1) * 30 + day
    for key, value in duration_zodiacs.items():
        if day_of_years >= key[0] and day_of_years <= key[1]:
            redirect_url = reverse("horoscope_name", args=[value])
            return HttpResponseRedirect(redirect_url)

    return HttpResponseNotFound(f"<h2> месяц - {month}, день - {day} </h2>")
