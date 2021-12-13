# Create your views here.
import datetime
import random

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.detail import View
from django.template import Context, Template

from .models import Answer

# Sessions keys
KEY_LEVEL = "KL"
KEY_TIMESTAMP = "TS"
KEY_RESULT = "RR"
KEY_WRONG_RESULT = "WR"

def set_level(request, level):
    request.session[KEY_LEVEL] = max(level, request.session.get(KEY_LEVEL, 0))

def check_level(request, level):
    return request.session.get(KEY_LEVEL, 0) >= level

class NoCsrfView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(NoCsrfView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        # controllare nella sessione l'avanzamento
        if not check_level(request, self.LEVEL):
            return self.previous_level()
        return self.post_riddle(request, *args, **kwargs)

    def get_extra(self, request):
        return None

    def get(self, request, *args, **kwargs):
        # controllare nella sessione l'avanzamento
        if self.LEVEL > 1 and not check_level(request, self.LEVEL):
            return self.previous_level()
        # azzerare nella sessione l'avanzamento
        set_level(request, self.LEVEL)
        return self.this_level(extra = self.get_extra(request))

    def next_level(self, request, answer):
        answer.set_right()
        next_level = self.LEVEL+1
        set_level(request, next_level)
        return HttpResponseRedirect(reverse('riddle%d' % next_level))

    def previous_level(self):
        return HttpResponseRedirect(reverse('riddle%d' % max(self.LEVEL - 1, 1)))

    def this_level(self, extra=None):
        return HttpResponse(render_to_response('riddle/level_%s.html' % self.NAME, extra))

class WinnerView(NoCsrfView):
    LEVEL = 4
    NAME = "winner"

    def post_riddle(self, request, *args, **kwargs):
        msg = "Uh?"
        value = request.POST.get('email', "")
        if value:
            try:
                # Save email
                obj = Answer.add(request, level=self.LEVEL)
                obj.set_right()
                return HttpResponse(render_to_response('riddle/done.html', {'email': value}))
            except ValueError:
                msg = "Error"
        return self.this_level({'answer': msg, 'default': value})

class RiddleBriesView(NoCsrfView):
    LEVEL = 2
    NAME = "bries"

    def post_riddle(self, request, *args, **kwargs):
        answer_obj = Answer.add(request, level=self.LEVEL)
        msg = "Uh?"
        value = request.POST.get('answer', "")
        if value:
            try:
                primes = 22627
                unoes = 450
                all_ = 109290
                answer = int(value)
                if answer == primes:
                    return self.next_level(request, answer_obj)
                elif answer == unoes + primes:
                    msg = "I don't think 1 is an empty brie"
                elif answer == all_ - primes:
                    msg = "Those aren't the empty ones"
                elif answer == all_:
                    msg = "I said empty bries, not all of them :)"
                elif answer == 0:
                    msg = "Zero?!? Ah, ah, ah!"
                elif answer == 1:
                    msg = "Only one? Nah!"
                elif answer == 2:
                    msg = "Two bries? Come on..."
                elif answer == 3:
                    msg = "Try again..."
                elif answer == 42:
                    msg = "Thanks for all the fish"
                elif answer < 10:
                    msg = "Come on..."
                elif answer > 10000000:
                    msg = "Wow! Not so many...."
                else:
                    msg = "Wrong"
            except ValueError:
                msg = "I think I need an integer..."
        return self.this_level({'answer': msg, 'default': value})

class RiddleCaptchaView(NoCsrfView):
    LEVEL = 3
    NAME = "captcha"

    def get_extra(self, request):
        operators = ("*", "-", "+")
        adder = random.randint(100, 1000)
        equation = " ".join(str(random.randint(100, 1000))
                if i % 2 == 0 else random.choice(operators) for i in range(9))
        extra = {
                "adder": adder,
                "math": equation,
            }
        request.session[KEY_TIMESTAMP] = datetime.datetime.now()
        request.session[KEY_WRONG_RESULT] = eval(equation)
        request.session[KEY_RESULT] = eval(" ".join(str(int(x) + adder)
            if i % 2 == 0 else x for i, x in enumerate(equation.split(" "))))
        return extra

    def post_riddle(self, request, *args, **kwargs):
        answer_obj = Answer.add(request, level=self.LEVEL)
        msg = "Uh?"
        value = request.POST.get('answer', "")
        if value:
            try:
                answer = int(value)
                if answer == request.session[KEY_WRONG_RESULT]:
                    msg = "Not bad... but you forgot the adder ;)"
                elif answer == 42:
                    msg = "No more HG2G easter egg!"
                elif answer == request.session[KEY_RESULT]:
                    elapsed = datetime.datetime.now() - request.session[KEY_TIMESTAMP]
                    if elapsed > datetime.timedelta(seconds=3):
                        msg = "Right!</br></br>But way too slooooowwww..."
                    else:
                        return self.next_level(request, answer_obj)
                else:
                    msg = "Wrong"
            except ValueError:
                msg = "I think I need an integer..."
        extra = self.get_extra(request)
        extra.update({'answer': msg, 'default': value})
        return self.this_level(extra)

class RiddleDatesView(NoCsrfView):
    LEVEL = 1
    NAME = "dates"
    date1 = datetime.datetime(1964, 9, 23, 12, 20, 23)
    date2 = datetime.datetime(1994, 6, 26, 8, 12, 15)
    adder404 = 23
    first_right = (date2 - date1).total_seconds() # 938980312
    more_template = Template("""{% load staticfiles %}<a href="{% static "files/dates.txt" %}">more</a>""")
    last_absolute_right = 37144557901
    last_right = 249995245161

    def get_extra(self, request):
        return {'date1': self.date1.strftime("%Y/%m/%d %H:%M:%S"),
                'date2': self.date2.strftime("%Y/%m/%d %H:%M:%S")}

    def post_riddle(self, request, *args, **kwargs):
        answer_obj = Answer.add(request, level=self.LEVEL)
        msg = "Uh?"
        value = request.POST.get('answer', "")
        more = self.more_template.render(Context())
        if value:
            try:
                answer = int(value)
                if answer == self.first_right:
                    msg = """Good!</br></br>Now you need <font color="red">{0}</font> dates""".format(more)
                elif answer == 0:
                    msg = "Wow... at light speed!"
                elif answer == 42:
                    msg = "Douglas Adams forever"
                elif answer == 71512:
                    msg = """Do you know <font color="red">total_seconds()</font>?"""
                elif answer == self.adder404:
                    msg = """Ok, you found something not found, but it's a long way to next level..."""
                elif answer == self.first_right + self.adder404:
                    msg = """Nice try... But I said you need <font color="red">{0}</font> dates ;)""".format(more)
                elif answer == self.last_absolute_right:
                    msg = """Uhm... I think you can't do 3 minus 5, it's much better 5 minus 3"""
                elif answer == self.last_right:
                    msg = ("""Almost right!</br></br>Now search something <font color="red">Not Found</font> ;)""" +
                                """<!-- Perhaps 404 ? -->""")
                elif answer == self.last_right + self.adder404:
                    return self.next_level(request, answer_obj)
                else:
                    msg = "Wrong"
            except ValueError:
                msg = "I think I need an integer..."
        extra = self.get_extra(request)
        extra.update({'answer': msg, 'default': value})
        return self.this_level(extra)

class HomeView(NoCsrfView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(render_to_response('riddle/home.html'));
