from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import redirect
from requests import get


def HomeView(_):
    return JsonResponse(
        {'Coder': 'TILON', 'Coder_URL': 't.me/TILON', 'repository': 'https://github.com/andijoniyuz/islom.uz'},
        json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)


def NamozRegionsView(_):
    resp = get("https://islom.uz/")
    soup = BeautifulSoup(resp.text, features="lxml")
    regions = soup.find('div', class_="custom-select")
    region = {}
    b = 0
    for i in regions.find('select').find_all('option'):
        b += 1
        region[b] = {'region_name': i.text.strip(), 'region_id': int(i['value'])}

    return JsonResponse(region,
                        json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)


def NamozView(_, region_id):
    resp = get(f"https://islom.uz/region/{region_id}")
    soup = BeautifulSoup(resp.text, features="lxml")
    bomdod = soup.find('div', id="tc1").text
    peshin = soup.find('div', id="tc3").text
    asr = soup.find('div', id="tc4").text
    shom = soup.find('div', id="tc5").text
    xufton = soup.find('div', id="tc6").text

    times = {"bomdod": bomdod, 'peshin': peshin, 'asr': asr, 'shom': shom, 'xufton': xufton}

    return JsonResponse('ok': True, 'resilts': times},
                        json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)


def SearchQuestView(request):
    search_text = request.GET.get('q')
    page = request.GET.get('page')
    page = 0 if page is None else page
    url = "https://savollar.islom.uz"
    resp = get(f"{url}/search?words={search_text}&page={page}")
    soup = BeautifulSoup(resp.text, features="lxml")
    word_search = soup.find('span', class_="word_search")
    navContent = soup.find("ul", {"class": "pagination flex-wrap"})
    try:
        counts = word_search.findNext('b').text
    except:
        counts = 0
    if int(counts) == 0:
        error_text = soup.find("form", id="search_form").find('h4').text.strip()
        return JsonResponse({'ok': False, 'error_text': error_text},
                            json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)
    try:
        count_pages = navContent.find_all("li", recursive=False)[-2].find('a').text.strip()
    except:
        count_pages = 1
    if (int(count_pages) < int(page) and int(counts) == 0) or (int(count_pages) == 0 and int(counts) == 0):
        error_text = "Saxifa topilmadi."
        return JsonResponse({'ok': False, 'error_text': error_text},
                            json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)
    results_content = soup.find_all('div', class_="question")
    result = {}
    i = 0
    for s in results_content:
        i += 1
        question_info = s.find('span', class_="time_question").text.strip().split("|")
        question_time = question_info[0].strip()
        question_section = question_info[2].strip()
        quest_id = s.findNext('b').findNext('a', href=True)['href'].replace("/s/", "")
        result[i] = {'title': s.findNext('b').text,
                     'question_time': question_time,
                     'question_section': question_section,
                     'short_answer': s.find('div', class_="text_question").text.strip().replace("  давоми...", "..."),
                     "quest_id": int(quest_id)
                     }

    resultes = {'ok': True, 'search_word': word_search.text, 'counts': int(counts), 'page_count': int(count_pages),
                "results": result}
    return JsonResponse(resultes,
                        json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)


def QuestView(_, quest_id):
    url = "https://savollar.islom.uz"
    resp = get(f"{url}/s/{quest_id}")
    soup = BeautifulSoup(resp.text, features="lxml")
    question_in = soup.find('div', class_="in_question")
    title = question_in.find("h1").text
    question_info = question_in.find('div', class_="info_quesiton").text.strip().split("|")
    question_time = question_info[0].strip()
    question_viws = question_info[2].strip()
    question_full_text = question_in.find("div", class_="text_in_question").text.strip()
    author = question_in.find("div", class_="header_answer_inquestion").text.strip().replace(":", "")
    answer_text = question_in.find("div", class_="answer_in_question").text.strip()

    return JsonResponse(
        {"title": title, "quest_time": question_time, "quest_views": int(question_viws), 'author': author,
         'question_text': question_full_text,
         'answer_text': answer_text,

         },
        json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)


def TerminView(_, atama_id):
    url = "https://savollar.islom.uz/atama"

    resp = get(f"{url}/{atama_id}")
    soup = BeautifulSoup(resp.text, features="lxml")
    termin_info = soup.find('div', class_='text_in_question').text.strip()
    termin_name = soup.find('h1').text.strip()
    return JsonResponse(
        {'termin_name': termin_name, 'termin_info': termin_info},
        json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)


def SearchTerminView(request):
    term = request.GET.get('term')
    resp = get(f"https://savollar.islom.uz/atamasearch?atama={term}")
    soup = BeautifulSoup(resp.text, features="lxml")
    try:
        termin_info = soup.find('tbody')
    except:

        error_text = soup.find('div', class_='alert alert-danger').text.strip()
        return JsonResponse({'ok': False, 'error_text': error_text},
                            json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)
    terms = {}
    b = 0
    for i in termin_info.find_all('tr', 'row'):
        b += 1
        term_id = i.find('th', class_='col-lg-1').text.strip()
        term_name = i.find('th', class_='col-lg-3').text.strip()
        term_text = i.find('th', 'col-lg-8').text.strip()
        terms[b] = {'term_id': term_id, 'term_name': term_name, 'term_text': term_text}
    return JsonResponse({'ok': True, 'results': terms},
                        json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)


def page_not_found(request, *args, **kwargs):
    """Page not found Error 404"""
    return redirect('Home')


def handler500(request, *args, **argv):
    return redirect('Home')
