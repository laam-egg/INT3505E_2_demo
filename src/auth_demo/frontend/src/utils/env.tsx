export const API_BASE_URL = "" + (import.meta.env.VITE_API_BASE_URL || "");

if (!API_BASE_URL) {
    throw new Error('Environmnt variable VITE_API_BASE_URL is not defined');
}
