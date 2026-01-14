/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                vaisala: {
                    blue: "#00A3E0", // Vaisala Blue
                    dark: "#000000",
                    gray: "#53565A"
                }
            }
        },
    },
    plugins: [
        require('@tailwindcss/typography'), // Optional: helpful for RAG text formatting
    ],
}