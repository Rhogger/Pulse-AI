from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from pathlib import Path
from fastapi import HTTPException


class GoogleAuthService:
    def __init__(self):
        root_dir = Path(__file__).parent.parent.parent
        self.credentials_path = os.path.join(
            root_dir, 'credentials', 'credentials.json')
        self.token_path = os.path.join(root_dir, 'credentials', 'token.json')
        self.scopes = [
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/calendar.events'
        ]

    def get_credentials(self):
        """
        Gerencia o fluxo de autenticação OAuth2
        """
        if not os.path.exists(self.token_path):
            raise HTTPException(
                status_code=500,
                detail="Token não encontrado. Execute o script de autenticação inicial (scripts/authenticate_google.py)"
            )

        try:
            creds = Credentials.from_authorized_user_file(
                self.token_path, self.scopes)

            # Renova o token se necessário
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(self.token_path, "w") as token:
                    token.write(creds.to_json())

            return creds

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao gerenciar credenciais: {str(e)}"
            )
