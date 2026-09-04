export type QuickAction = {
	id: 'summarize' | 'translate' | 'optimize';
	labelKey: string;
	promptKey: string;
};

export const QUICK_ACTIONS: QuickAction[] = [
	{
		id: 'summarize',
		labelKey: 'Summarize content',
		promptKey: 'Please summarize the following content and list 3 key conclusions:'
	},
	{
		id: 'translate',
		labelKey: 'Translate to Chinese',
		promptKey:
			'Please translate the following content into Chinese while preserving the original meaning and using accurate professional terminology:'
	},
	{
		id: 'optimize',
		labelKey: 'Optimize writing',
		promptKey: 'Please improve the following content to make it clearer, more concise, and more professional:'
	}
];

export const prependQuickAction = (quickPrompt: string, currentPrompt: string) =>
	`${quickPrompt}\n${currentPrompt}`;
