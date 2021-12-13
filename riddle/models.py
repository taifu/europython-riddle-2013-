from django.db import models

class Answer(models.Model):
    timestamp = models.DateTimeField(auto_now_add = True)
    is_right = models.BooleanField(default=False)
    level = models.IntegerField(null=True, blank=True)
    answer = models.CharField(max_length=32, null=True, blank=True)
    attempts = models.IntegerField(default=0)
    ip = models.IPAddressField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"%s" % (self.ip or "<N.A.>")

    class Meta:
        ordering = ['-timestamp']

    def set_right(self):
        self.is_right = True
        self.save()

    @staticmethod
    def add(request, level, notes=""):
        obj = Answer()
        obj.level = level
        obj.notes = "notes"
        obj.email = request.POST.get('email', "")
        obj.answer = request.POST.get('answer', "")[:32]
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip_adds = request.META['HTTP_X_FORWARDED_FOR'].split(",")
            obj.ip = ip_adds[0]
        else:
            obj.ip = request.META.get('REMOTE_ADDR', "")
        obj.attempts = Answer.objects.filter(ip=obj.ip).count() + 1
        obj.save()
        return obj
