import random
from django.core.management.base import BaseCommand
from milkman.dairy import milkman
from tests.utils import random_date
from datetime import datetime, timedelta
from users.models import User


class Command(BaseCommand):
    args = '<amount>'
    help = 'Fills existing database with test users'

    def handle(self, *args, **options):
        amount = int(args[0])
        for i in range(amount):
            gender = random.choice((User.GENDERS.male, User.GENDERS.female))
            user = milkman.deliver('users.user',
                provider="facebook",
                birthday=random_date(
                    datetime.now()-timedelta(days=70*365),
                    datetime.now()-timedelta(days=18*365)
                ),
                gender=gender,
                first_name=str(i),
                last_name="_" + str(gender)
            )
            self.stdout.write("Created user '{0}'".format(user))

        self.stdout.write("Successfully created test users")
