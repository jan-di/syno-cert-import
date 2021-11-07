class Util:
    @staticmethod
    def strtobool(s: str):
        return s.lower() in ['true', '1', 'yes']
