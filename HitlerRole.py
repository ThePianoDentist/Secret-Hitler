class Role(object):
    """
    Parent role. Inherited by three subclasses: Liberal, Fascist, Hitler.
    """
    def __init__(self):
        self.party_membership = ""
        self.role = ""

    def __repr__(self):
        return self.role.title()


class Liberal(Role):
    def __init__(self):
        super(Liberal, self).__init__()
        self.is_liberal = True
        self.role = "liberal"


class Fascist(Role):
    def __init__(self, is_hitler):
        super(Fascist, self).__init__()
        self.is_liberal = False
        self.role = "hitler" if is_hitler else "fascist"
        self.is_hitler = is_hitler
