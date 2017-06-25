from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from s13core import helpers as h
from s13core.settings.models import Setting

from .models import Article


class HttpTests(TestCase):
    c = Client()

    def setUp(self):
        # We need settings.
        if Setting.objects.count() < 1:
            setting = Setting()
            setting.is_active = True
            setting.save()
        # We want test articles.
        if Article.objects.count() < 1:
            Article(slug='homepage', title='Home Page',
                    is_homepage=True).save()
            Article(slug='section', title='Section Page').save()
            Article(slug='article', title='Article Page',
                    parent=Article.objects.get(slug='section')).save()

    def test_homepage(self):
        response = self.c.get(reverse('s13cms:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Home Page', str(response.content))

    def test_section(self):
        # There is no section with slug: no-section.
        response = self.c.get(reverse('s13cms:section', args=['no-section']))
        self.assertEqual(response.status_code, 404)
        # There is a section with slug: section; see setUp.
        response = self.c.get(reverse('s13cms:section', args=['section']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Section Page', str(response.content))

    def test_article(self):
        # Article with slug: article is not a section because it has a parent;
        # therefore, it cannot be accessed by its slug alone.
        response = self.c.get(reverse('s13cms:section', args=['article']))
        self.assertEqual(response.status_code, 404)
        # This is correct.
        response = self.c.get(
            reverse('s13cms:article', args=['section', 'article'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Article Page', str(response.content))


class ModelArticleTests(TestCase):

    def test_generate_date_made(self):
        t = h.get_now()
        Article(slug='1234567890').save()
        a = Article.objects.get(slug='1234567890')
        self.assertEqual(
            (t.year, t.month, t.day),
            (a.date_made.year, a.date_made.month, a.date_made.day)
        )

    def test_generate_slug_from_date(self):
        t = h.get_now()
        Article(title='This is the title of the article').save()
        a = Article.objects.get(title='This is the title of the article')
        self.assertEqual(a.slug[:9], t.strftime('%Y%m%d-'))

    def test_only_one_homepage(self):
        for a in range(2):
            Article(slug='article-{}'.format(a)).save()
        a = Article.objects.get(slug='article-0')
        a.is_homepage = True
        a.save()
        self.assertEqual(Article.objects.filter(is_homepage=True).count(), 1)
        b = Article.objects.get(slug='article-1')
        b.is_homepage = True
        b.save()
        self.assertEqual(Article.objects.filter(is_homepage=True)[0], b)
        self.assertFalse(Article.objects.get(slug=a.slug).is_homepage)

    def test_make_url(self):
        h = Article(slug='homepage', is_homepage=True)
        s = Article(slug='section')
        a = Article(slug='article', parent=s)
        self.assertEqual(h.make_url(), '/')
        self.assertEqual(s.make_url(), '/section/')
        self.assertEqual(a.make_url(), '/section/article/')

    def test_get_ancestry(self):
        parents = []
        for i in range(4):
            p = None if len(parents) < 1 else parents[-1]
            a = Article(slug='article-{}'.format(i), parent=p)
            parents.append(a)
        youngest = parents.pop()
        parents.reverse()
        self.assertEqual(parents, youngest.get_ancestry())

    def test_get_children(self):
        p = Article(slug='the-parent')
        p.save()
        for i in range(4):
            Article(
                slug='child-{}'.format(i),
                parent=p,
                is_public=False
            ).save()
        self.assertEqual(len(p.get_children()), 0)
        self.assertEqual(len(p.get_children(exclude_private=False)), 4)

    def test_get_siblings(self):
        p = Article(slug='the-parent')
        p.save()
        for i in range(4):
            Article(
                slug='child-{}'.format(i),
                parent=p,
                is_public=False
            ).save()
        a = Article.objects.get(slug='child-0')
        self.assertEqual(len(a.get_siblings()), 0)
        self.assertEqual(len(a.get_siblings(exclude_private=False)), 4)
