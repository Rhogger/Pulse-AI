from google_auth_oauthlib.flow import InstalledAppFlow
import os
from pathlib import Path

def authenticate():
    root_dir = Path(__file__).parent.parent
    credentials_path = os.path.join(root_dir, 'credentials', 'credentials.json')
    token_path = os.path.join(root_dir, 'credentials', 'token.json')
    
    scopes = [
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/calendar.events'
    ]

    if not os.path.exists(credentials_path):
        print("❌ Arquivo credentials.json não encontrado em credentials/")
        return

    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path, 
            scopes
        )
        creds = flow.run_local_server(port=0)

        # Salva o token
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, "w") as token:
            token.write(creds.to_json())
        
        print("✅ Autenticação realizada com sucesso!")
        print(f"✅ Token salvo em {token_path}")

    except Exception as e:
        print(f"❌ Erro durante autenticação: {str(e)}")

if __name__ == "__main__":
    authenticate() 