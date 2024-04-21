from django.shortcuts import render, get_object_or_404, redirect
from django_utilsds import utils
from .forms import AppointmentForm
from _data import bocords
from .models import Portfolio

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


def robots(request):
    from django.shortcuts import HttpResponse
    file_content = utils.make_robots()
    return HttpResponse(file_content, content_type="text/plain")


def home(request):
    c = bocords.context

    logger.info(c)
    if request.method == 'GET':
        c.update({'form': AppointmentForm()})
        c['post_message'] = None
        return render(request, 'bocords/index.html', c)
    elif request.method == "POST":
        c.update(make_post_context(request.POST, c['basic_info']['consult_email']))
        return render(request, 'bocords/index.html', c)


def make_post_context(request_post, consult_mail):
    logger.info(request_post)
    context = {}
    # appointment 앱에서 post 요청을 처리함.
    logger.info(f'request.POST : {request_post}')
    form = AppointmentForm(request_post)

    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        company = form.cleaned_data['company']
        message = form.cleaned_data['message']
        logger.info(f'Pass validation test -  {name} {email} {company} {message}')
        is_sendmail = utils.mail_to(title=f'{name} 고객 상담 문의',
                                    text=f'이름: {name}\n메일: {email}\n업체명: {company}\n메시지: {message}',
                                    mail_addr=consult_mail)
        if is_sendmail:
            context['post_message'] = '담당자에게 문의사항이 전달 되었습니다. 확인 후 바로 연락 드리겠습니다. 감사합니다.'
        else:
            context['post_message'] = '메일 전송에서 오류가 발생 하였습니다. 전화로 문의주시면 감사하겠습니다. 죄송합니다.'
        return context
    else:
        logger.error('Fail form validation test')
        context['post_message'] = '입력 항목이 유효하지 않습니다. 다시 입력해 주십시요.'
        return context


def details(request, id: int):
    url = get_object_or_404(Portfolio, pk=id).url
    return redirect(url)
