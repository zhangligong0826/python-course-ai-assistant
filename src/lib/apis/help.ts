import { WEBUI_API_BASE_URL } from '$lib/constants';

export type SystemDocumentation = {
	title: string;
	content: string;
	source: string;
	updated_at: string;
};

export const getSystemDocumentation = async (token: string): Promise<SystemDocumentation> => {
	const res = await fetch(`${WEBUI_API_BASE_URL}/help/system-documentation`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			authorization: `Bearer ${token}`
		}
	});

	if (!res.ok) {
		let detail = 'Failed to load system documentation';
		try {
			const body = await res.json();
			detail = body?.detail ?? detail;
		} catch {
			// Keep the stable fallback when the server response is not JSON.
		}
		throw new Error(detail);
	}

	return res.json();
};
