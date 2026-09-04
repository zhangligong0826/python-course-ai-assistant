import { describe, expect, it } from 'vitest';
import { QUICK_ACTIONS, prependQuickAction } from './quickActions';

describe('quick chat actions', () => {
	it('provides the three required actions', () => {
		expect(QUICK_ACTIONS.map((action) => action.id)).toEqual(['summarize', 'translate', 'optimize']);
	});

	it('places the quick prompt before existing input on a new line', () => {
		expect(prependQuickAction('Prompt:', 'Original content')).toBe('Prompt:\nOriginal content');
	});

	it('keeps a second empty line for a blank input', () => {
		expect(prependQuickAction('Prompt:', '')).toBe('Prompt:\n');
	});
});
