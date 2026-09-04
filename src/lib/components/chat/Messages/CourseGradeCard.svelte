<script lang="ts">
	import type { CourseGrade } from '../courseAssistant';

	export let grade: CourseGrade;
</script>

<section
	class="my-4 overflow-hidden rounded-2xl border border-indigo-100 bg-white shadow-sm dark:border-indigo-900 dark:bg-gray-900"
	aria-label="练习判分结果"
>
	<div class="bg-gradient-to-r from-indigo-600 via-violet-600 to-fuchsia-600 px-5 py-4 text-white">
		<p class="text-xs font-medium uppercase tracking-wider text-indigo-100">练习结果</p>
		<div class="mt-1 flex items-end justify-between">
			<span class="text-3xl font-bold"
				>{grade.score}<span class="text-lg font-medium text-indigo-100">
					/ {grade.maxScore}</span
				></span
			>
			<span class="rounded-full bg-white/15 px-2.5 py-1 text-xs">自动判分完成</span>
		</div>
	</div>
	<div class="grid grid-cols-3 divide-x divide-gray-100 dark:divide-gray-800">
		<div class="p-3 text-center">
			<p class="text-lg font-semibold text-emerald-600">{grade.correct}</p>
			<p class="text-xs text-gray-500">正确</p>
		</div>
		<div class="p-3 text-center">
			<p class="text-lg font-semibold text-rose-500">{grade.wrong}</p>
			<p class="text-xs text-gray-500">错误</p>
		</div>
		<div class="p-3 text-center">
			<p class="text-lg font-semibold text-amber-500">{grade.missing}</p>
			<p class="text-xs text-gray-500">漏答</p>
		</div>
	</div>
	{#if grade.results.length}
		<div class="border-t border-gray-100 px-5 py-4 dark:border-gray-800">
			<p class="text-sm font-semibold text-gray-800 dark:text-gray-100">逐题结果</p>
			<div class="mt-2 flex flex-wrap gap-2">
				{#each grade.results as result (result.questionId)}
					<span
						class={`rounded-full border px-2.5 py-1 text-xs font-medium ${
							result.status === 'correct'
								? 'border-emerald-100 bg-emerald-50 text-emerald-700'
								: result.status === 'wrong'
									? 'border-rose-100 bg-rose-50 text-rose-700'
									: 'border-amber-100 bg-amber-50 text-amber-700'
						}`}
					>
						{result.questionId} · {result.status === 'correct'
							? '正确'
							: result.status === 'wrong'
								? '错误'
								: '漏答'}
					</span>
				{/each}
			</div>
		</div>
	{/if}
	{#if grade.recommendations.length}
		<div class="border-t border-gray-100 px-5 py-4 dark:border-gray-800">
			<p class="text-sm font-semibold text-gray-800 dark:text-gray-100">下一步复习</p>
			<ul class="mt-2 list-inside list-disc space-y-1 text-sm text-gray-600 dark:text-gray-300">
				{#each grade.recommendations as recommendation}
					<li>{recommendation}</li>
				{/each}
			</ul>
		</div>
	{/if}
</section>
