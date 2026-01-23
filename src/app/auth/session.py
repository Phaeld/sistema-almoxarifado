class Session:
    _user = None

    @classmethod
    def start(cls, user_data: dict):
        """
        Inicia a sessão do usuário
        """
        cls._user = user_data

    @classmethod
    def get(cls):
        """
        Retorna os dados do usuário logado
        """
        return cls._user

    @classmethod
    def is_authenticated(cls):
        """
        Verifica se existe sessão ativa
        """
        return cls._user is not None

    @classmethod
    def end(cls):
        """
        Encerra a sessão
        """
        cls._user = None
