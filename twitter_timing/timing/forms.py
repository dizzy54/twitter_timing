from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings

# import pprint

import twitter


class TwitterUserForm(forms.Form):
    username = forms.CharField(label='Your Twitter username', max_length=100, required=False)
    user_id = forms.CharField(label='Your Twitter user id', max_length=100, required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        # print(cleaned_data)

        # validate if either fields are present
        username = cleaned_data['username']
        user_id = cleaned_data['user_id']
        if username == '' and user_id == '':
            raise ValidationError(('Either of Fields username and user_id required.'), code='invalid')

        # validate user info
        api = twitter.Api(
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
            access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
        )
        try:
            # check if user_id is input (default behaviour, checks for user_id if both given)
            if user_id != '':
                user = api.GetUser(user_id=user_id)
                # print(user)
            else:
                user = api.GetUser(screen_name=username)
                # print(user)
        except twitter.error.TwitterError as e:
            raise ValidationError((e.message), code='invalid')
            # raise ValidationError(('Specified username / user_id is invalid.'), code='invalid')

        # get followers
        user_id = user.id
        try:
            followers = api.GetFollowers(user_id=user_id)
        except twitter.error.TwitterError as e:
            raise ValidationError((e.message), code='invalid')

        cleaned_data['twitter_followers'] = followers

        return cleaned_data
