type ErrorBannerProps = {
  message: string | null;
};

// Render an error message banner.
export function ErrorBanner({ message }: ErrorBannerProps) {
  if (!message) {
    return null;
  }

  return (
    <div className="error-banner">
      {message}
    </div>
  );
}