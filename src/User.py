
class User:
    def __init__(self):
        self.id = None
        self.fname = None
        self.lname = None
        self.role = None
        self.roleId = None
        self.majorId = None
        
    def clear(self):
        self.id = None
        self.fname = None
        self.lname = None
        self.role = None
        self.roleId = None
        self.majorId = None
    
    def load(self, userInfo):
        if len(userInfo) != 6:
            raise IndexError(f'{len(userInfo)}: potential over/under flow')
        
        self.id, self.fname, self.lname, self.role, self.roleId, self.majorId = userInfo
