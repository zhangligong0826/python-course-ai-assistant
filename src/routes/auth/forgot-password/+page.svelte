<script lang="ts">
	import { requestPasswordReset } from '$lib/apis/auths';

	let email = '';
	let submitting = false;
	let sent = false;
	let error = '';

	const submit = async () => {
		submitting = true;
		error = '';
		try {
			await requestPasswordReset(email.trim().toLowerCase());
			sent = true;
		} catch (message) {
			error = `${message}`;
		} finally {
			submitting = false;
		}
	};
</script>

<svelte:head><title>找回密码 · 南开大学 AIOps 组</title></svelte:head>

<main
	class="flex min-h-screen items-center justify-center bg-gradient-to-br from-indigo-50 via-white to-violet-50 p-5 dark:from-gray-950 dark:via-gray-950 dark:to-indigo-950"
>
	<section
		class="w-full max-w-md rounded-3xl border border-white bg-white/90 p-8 shadow-2xl shadow-indigo-950/10 dark:border-gray-800 dark:bg-gray-950"
	>
		<a href="/auth" class="mb-8 inline-flex text-sm text-indigo-600">← 返回登录</a>
		<div class="mb-7 flex items-center gap-3">
			<div
				class="flex size-11 items-center justify-center rounded-xl bg-indigo-600 text-sm font-bold text-white"
			>
				NK
			</div>
			<div>
				<div class="font-semibold">南开大学 AIOps 组</div>
				<div class="text-xs text-gray-500">Python 程序设计 AI 助教</div>
			</div>
		</div>
		{#if sent}
			<h1 class="text-2xl font-semibold">请检查邮箱</h1>
			<p class="mt-3 text-sm leading-6 text-gray-600 dark:text-gray-300">
				如果该邮箱已注册，你将收到一封包含 15 分钟有效链接的邮件。
			</p>
		{:else}
			<h1 class="text-2xl font-semibold">找回密码</h1>
			<p class="mt-2 text-sm text-gray-500">输入管理员为你创建账户时使用的邮箱。</p>
			<form class="mt-7" on:submit|preventDefault={submit}>
				<label for="email" class="mb-2 block text-sm font-medium">邮箱</label>
				<input
					id="email"
					bind:value={email}
					type="email"
					autocomplete="email"
					required
					class="w-full rounded-xl border border-gray-200 bg-gray-50 px-3 py-3 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 dark:border-gray-700 dark:bg-gray-900"
					placeholder="name@example.com"
				/>
				{#if error}<p class="mt-2 text-sm text-red-600" role="alert">{error}</p>{/if}
				<button
					type="submit"
					disabled={submitting}
					class="mt-6 w-full rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 py-3 font-semibold text-white disabled:opacity-50"
					>{submitting ? '正在发送…' : '发送重置邮件'}</button
				>
			</form>
		{/if}
	</section>
</main>
