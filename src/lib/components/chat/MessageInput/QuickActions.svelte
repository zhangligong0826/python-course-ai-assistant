<script lang="ts">
	import { getContext } from 'svelte';
	import { QUICK_ACTIONS } from './quickActions';

	const i18n = getContext('i18n');

	export let onSelect: (prompt: string) => void = () => {};
</script>

<div
	class="aiops-glass-chip-row mx-4 mb-4 mt-4 flex flex-wrap gap-2.5"
	aria-label={$i18n.t('Quick actions')}
>
	{#each QUICK_ACTIONS as action (action.id)}
		<button
			type="button"
			data-testid={`quick-action-${action.id}`}
			class="aiops-glass-chip rounded-full border border-white/70 px-3.5 py-1.5 text-sm text-gray-700 transition hover:-translate-y-px hover:border-indigo-200 focus:outline-hidden focus:ring-2 focus:ring-indigo-300 dark:border-white/10 dark:text-gray-200"
			on:click={() => onSelect($i18n.t(action.promptKey))}
		>
			{$i18n.t(action.labelKey)}
		</button>
	{/each}
</div>
