# ============================================================================
# Author: Raphael da Silva
# Copyright (c) 2026 Raphael da Silva. All rights reserved.
# Proprietary and confidential software.
# Unauthorized use, copying, modification, distribution, disclosure,
# reverse engineering, sublicensing, or commercialization of this source code,
# in whole or in part, is strictly prohibited without prior written permission.
# This work is protected under Brazilian Software Law (Law No. 9,609/1998),
# Brazilian Copyright Law (Law No. 9,610/1998), and other applicable laws.
# ============================================================================

class Session:
    _user = None

    @classmethod
    def start(cls, user_data: dict):
        """
        Inicia a sessÃ£o do usuÃ¡rio
        """
        cls._user = user_data

    @classmethod
    def get(cls):
        """
        Retorna os dados do usuÃ¡rio logado
        """
        return cls._user

    @classmethod
    def is_authenticated(cls):
        """
        Verifica se existe sessÃ£o ativa
        """
        return cls._user is not None

    @classmethod
    def end(cls):
        """
        Encerra a sessÃ£o
        """
        cls._user = None

# Copyright (c) 2026 Raphael da Silva. All rights reserved.
