// Base URL for backend API calls.
// In production (Vercel), reads from VITE_API_URL env variable.
// In development, falls back to empty string (Vite proxy handles /api/* → localhost:5000).
const API_BASE = import.meta.env.VITE_API_URL || '';

export default API_BASE;
