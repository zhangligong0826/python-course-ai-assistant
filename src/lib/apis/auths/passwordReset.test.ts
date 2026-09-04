import { afterEach, describe, expect, it, vi } from 'vitest';

import { requestPasswordReset, resetPassword } from './index';

describe('password reset API', () => {
	afterEach(() => vi.unstubAllGlobals());

	it('requests a reset without exposing account state', async () => {
		const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ status: true }) });
		vi.stubGlobal('fetch', fetchMock);

		await expect(requestPasswordReset('student@nankai.edu.cn')).resolves.toEqual({ status: true });
		expect(fetchMock).toHaveBeenCalledWith(
			expect.stringContaining('/auths/forgot-password'),
			expect.objectContaining({ body: JSON.stringify({ email: 'student@nankai.edu.cn' }) })
		);
	});

	it('submits the one-time token and new password', async () => {
		const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ status: true }) });
		vi.stubGlobal('fetch', fetchMock);

		await resetPassword('one-time-token', 'strong-password');
		expect(fetchMock).toHaveBeenCalledWith(
			expect.stringContaining('/auths/reset-password'),
			expect.objectContaining({
				body: JSON.stringify({ token: 'one-time-token', new_password: 'strong-password' })
			})
		);
	});
});
