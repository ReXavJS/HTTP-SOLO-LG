class AdminEngine:
    def __init__(self):
        self.parties = {}
        self.next_id = 1

    def create_party(self, params):
        party_id = self.next_id
        self.parties[party_id] = params
        self.next_id += 1
        return {
            "id_party": party_id,
            "message": "Partie créée avec succès.",
            "params": params
        }

    def list_parties(self):
        return [{"id": pid, **data} for pid, data in self.parties.items()]

    def get_party(self, party_id):
        return self.parties.get(party_id, {"error": "Partie inconnue."})
