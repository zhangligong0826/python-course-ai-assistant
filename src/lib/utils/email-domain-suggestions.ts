export type EmailDomainSuggestion = {
	provider: string;
	domain: string;
	badgeClass: string;
};

export const EMAIL_DOMAIN_SUGGESTIONS: EmailDomainSuggestion[] = [
	{ provider: 'Google', domain: 'gmail.com', badgeClass: 'bg-blue-100 text-blue-700' },
	{ provider: '网易', domain: '163.com', badgeClass: 'bg-red-100 text-red-700' },
	{ provider: '网易', domain: '126.com', badgeClass: 'bg-red-100 text-red-700' },
	{ provider: '腾讯', domain: 'qq.com', badgeClass: 'bg-sky-100 text-sky-700' },
	{ provider: '腾讯', domain: 'foxmail.com', badgeClass: 'bg-sky-100 text-sky-700' },
	{ provider: 'Apple', domain: 'icloud.com', badgeClass: 'bg-gray-200 text-gray-700' }
];

export const getEmailDomainSuggestions = (email: string): EmailDomainSuggestion[] => {
	const atIndex = email.lastIndexOf('@');
	if (atIndex <= 0 || email.indexOf('@') !== atIndex) {
		return [];
	}

	const typedDomain = email
		.slice(atIndex + 1)
		.trim()
		.toLowerCase();
	return EMAIL_DOMAIN_SUGGESTIONS.filter(
		({ domain }) => domain.startsWith(typedDomain) && domain !== typedDomain
	);
};

export const applyEmailDomain = (email: string, domain: string): string => {
	const atIndex = email.lastIndexOf('@');
	return atIndex > 0 ? `${email.slice(0, atIndex)}@${domain}` : email;
};
