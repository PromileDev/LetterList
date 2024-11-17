/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
		extend: {
			colors:{
				"brand": "#fdba74",
				"darkest": "#3b3732",
				"dark": "#615951",
				"mid": "#8db0a1",
				"light": "#dbcfc0",
				"lightest": "#FFFFFF",
			}
		},
	},
	plugins: [],
}
