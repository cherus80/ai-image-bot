"""
Google OAuth utilities for validating Google ID tokens.

Uses google-auth library to verify ID tokens from Google Sign-In.
"""

from typing import Optional
from google.auth.transport import requests
from google.oauth2 import id_token
from app.core.config import settings


class GoogleOAuthError(Exception):
    """Exception raised for Google OAuth validation errors"""
    pass


def verify_google_id_token(id_token_string: str) -> dict:
    """
    Verify a Google ID token and extract user information.

    Args:
        id_token_string: The ID token from Google Sign-In (JWT string)

    Returns:
        dict: User information from the token
            {
                'sub': '123456789',  # Google user ID
                'email': 'user@example.com',
                'email_verified': True,
                'name': 'John Doe',
                'given_name': 'John',
                'family_name': 'Doe',
                'picture': 'https://...',
            }

    Raises:
        GoogleOAuthError: If token is invalid or verification fails

    Example:
        >>> user_info = verify_google_id_token(id_token)
        >>> print(user_info['email'])
        'user@example.com'
    """
    try:
        # Verify the token
        # This will:
        # 1. Verify the signature using Google's public keys
        # 2. Verify the token hasn't expired
        # 3. Verify the audience matches our client ID
        idinfo = id_token.verify_oauth2_token(
            id_token_string,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        # Verify the issuer
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise GoogleOAuthError('Invalid token issuer')

        # Extract user information
        return {
            'sub': idinfo['sub'],  # Google user ID (unique)
            'email': idinfo.get('email'),
            'email_verified': idinfo.get('email_verified', False),
            'name': idinfo.get('name'),
            'given_name': idinfo.get('given_name'),
            'family_name': idinfo.get('family_name'),
            'picture': idinfo.get('picture'),
        }

    except ValueError as e:
        # Invalid token
        raise GoogleOAuthError(f'Invalid Google ID token: {str(e)}')

    except Exception as e:
        # Other errors
        raise GoogleOAuthError(f'Google OAuth verification failed: {str(e)}')


def get_google_user_info(id_token_string: str) -> Optional[dict]:
    """
    Safely get Google user info, returning None on error.

    Args:
        id_token_string: The ID token from Google Sign-In

    Returns:
        dict | None: User information or None if verification fails

    Example:
        >>> user_info = get_google_user_info(id_token)
        >>> if user_info:
        ...     print(f"User: {user_info['email']}")
    """
    try:
        return verify_google_id_token(id_token_string)
    except GoogleOAuthError:
        return None
