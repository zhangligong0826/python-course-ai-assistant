<script lang="ts">
	import { COURSE_ACTIONS } from './courseAssistant';

	export let onSelect: (prompt: string) => void = () => {};
</script>

<section class="mt-5" aria-label="Python 课程学习入口">
	<div
		class="mb-4 flex items-center gap-2 text-sm font-medium text-indigo-700 dark:text-indigo-300"
	>
		<span
			class="flex size-6 items-center justify-center rounded-lg bg-indigo-100 dark:bg-indigo-950"
			>✦</span
		>
		Python 程序设计学习路径
	</div>
	<div class="grid gap-3 md:grid-cols-3">
		{#each COURSE_ACTIONS as action (action.id)}
			<button
				type="button"
				data-testid={`course-action-${action.id}`}
				class="group overflow-hidden rounded-2xl border border-gray-200 bg-white text-left shadow-sm transition duration-200 hover:-translate-y-0.5 hover:shadow-lg focus:outline-hidden focus:ring-2 focus:ring-indigo-500 dark:border-gray-800 dark:bg-gray-900"
				on:click={() => onSelect(action.prompt)}
			>
				<div class={`h-1.5 bg-gradient-to-r ${action.accentClass}`}></div>
				<div class="p-4">
					<div class="flex items-center justify-between gap-3">
						<span class="font-semibold text-gray-900 dark:text-gray-100">{action.title}</span>
						<span class="text-indigo-500 transition-transform group-hover:translate-x-0.5">→</span>
					</div>
					<p class="mt-2 text-sm leading-5 text-gray-500 dark:text-gray-400">
						{action.description}
					</p>
				</div>
			</button>
		{/each}
	</div>
	<p class="mt-3 text-xs text-gray-500 dark:text-gray-400">
		回答会优先检索课程资料；题库判分会生成可继续复习的反馈。
	</p>
</section>
