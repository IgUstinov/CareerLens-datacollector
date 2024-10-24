class Params:
    professional_role: int
    page: int
    per_page: int

    def __init__(self,professional_role=96,page=0,per_page=20):
        self.professional_role = professional_role
        self.page=page
        self.per_page=per_page

    def  get_params(self):
        return dict({
            "professional_role": self.professional_role,
            "page": self.page,
            "per_page": self.per_page
        })