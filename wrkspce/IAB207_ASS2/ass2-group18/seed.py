from datetime import datetime
 
from livebeat import create_app, db
 
from livebeat.models import (
    Event,
    User
)
 
from livebeat.views import GENERIC_ACK_TEXT
 
from flask_bcrypt import generate_password_hash
 
 
app = create_app()
 
 
# A finished enhanced acknowledgement (as the builder would produce for Sydney)
ENHANCED_ACK_TEXT = (
    "I would like to acknowledge the Traditional Custodians of the land on "
    "which we gather today, the Gadigal people, and pay my respects to Elders "
    "past and present. I recognise their continuing connection to Country, "
    "culture, and community. As we come together for Neon Horizons Tour, "
    "we do so with respect and understanding."
)
 
 
with app.app_context():
 
    # =========================================
    # CREATE DEMO USER
    # =========================================
 
    user = User.query.filter_by(
        email="demo@livebeat.com"
    ).first()
 
    if not user:
 
        user = User(
 
            first_name="Demo",
 
            last_name="User",
 
            email="demo@livebeat.com",
 
            password=generate_password_hash(
                "Password123"
            ).decode("utf-8"),
 
            phone="0400000000",
 
            address="Brisbane QLD"
        )
 
        db.session.add(user)
 
        db.session.commit()
 
        print("Demo user created.")
 
 
    # =========================================
    # SEED EVENTS
    # =========================================
 
    if Event.query.count() == 0:
 
        events = [
 
            # =========================================
            # ROCK EVENT
            # =========================================
 
            Event(
 
                title="Sonic Crush Festival",
 
                artist="Redline & The Amps",
 
                description="Sonic Crush Festival is one of Brisbane's best rock shows, featuring energetic live performances and a festival atmosphere.",
 
                category="Rock",
 
                status="Open",
 
                capacity=2500,
 
                date=datetime(2026, 4, 10, 18, 0),
 
                time=datetime.strptime(
                    "18:00",
                    "%H:%M"
                ).time(),
 
                end_time=datetime.strptime(
                    "22:00",
                    "%H:%M"
                ).time(),
 
                venue_name="RNA Showgrounds",
 
                venue_address="Gregory Terrace, Brisbane QLD 4006",
 
                ticket_type="standard",
 
                standard_price=65.00,
 
                vip_price=120.00,
 
                premium_price=180.00,
 
                acknowledgement=GENERIC_ACK_TEXT,
 
                image="concert1.jpg",
 
                user_id=user.id
            ),
 
 
            # =========================================
            # JAZZ EVENT
            # =========================================
 
            Event(
 
                title="Blue Note Sessions",
 
                artist="Marcus Trio",
 
                description="A smooth jazz night featuring Marcus Trio and special guests.",
 
                category="Jazz",
 
                status="Open",
 
                capacity=800,
 
                date=datetime(2026, 4, 11, 19, 0),
 
                time=datetime.strptime(
                    "19:00",
                    "%H:%M"
                ).time(),
 
                end_time=datetime.strptime(
                    "22:30",
                    "%H:%M"
                ).time(),
 
                venue_name="The Jazzlab",
 
                venue_address="Melbourne VIC",
 
                ticket_type="standard",
 
                standard_price=55.00,
 
                vip_price=95.00,
 
                premium_price=150.00,
 
                acknowledgement=GENERIC_ACK_TEXT,
 
                image="concert2.jpg",
 
                user_id=user.id
            ),
 
 
            # =========================================
            # POP EVENT
            # =========================================
 
            Event(
 
                title="Neon Horizons Tour",
 
                artist="Stella Voss",
 
                description="A high-energy pop concert with lights, visuals, and Stella Voss performing live.",
 
                category="Pop",
 
                status="Sold Out",
 
                capacity=0,
 
                date=datetime(2026, 4, 12, 20, 0),
 
                time=datetime.strptime(
                    "20:00",
                    "%H:%M"
                ).time(),
 
                end_time=datetime.strptime(
                    "23:00",
                    "%H:%M"
                ).time(),
 
                venue_name="Qudos Bank Arena",
 
                venue_address="Sydney Olympic Park NSW",
 
                ticket_type="premium",
 
                standard_price=90.00,
 
                vip_price=160.00,
 
                premium_price=240.00,
 
                acknowledgement=ENHANCED_ACK_TEXT,
 
                image="concert3.jpg",
 
                user_id=user.id
            ),
 
 
            # =========================================
            # RNB EVENT
            # =========================================
 
            Event(
 
                title="Velvet Nights",
 
                artist="Layla & The Collective",
 
                description="An RnB night with smooth vocals and live band performances.",
 
                category="RnB",
 
                status="Open",
 
                capacity=1500,
 
                date=datetime(2026, 4, 17, 19, 30),
 
                time=datetime.strptime(
                    "19:30",
                    "%H:%M"
                ).time(),
 
                end_time=datetime.strptime(
                    "23:00",
                    "%H:%M"
                ).time(),
 
                venue_name="The Fortitude Music Hall",
 
                venue_address="Fortitude Valley, Brisbane QLD",
 
                ticket_type="vip",
 
                standard_price=70.00,
 
                vip_price=130.00,
 
                premium_price=190.00,
 
                acknowledgement=None,
 
                image="concert4.jpg",
 
                user_id=user.id
            ),
 
 
            # =========================================
            # SOUL EVENT
            # =========================================
 
            Event(
 
                title="Deep Soul Revue",
 
                artist="Isaiah Carter",
 
                description="A soul music event featuring Isaiah Carter and supporting artists.",
 
                category="Soul",
 
                status="Inactive",
 
                capacity=1200,
 
                date=datetime(2025, 4, 25, 18, 30),
 
                time=datetime.strptime(
                    "18:30",
                    "%H:%M"
                ).time(),
 
                end_time=datetime.strptime(
                    "22:00",
                    "%H:%M"
                ).time(),
 
                venue_name="Enmore Theatre",
 
                venue_address="Newtown NSW",
 
                ticket_type="standard",
 
                standard_price=60.00,
 
                vip_price=110.00,
 
                premium_price=170.00,
 
                acknowledgement=GENERIC_ACK_TEXT,
 
                image="concert5.jpg",
 
                user_id=user.id
            ),
 
 
            # =========================================
            # CANCELLED EVENT
            # =========================================
 
            Event(
 
                title="Moonlight Brass Night",
 
                artist="Harbour City Collective",
 
                description="A jazz brass performance under the moonlight.",
 
                category="Jazz",
 
                status="Cancelled",
 
                capacity=900,
 
                date=datetime(2026, 5, 2, 19, 0),
 
                time=datetime.strptime(
                    "19:00",
                    "%H:%M"
                ).time(),
 
                end_time=datetime.strptime(
                    "22:00",
                    "%H:%M"
                ).time(),
 
                venue_name="The Triffid",
 
                venue_address="Brisbane QLD",
 
                ticket_type="standard",
 
                standard_price=50.00,
 
                vip_price=90.00,
 
                premium_price=140.00,
 
                acknowledgement=GENERIC_ACK_TEXT,
 
                image="concert2.jpg",
 
                user_id=user.id
            )
        ]
 
 
        db.session.add_all(events)
 
        db.session.commit()
 
        print("Dummy events added successfully.")
 
 
    else:
 
        print(
            "Events already exist. No new events added."
        )