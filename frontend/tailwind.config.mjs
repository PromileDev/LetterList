/** @type {import('tailwindcss').Config} */
export default {
	content: [
		'./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}',
		'./node_modules/flowbite/**/*.js'
	],
	theme: {
		extend: {
			colors:{
				"brand": "#fdba74",
				"darkest": "#3b3732",
				"dark": "#615951",
				"mid": "#bdb0a1",
				"light": "#dbcfc0",
				"lightest": "#FFFFFF"
			}
		},
	},
	plugins: [
		require('flowbite/plugin')
	],
}
