const protocol = "http";
const hostname = "localhost";
const port = "8000";
const api = "api";

const host = protocol + "://" + hostname + ":" + port + "/" + api + "/";

/**
 * Get json object from the api server.
 * @param {string} apiurl - The url of the api.
 * @return {object} - JSON object.
 * 
 * @example
 * ```js
 * Api.get("alerts/get_alerts").then(response => {
 * 		console.log(response);
 * });
 * ```
 * 
 */
async function get(apiurl) {
	const response = await fetch(host + apiurl);
	return response.json();
}

/**
 * Sent json object to the api server and get the response.
 * @param {string} apiurl - The url of the api.
 * @param {object} data - Post data to send.
 * @return {object} - JSON object.
 * 
 * @example
 * ```js
 * data = {username: "user", password: "pass"}
 * Api.post("api/login", data).then(response => {
 * 		console.log(response);
 * });
 * ```
 * 
 */
function post(apiurl, data) {
	const response = fetch(host + apiurl, {
		method: "POST",
		body: JSON.stringify(data),
	});
	return response.json();
}

/**
 * Api module
 */
export default {
	get,
	post,
};
