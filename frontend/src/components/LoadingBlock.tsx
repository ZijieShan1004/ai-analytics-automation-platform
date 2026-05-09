type LoadingBlockProps = {
  message?: string;
};

// Render a reusable loading block.
export function LoadingBlock({ message = "Loading..." }: LoadingBlockProps) {
  return (
    <div className="loading-block">
      <div className="spinner" />
      <span>{message}</span>
    </div>
  );
}