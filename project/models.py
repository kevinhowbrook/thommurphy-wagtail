from django.db import models

# Create your models here.

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel

from modelcluster.fields import ParentalKey
from wagtail.images.edit_handlers import ImageChooserPanel


from wagtail.core.models import Orderable, Page
from django.shortcuts import render
from django.views.decorators.vary import vary_on_headers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# The abstract model for Project links, complete with panels
class ProjectImage(models.Model):
	title = models.CharField(max_length=255)
	image = models.ForeignKey(
		'wagtailimages.Image',
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+'
	)

	panels = [
		FieldPanel('title'),
		ImageChooserPanel('image'),
	]

	class Meta:
		abstract = True


# The real model which combines the abstract model, an
# Orderable helper class, and what amounts to a ForeignKey link
# to the model we want to add related links to (BookPage)
class ProjectPageProjectImages(Orderable, ProjectImage):
	page = ParentalKey('project.ProjectPage', related_name='project_images')


# The abstract model for Project links, complete with panels
class ProjectSlideshow(models.Model):
	title = models.CharField(max_length=255)
	image = models.ForeignKey(
		'wagtailimages.Image',
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+'
	)
	slide_description = models.TextField(blank=True)

	panels = [
		FieldPanel('title'),
		FieldPanel('slide_description'),
		ImageChooserPanel('image'),
	]

	class Meta:
		abstract = True


# The real model which combines the abstract model, an
# Orderable helper class, and what amounts to a ForeignKey link
# to the model we want to add related links to (BookPage)
class ProjectPageProjectSlideshowImages(Orderable, ProjectSlideshow):
	page = ParentalKey('project.ProjectPage', related_name='project_slideshow')


class ProjectPage(Page):
	date = models.DateField("Post date")
	teaser_intro = models.TextField(blank=True, help_text='This text will appear below teaser', max_length='140')
	body = RichTextField(blank=True)
	listing_image = models.ForeignKey(
		'wagtailimages.Image',
		null=True,
		blank=True,
		on_delete=models.SET_NULL
	)

	content_panels = Page.content_panels + [
		FieldPanel('date'),
		FieldPanel('teaser_intro'),
		FieldPanel('body', classname="full"),
		ImageChooserPanel('listing_image'),
		InlinePanel('project_images', label="Project Images"),
		InlinePanel('project_slideshow', label="Project Slideshow"),
	]

	parent_page_types = ['project.ProjectIndexPage']
	subpage_types = []


class ProjectIndexPage(Page):
	intro = RichTextField(blank=True)

	content_panels = Page.content_panels + [
		FieldPanel('intro', classname="full")
	]

	@property
	def projects(self):
		# Get list of poject pages that are descendants of this page
		projects = ProjectPage.objects.filter(
			live=True,
			path__startswith=self.path
		)

		# Order by most recent date first
		projects = projects.order_by('-date')

		return projects

	@vary_on_headers('X-Requested-With')
	def serve(self, request):
		# Get projects
		projects = self.projects

		# Pagination
		page = request.GET.get('page')
		paginator = Paginator(projects, 12)  # Show 12 events per page
		try:
			projects = paginator.page(page)
		except PageNotAnInteger:
			projects = paginator.page(1)
		except EmptyPage:
			projects = paginator.page(paginator.num_pages)

		return render(request, self.template, {
			'self': self,
			'projects': projects,
		})


