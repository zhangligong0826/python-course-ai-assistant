<script lang="ts">
	import { getContext } from 'svelte';
	import { QUICK_ACTIONS } from './quickActions';

	const i18n = getContext('i18n');

	export let onSelect: (prompt: string) => void = () => {};
</script>

<div class="mx-2 mb-2 flex flex-wrap gap-2" aria-label={$i18n.t('Quick actions')}>
	{#each QUICK_ACTIONS as action (action.id)}
		<button
			type="button"
			data-testid={`quick-action-${action.id}`}
			class="rounded-full border border-gray-200 bg-white px-3 py-1.5 text-sm text-gray-700 transition-colors hover:border-gray-300 hover:bg-gray-50 focus:outline-hidden dark:border-gray-700 dark:bg-gray-900 dark:text-gray-200 dark:hover:border-gray-600 dark:hover:bg-gray-800"
			on:click={() => onSelect($i18n.t(action.promptKey))}
		>
			{$i18n.t(action.labelKey)}
		</button>
	{/each}
</div>
