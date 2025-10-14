from flask_restx import reqparse

class Pageable:
    def __init__(self, page, size):
        # type: (Pageable, int, int) -> None
        """
        page number starts at 0.
        """
        self.page = page
        self.size = size

    def get_skip(self):
        return self.page * self.size
    
    def get_limit(self):
        return self.size
    
    def get_kwargs(self):
        return {
            "skip": self.get_skip(),
            "limit": self.get_limit(),
        }
    
    def increment(self):
        self.page += 1
    
    @staticmethod
    def pageable_query_params(parser=None):
        if not parser:
            parser = reqparse.RequestParser()
        parser.add_argument('pageNumber', type=int, required=False, default=0, help='Page number')
        parser.add_argument('pageSize', type=int, required=False, default=2, help='Page size')
        return parser
    
    @classmethod
    def from_query_params(cls, parser_args):
        page = parser_args.get("pageNumber")
        size = parser_args.get("pageSize")
        return cls(page, size)
