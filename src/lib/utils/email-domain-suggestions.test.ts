import { describe, expect, it } from 'vitest';

import { applyEmailDomain, getEmailDomainSuggestions } from './email-domain-suggestions';

describe('email domain suggestions', () => {
	it('lists the supported providers after an at sign', () => {
		expect(getEmailDomainSuggestions('1063896870@').map(({ domain }) => domain)).toEqual([
			'gmail.com',
			'163.com',
			'126.com',
			'qq.com',
			'foxmail.com',
			'icloud.com'
		]);
	});

	it('filters suggestions by the typed domain prefix', () => {
		expect(getEmailDomainSuggestions('student@q').map(({ domain }) => domain)).toEqual(['qq.com']);
	});

	it('does not suggest before an at sign or after an exact domain', () => {
		expect(getEmailDomainSuggestions('student')).toEqual([]);
		expect(getEmailDomainSuggestions('student@qq.com')).toEqual([]);
	});

	it('replaces only the domain portion of the address', () => {
		expect(applyEmailDomain('1063896870@q', 'qq.com')).toBe('1063896870@qq.com');
	});
});
