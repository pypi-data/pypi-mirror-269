# safety_kit_pkg/safety.py

class SafetyTips:
    def __init__(self):
        # Initialize safety tips data (e.g., from a database or external API)
        self.tips = [
            "Wear a helmet at all times while riding.",
            "Always perform a pre-ride inspection of your motorcycle.",
            "Ride defensively and be aware of your surroundings.",
            # Add more safety tips as needed
        ]

    def get_random_tip(self):
        # Return a random safety tip
        import random
        return random.choice(self.tips)


class EmergencyContacts:
    def __init__(self):
        # Initialize emergency contact information (e.g., from a database or external API)
        self.contacts = {
            "Police": "911",
            "Ambulance": "911",
            "Roadside Assistance": "1-800-555-HELP",
            # Add more emergency contacts as needed
        }

    def get_contact(self, name):
        # Get the contact information for a specific emergency service
        return self.contacts.get(name)


class FirstAidGuide:
    def __init__(self):
        # Initialize first aid guide data (e.g., from a database or external API)
        self.guides = {
            "CPR": "Perform chest compressions and rescue breaths.",
            "Bleeding Control": "Apply direct pressure to the wound.",
            # Add more first aid guides as needed
        }

    def get_guide(self, name):
        # Get the first aid guide for a specific condition or procedure
        return self.guides.get(name)
