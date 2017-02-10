from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required

import json
from dateutil import parser
from collections import Counter

from .forms import TwitterUserForm

from users.models import Profile

from django.contrib.auth.models import User

days = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]


def parse_twitter_time_string(s):
    """takes twitter string and returns datetime in UTC.
    Also returns time as minutes from 0000, day as int (Monday=0)
    """
    dt = parser.parse(s)
    day = dt.weekday()
    time = dt.hour * 60 + dt.minute
    return dt, time, day


# Create your views here.
@login_required
def get_best_posting_time(request):
    # User.objects.all().delete()
    # Profile.objects.all().delete()
    # print(profile)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        user = request.user
        # for profile in Profile.objects.all():
        #     print(profile.user)
        profile = Profile.objects.get(user=user)
        is_new_user = profile.created_now
        print(is_new_user)
        profile.created_now = False
        profile.save()
        # create a form instance and populate it with data from the request:
        form = TwitterUserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = form.cleaned_data
            followers = data['twitter_followers']

            day_list = []
            minutes_from_noon_list = []

            for entry in followers:
                if entry.status is not None:
                    last_posted_datetime, last_posted_time, last_posted_day = parse_twitter_time_string(entry.status.created_at)
                    day_list.append(last_posted_day)
                    minutes_from_noon_list.append(last_posted_time)
                else:
                    # print('no status')
                    continue

            # if no latest tweets, return error
            if len(day_list) < 1:
                response = 'Sorry, not enough followers to predict best times'
            else:
                # find most active time by averaging all times
                best_time = sum(minutes_from_noon_list) / len(minutes_from_noon_list)
                best_time_hours = int(best_time / 60)
                best_time_minutes = int(best_time - best_time_hours * 60)
                # find best day by checking day with max occurances
                most_common_day, num_most_common = Counter(day_list).most_common(1)[0]
                best_day = days[most_common_day]
                if is_new_user:
                    response = 'Welcome %s. ' % user
                else:
                    response = 'Welcome back %s. ' % user
                response += 'Best time to post is %s%s GMT. Best day to post is %s' % (
                    best_time_hours,
                    best_time_minutes,
                    best_day
                )

            response_json = json.dumps(response)
            return HttpResponse(response_json)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TwitterUserForm()

    return render(request, 'timing/twitter_info.html', {'form': form})
