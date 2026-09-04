import { beforeEach, describe, expect, it, vi } from 'vitest';
import { getSystemDocumentation } from './help';

describe('help API', () => {
	beforeEach(() => {
		vi.restoreAllMocks();
	});

	it('requests the authenticated system documentation endpoint', async () => {
		const response = {
			ok: true,
			json: vi.fn().mockResolvedValue({ title: 'Help', content: '# Docs' })
		};
		const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(response as Response);

		await expect(getSystemDocumentation('test-token')).resolves.toEqual({
			title: 'Help',
			content: '# Docs'
		});
		expect(fetchMock).toHaveBeenCalledWith(
			expect.stringContaining('/help/system-documentation'),
			expect.objectContaining({
				headers: expect.objectContaining({ authorization: 'Bearer test-token' })
			})
		);
	});

	it('exposes the server error detail', async () => {
		vi.spyOn(globalThis, 'fetch').mockResolvedValue({
			ok: false,
			json: vi.fn().mockResolvedValue({ detail: 'Document unavailable' })
		} as unknown as Response);

		await expect(getSystemDocumentation('test-token')).rejects.toThrow('Document unavailable');
	});
});
