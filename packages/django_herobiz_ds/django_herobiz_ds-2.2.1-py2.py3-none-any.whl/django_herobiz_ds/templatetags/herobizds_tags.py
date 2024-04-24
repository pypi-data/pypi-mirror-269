from django.template import Library, loader
from ..models import Post
from ..models import Portfolio, Category
from taggit.models import Tag
from _data.herobizds import CATEGORY
from ..forms import SearchForm

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


register = Library()

# https://localcoder.org/django-inclusion-tag-with-configurable-template


@register.simple_tag(takes_context=True)
def hero(context):
    t = loader.get_template(f"herobizds/_hero-{context['hero_type']}.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def featured_services(context):
    t = loader.get_template("herobizds/_featured-services.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def about(context):
    t = loader.get_template("herobizds/_about.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def clients(context):
    t = loader.get_template("herobizds/_clients.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def cta(context):
    t = loader.get_template("herobizds/_cta.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def onfocus(context):
    t = loader.get_template("herobizds/_onfocus.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def features(context):
    t = loader.get_template("herobizds/_features.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def services(context):
    t = loader.get_template("herobizds/_services.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def testimonials(context):
    t = loader.get_template("herobizds/_testimonials.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def pricing(context):
    t = loader.get_template("herobizds/_pricing.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def faq(context):
    t = loader.get_template("herobizds/_faq.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def portfolio(context):
    t = loader.get_template("herobizds/_portfolio.html")
    context.update({
        'categories': Category.objects,
        'items': Portfolio.objects,
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def team(context):
    t = loader.get_template("herobizds/_team.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def recent_blog_posts(context):
    t = loader.get_template("herobizds/_recent-blog-posts.html")
    objects = Post.objects.filter(status=1).order_by('-updated_on')
    context.update({
        'top3': objects[:3],
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def contact(context):
    t = loader.get_template("herobizds/_contact.html")
    context.update({

    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def sidebar(context):
    t = loader.get_template(f"herobizds/_sidebar.html")
    tags = Tag.objects.all()
    category = []
    for category_int, name in CATEGORY:
        category.append([category_int, name, Post.objects.filter(status=1).filter(category=category_int).count()])
    context.update({
        'form': SearchForm(),
        'category': category,
        'all_tags': tags,
        'latest': Post.objects.filter(status=1).order_by('-updated_on')[:6],
    })
    logger.info(context)
    return t.render(context.flatten())
