from tales_django.models import Track
from tales_django.models import User

user = User.objects.get(email='dmia@yandex.ru')
track = Track.objects.all()[:1].get()
user.favorite_tracks.add(track)
user.favorite_tracks.all()
user.save()
