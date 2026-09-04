<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { getSystemDocumentation, type SystemDocumentation } from '$lib/apis/help';
	import Markdown from '$lib/components/chat/Messages/Markdown.svelte';
	import Spinner from '$lib/components/common/Spinner.svelte';

	const i18n = getContext('i18n');
	let documentation: SystemDocumentation | null = null;
	let loading = true;
	let error = '';

	const loadDocumentation = async () => {
		loading = true;
		error = '';
		try {
			documentation = await getSystemDocumentation(localStorage.token ?? '');
		} catch (err) {
			documentation = null;
			error = err instanceof Error ? err.message : $i18n.t('Failed to load system documentation');
		} finally {
			loading = false;
		}
	};

	onMount(loadDocumentation);
</script>

<svelte:head>
	<title>{$i18n.t('System Help')}</title>
</svelte:head>

<div class="min-h-screen w-full overflow-y-auto bg-white dark:bg-gray-950">
	<div class="mx-auto w-full max-w-5xl px-5 py-8 sm:px-8 lg:px-12">
		<div class="mb-8 flex items-center justify-between gap-4">
			<div>
				<h1 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">{$i18n.t('System Help')}</h1>
				<p class="mt-1 text-sm text-gray-500 dark:text-gray-400">{$i18n.t('Project documentation')}</p>
			</div>
			<button type="button" class="rounded-lg border border-gray-200 px-3 py-2 text-sm" on:click={loadDocumentation} disabled={loading}>
				{$i18n.t('Retry')}
			</button>
		</div>

		{#if loading}
			<div class="flex min-h-40 items-center justify-center"><Spinner className="size-6" /></div>
		{:else if error}
			<div class="rounded-xl border border-red-200 bg-red-50 p-5 text-red-700 dark:border-red-900/50 dark:bg-red-950/30 dark:text-red-300">
				<p class="font-medium">{$i18n.t('Failed to load system documentation')}</p>
				<p class="mt-1 text-sm">{error}</p>
				<button type="button" class="mt-4 rounded-lg bg-red-600 px-3 py-2 text-sm text-white" on:click={loadDocumentation}>
					{$i18n.t('Retry')}
				</button>
			</div>
		{:else if !documentation?.content.trim()}
			<div class="rounded-xl border border-gray-200 p-5 text-gray-500 dark:border-gray-800 dark:text-gray-400">{$i18n.t('No documentation available')}</div>
		{:else}
			<article class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-900 sm:p-8">
				<Markdown id="system-documentation" content={documentation.content} done={true} />
			</article>
		{/if}
	</div>
</div>
