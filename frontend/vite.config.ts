
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
export default defineConfig({
  plugins: [vue()],
  server: { port: 5173, strictPort: true },
  build: { outDir: "dist" },
  define: {
    __API__: JSON.stringify(process.env.VITE_API_BASE || "https://regatta-api.fly.dev/api")
  }
});
