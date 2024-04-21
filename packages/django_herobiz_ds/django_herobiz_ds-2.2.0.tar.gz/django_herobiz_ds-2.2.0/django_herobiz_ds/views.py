from django.shortcuts import render, get_object_or_404
from django_utilsds import utils
from .forms import AppointmentForm
from _data import herobizds
from .models import Portfolio
from hitcount.views import HitCountDetailView
from .models import Post, CATEGORY
from django.views import generic
from .forms import SearchForm

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)

num_pagination = 7


def make_page_bundle(page_range, n=5):
    # 전체 페이지를 n 개수의 묶음으로 만든다.
    # pagination에 사용
    l = [i for i in page_range]
    return [l[i:i + n] for i in range(0, len(l), n)]


def robots(request):
    from django.shortcuts import HttpResponse
    file_content = utils.make_robots()
    return HttpResponse(file_content, content_type="text/plain")


def home(request):
    c = herobizds.context

    logger.info(c)
    if request.method == 'GET':
        c.update({'form': AppointmentForm()})
        c['post_message'] = None
        return render(request, 'herobizds/index.html', c)
    elif request.method == "POST":
        c.update(make_post_context(request.POST, c['basic_info']['consult_email']))
        return render(request, 'herobizds/index.html', c)


def make_post_context(request_post, consult_mail):
    logger.info(request_post)
    context = {}
    # appointment 앱에서 post 요청을 처리함.
    logger.info(f'request.POST : {request_post}')
    form = AppointmentForm(request_post)

    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        logger.info(f'Pass validation test -  {name} {email} {subject} {message}')
        is_sendmail = utils.mail_to(title=f'{name} 고객 상담 문의',
                                    text=f'이름: {name}\n메일: {email}\n제목: {subject}\n메시지: {message}',
                                    mail_addr=consult_mail)
        if is_sendmail:
            context['post_message'] = '담당자에게 예약 신청이 전달되었습니다. 확인 후 바로 연락 드리겠습니다. 감사합니다.'
        else:
            context['post_message'] = '메일 전송에서 오류가 발생하였습니다. 카카오톡이나 전화로 문의주시면 감사하겠습니다. 죄송합니다.'
        return context
    else:
        logger.error('Fail form validation test')
        context['post_message'] = '입력 항목이 유효하지 않습니다. 다시 입력해 주십시요.'
        return context


def details(request, id: int):
    c = herobizds.context
    c.update(
        {
            "breadcrumb": {
                "title": c['portfolio']['title'],
            },
            "obj": get_object_or_404(Portfolio, pk=id),
        }
    )
    logger.debug(c)
    return render(request, "herobizds/portfolio-details.html", c)


def terms(request):
    c = herobizds.context
    c.update(
        {
            "breadcrumb": {
                "title": "Terms of Use",
            },
            "terms": {
                "company_name": c['basic_info']['company_name'],
                "sdate": c['basic_info']['sdate'],
            },
        }
    )
    return render(request, "herobizds/terms.html", c)


def privacy(request):
    c = herobizds.context
    c.update(
        {
            "breadcrumb": {
                "title": "Privacy Policy",
            },
            "privacy": {
                "company_name": c['basic_info']['company_name'],
                "assigned_company_name": "데미안소프트",
                "owner": c['basic_info']['owner'],
                "position": "담당자",
                "phone": c['basic_info']['phone'],
                "email": c['basic_info']['owner_email'],
                "sdate": c['basic_info']['sdate'],
            },
        }
    )
    return render(request, "herobizds/privacy.html", c)


class PostDetailView(HitCountDetailView):
    model = Post
    template_name = 'herobizds/blog-details.html'
    context_object_name = 'object'
    slug_field = 'slug'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for i, name in CATEGORY:
            if self.get_object().category == i:
                category_name = name
                break

        context.update(herobizds.context)
        context.update(
            {
                'breadcrumb': {
                    'title': 'Blog Detail'
                },
                'category_name': category_name
            }
        )
        return context


class SearchResult(generic.ListView):
    template_name = 'herobizds/blog.html'
    paginate_by = num_pagination

    def get_queryset(self):
        form = SearchForm(self.request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
        else:
            q = ''
        return Post.objects.filter(content__contains='' if q is None else q).filter(status=1).order_by(
            '-updated_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pages_devided = make_page_bundle(context['paginator'].page_range)

        # 현재 페이지에 해당하는 묶음을 page_bundle로 전달한다.
        for page_bundle in pages_devided:
            if context['page_obj'].number in page_bundle:
                context['page_bundle'] = page_bundle

        context.update(herobizds.context)
        return context


class Blog(SearchResult):
    # 홈페이지에서 다이렉트 링크로 연결하기 위해서 필요하다.
    def get_queryset(self):
        # https://stackoverflow.com/questions/56067365/how-to-filter-posts-by-tags-using-django-taggit-in-django
        return Post.objects.filter(status=1).order_by('-updated_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "breadcrumb": {
                "title": "Blog",
            },
        })
        return context


class SearchTag(SearchResult):
    def get_queryset(self):
        # https://stackoverflow.com/questions/56067365/how-to-filter-posts-by-tags-using-django-taggit-in-django
        return Post.objects.filter(tags__name__in=[self.kwargs['tag']]).filter(status=1).order_by('-updated_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "breadcrumb": {
                "title": "Tag: " + self.kwargs['tag'],
            },
        })
        return context


class Category(SearchResult):
    def get_queryset(self):
        return Post.objects.filter(status=1).filter(category=self.kwargs['category_int']).order_by('-updated_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for i, name in CATEGORY:
            if self.kwargs['category_int'] == i:
                category_name = name
                break

        context.update({
            "breadcrumb": {
                "title": "Category: " + category_name,
            },
        })
        return context
