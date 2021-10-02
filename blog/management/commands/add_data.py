import random
import sys

from blog.models import Comment, Post

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError

from faker import Faker


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('number',
                            default=200,
                            type=int)

    def handle(self, *args, **kwargs):
        number = kwargs['number']
        try:
            fake = Faker()
            User = get_user_model()
            gum_li = [User(username=fake.user_name(), email=fake.ascii_email(),
                           password=make_password(fake.swift())) for _ in range(1, number)]

            User.objects.bulk_create(gum_li)
            gum_id = User.objects.values_list('id', flat=True)
            post_li = [Post(title=(fake.text(max_nb_chars=25))[:-1],
                            text=str(fake.paragraphs(nb=random.randint(10, 50))).
                            replace("[", '').replace("]", '').
                            replace("'", '').replace(",", ''),
                            description=str(fake.paragraphs(nb=random.randint(1, 5))).
                            replace("[", '').replace("]", '').
                            replace("'", '').replace(",", ''),
                            author_id=random.choice(gum_id),
                            img=fake.image_url(width=random.randint(225, 825),
                                               height=random.randint(225, 825)))
                       for _ in range(1, number)]

            Post.objects.bulk_create(post_li)
            post_id = Post.objects.values_list('id', flat=True)

            com_li = [Comment(username=fake.user_name(),
                              text=str(fake.paragraphs(nb=random.randint(1, 5))).
                              replace("[", '').replace("]", '').
                              replace("'", '').replace(",", ''),
                              is_published=random.choice((True, False)),
                              post_id=random.choice(post_id)) for _ in range(1, number)]
            Comment.objects.bulk_create(com_li)

            sys.stdout.write("!SUCCESS!")

        except (Post.DoesNotExist or Comment.DoesNotExist):
            raise CommandError('Smth wrong :(')
