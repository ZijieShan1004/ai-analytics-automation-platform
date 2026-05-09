import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Configure the Vite React application.
export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173
  }
});