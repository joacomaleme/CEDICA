from sqlalchemy.orm.session import make_transient

class Generic_sql_object(): #Abstract class
    def deepcopy(self):
        id = self.id
        make_transient(self)
        self.id = id
        return self