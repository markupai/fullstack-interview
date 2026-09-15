import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "wxt";

export default defineConfig({
    modules: ["@wxt-dev/module-react"],
    manifest: {
        name: "Interview Extension",
        permissions: ["storage", "sidePanel"],
        action: {},
    },
    vite: () => ({
        plugins: [tailwindcss()],
    }),
});
