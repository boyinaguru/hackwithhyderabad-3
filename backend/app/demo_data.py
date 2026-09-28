from .models import Customer

CUSTOMERS = [
    Customer(
        id="c_rahul",
        name="Rahul Sharma",
        company="Acme Technologies",
        email="rahul@acme.example",
        device="HP LaserJet Pro M404",
        open_ticket="TCK-4821",
    ),
    Customer(
        id="c_priya",
        name="Priya Reddy",
        company="Nova Retail",
        email="priya@nova.example",
        device="Dell Latitude 7440",
        open_ticket="TCK-5178",
    ),
    Customer(
        id="c_arjun",
        name="Arjun Mehta",
        company="BluePeak Labs",
        email="arjun@bluepeak.example",
        device="Cisco AnyConnect VPN",
        open_ticket=None,
    ),
]
