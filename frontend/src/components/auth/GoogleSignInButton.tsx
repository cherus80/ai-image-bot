/**
 * Google Sign-In Button Component
 *
 * Renders Google's official Sign-In button and handles OAuth flow
 */

import { useEffect, useRef, useState } from 'react';
import { useAuth } from '../../store/authStore';
import type { GoogleSignInResponse, GoogleSignInButtonConfig } from '../../types/auth';

interface GoogleSignInButtonProps {
  onSuccess?: () => void;
  onError?: (error: string) => void;
  text?: 'signin_with' | 'signup_with' | 'continue_with';
  theme?: 'outline' | 'filled_blue' | 'filled_black';
  size?: 'large' | 'medium' | 'small';
  width?: number;
}

export function GoogleSignInButton({
  onSuccess,
  onError,
  text = 'signin_with',
  theme = 'outline',
  size = 'large',
  width,
}: GoogleSignInButtonProps) {
  const buttonRef = useRef<HTMLDivElement>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { loginWithGoogle } = useAuth();

  const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

  useEffect(() => {
    // Check if Google Identity Services script is loaded
    if (!window.google) {
      console.error('Google Identity Services not loaded. Add script to index.html');
      onError?.('Google Sign-In not available');
      return;
    }

    if (!clientId) {
      console.error('Google Client ID not configured. Set VITE_GOOGLE_CLIENT_ID in .env');
      onError?.('Google Sign-In not configured');
      return;
    }

    // Initialize Google Sign-In
    window.google.accounts.id.initialize({
      client_id: clientId,
      callback: handleCredentialResponse,
      auto_select: false,
      cancel_on_tap_outside: true,
    });

    // Render the button
    if (buttonRef.current) {
      const config: GoogleSignInButtonConfig = {
        type: 'standard',
        theme,
        size,
        text,
        shape: 'rectangular',
        logo_alignment: 'left',
      };

      if (width) {
        config.width = width;
      }

      window.google.accounts.id.renderButton(buttonRef.current, config);
    }
  }, [clientId, theme, size, text, width]);

  const handleCredentialResponse = async (response: GoogleSignInResponse) => {
    setIsLoading(true);

    try {
      // Send ID token to backend
      await loginWithGoogle(response.credential);

      // Success
      onSuccess?.();
    } catch (error: any) {
      console.error('Google Sign-In error:', error);
      const errorMessage =
        error.response?.data?.detail || error.message || 'Google Sign-In failed';
      onError?.(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  // Show loading state or placeholder
  if (!window.google || !clientId) {
    return (
      <div className="flex items-center justify-center p-3 border border-gray-300 rounded-md bg-gray-50">
        <span className="text-sm text-gray-500">Loading Google Sign-In...</span>
      </div>
    );
  }

  return (
    <div className="relative">
      {/* Google button will be rendered here */}
      <div ref={buttonRef} className={isLoading ? 'opacity-50 pointer-events-none' : ''} />

      {/* Loading overlay */}
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75">
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
        </div>
      )}
    </div>
  );
}
