from django.db import models

class Mount(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    expansion = models.CharField(max_length=20)
    notes_1 = models.CharField(max_length=50, null=True)
    notes_2 = models.CharField(max_length=500, null=True)
    requirements = models.CharField(max_length=50, null=True)
    source = models.CharField(max_length=50, null=True)
    url_info = models.CharField(max_length=100, null=True)
    url_wowhead = models.CharField(max_length=100, null=True)
    image_mini = models.CharField(max_length=100, null=True)
    image = models.CharField(max_length=100, null=True)
    url_img = models.CharField(max_length=100, null=True)
    url_img_min = models.CharField(max_length=100, null=True)

    @classmethod
    def create(cls, **kwargs):
        mount = cls.objects.create(
            id = kwargs['Id'],
            name = kwargs['Name'],
            expansion = kwargs['Expansion'],
            notes_1 = kwargs['Notes_1'],
            notes_2 = kwargs['Notes_2'],
            requirements = kwargs['Requirements'],
            source = kwargs['Source'],
            url_info = kwargs['UrlInfo'],
            url_wowhead = kwargs['UrlWowhead'],
            image_mini = kwargs['ImageMini'],
            image = kwargs['Image'],
            url_img = kwargs['Id'] + "-" + kwargs['Name'].replace('/', ' ') + "/" + kwargs['Image'],
            url_img_min = kwargs['Id'] + "-" + kwargs['Name'].replace('/', ' ') + "/" + kwargs['ImageMini']
        )