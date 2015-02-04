from django.db import models

class Hash(models.Model):
	read_key = models.CharField(max_length = 33, blank = False)
	write_key = models.CharField(max_length = 34, null = True, blank = True)
	date_added = models.DateTimeField(auto_now_add = True, editable = False)
	date_updated = models.DateTimeField(auto_now_add = True, auto_now = True, editable = False)
	thankyous = models.IntegerField(null = True, blank = True, editable = False)
	looks = models.IntegerField(null = True, blank = True, editable = False)
	deleted = models.BooleanField(default = False)
	date_deleted = models.DateTimeField(null = True, editable = True)
	#comments

	def __unicode__(self):
		return self.read_key

class Movie(models.Model):
	hashes = models.ManyToManyField( Hash, null = True, blank = True, verbose_name = "all hashes for a given Movie")
	name = models.CharField(max_length = 255)
	tvdbid = models.IntegerField()
	banner_path = models.CharField(max_length = 255)
	banner = models.ImageField(upload_to = 'movie_banners')
	looks = models.IntegerField(null = True, blank = True, editable = False)
	overview = models.TextField(null = True, blank = True)
	runtime = models.CharField(null = True, blank = True, max_length = 4)
	tagline = models.TextField(null = True, blank = True)
	genre = models.CharField(null = True, blank = True, max_length = 64)
	info_url = models.CharField(null = True, blank = True, max_length = 255)
	
	def __unicode__(self):
		return self.name

class Show(models.Model):
	name = models.CharField(max_length = 255)
	tvdbid = models.IntegerField(unique = True)
	banner = models.ImageField(upload_to = 'TV_banners')
	banner_path = models.CharField(max_length = 255, null = True, blank = True)
	poster_path = models.CharField(max_length = 255, null = True, blank = True)
	overview = models.TextField(null = True, blank = True)
	status = models.CharField(max_length = 16, null = True, blank = True)
	Airs_DayOfWeek = models.CharField(max_length = 16, null = True, blank = True)
	Airs_Time = models.CharField(max_length = 16, null = True, blank = True)
	click = models.IntegerField(null = True, blank = True, editable = False)
	all_season_hashes = models.ManyToManyField( Hash, null = True, blank = True, verbose_name = "Hashes containing All Seasons")
	looks = models.IntegerField(null = True, blank = True, editable = False)
	#comments
	def __unicode__(self):
		return self.name

class Season(models.Model):
	show = models.ForeignKey(Show, verbose_name = "Season of")
	hashes = models.ManyToManyField( Hash, null = True, blank = True, verbose_name = "all hashes for a given season")
	number = models.IntegerField()
	looks = models.IntegerField(null = True, blank = True, editable = False)

	def __unicode__(self):
		return u'%s %d' % (self.show, self.number)
# Create your models here.
