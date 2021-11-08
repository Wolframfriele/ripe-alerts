module.exports = {
	mode: 'jit',
	purge: {
		enabled: true,
		preserveHtmlElements: false,
		mode: 'all', 
		content: ['./public/index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
	},
	darkMode: false, // or 'media' or 'class'
	theme: {
	  extend: {},
	},
	variants: {
	  extend: {},
	},
	plugins: [],
}