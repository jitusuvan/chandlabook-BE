from django.core.management.base import BaseCommand
from faker import Faker
from api.Event.model import Event
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seed Event model with fake data'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of events to create')

    def handle(self, *args, **options):
        fake = Faker()
        count = options['count']
        
        for _ in range(count):
            event_type = random.choice(['chandlo', 'marriage'])
            select_type = random.choice(['mukel', 'aavel'])
            
            event_date = fake.date_between(start_date='-1y', end_date='+1y')
            bride_groom_name = None
            
            if event_type == 'marriage':
                bride_groom_name = fake.name()
            
            Event.objects.create(
                name=f"{event_type.title()} Event {_+1}",
                date=event_date,
                event_type=event_type,
                select_type=select_type,
                bride_groom_name=bride_groom_name
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} events')
        )