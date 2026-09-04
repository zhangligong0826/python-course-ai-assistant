<script lang="ts">
	import { page } from '$app/stores';
	import { resetPassword } from '$lib/apis/auths';

	let password = '';
	let confirmPassword = '';
	let submitting = false;
	let success = false;
	let error = '';

	const submit = async () => {
		if (password !== confirmPassword) {
			error = '两次输入的密码不一致。';
			return;
		}
		const token = $page.url.searchParams.get('token') ?? '';
		if (!token) {
			error = '重置链接无效或已过期。';
			return;
		}
		submitting = true;
		error = '';
		try {
			await resetPassword(token, password);
			success = true;
		} catch (message) {
			error = `${message}`;
		} finally {
			submitting = false;
		}
	};
</script>

<svelte:head><title>重置密码 · 南开大学 AIOps 组</title></svelte:head>

<main
	class="flex min-h-screen items-center justify-center bg-gradient-to-br from-indigo-50 via-white to-violet-50 p-5 dark:from-gray-950 dark:via-gray-950 dark:to-indigo-950"
>
	<section
		class="w-full max-w-md rounded-3xl bg-white p-8 shadow-2xl shadow-indigo-950/10 dark:bg-gray-950"
	>
		<div class="mb-7 flex items-center gap-3">
			<div
				class="flex size-11 items-center justify-center rounded-xl bg-indigo-600 text-sm font-bold text-white"
			>
				NK
			</div>
			<div>
				<div class="font-semibold">南开大学 AIOps 组</div>
				<div class="text-xs text-gray-500">安全密码重置</div>
			</div>
		</div>
		{#if success}
			<h1 class="text-2xl font-semibold">密码已更新</h1>
			<p class="mt-3 text-sm text-gray-500">所有旧登录会话均已失效，请使用新密码重新登录。</p>
			<a
				class="mt-6 block w-full rounded-xl bg-indigo-600 py-3 text-center font-semibold text-white"
				href="/auth">返回登录</a
			>
		{:else}
			<h1 class="text-2xl font-semibold">设置新密码</h1>
			<form class="mt-7 space-y-4" on:submit|preventDefault={submit}>
				<div>
					<label for="password" class="mb-2 block text-sm font-medium">新密码</label><input
						id="password"
						bind:value={password}
						type="password"
						autocomplete="new-password"
						required
						minlength="8"
						class="w-full rounded-xl border border-gray-200 bg-gray-50 px-3 py-3 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 dark:border-gray-700 dark:bg-gray-900"
					/>
				</div>
				<div>
					<label for="confirm-password" class="mb-2 block text-sm font-medium">确认新密码</label
					><input
						id="confirm-password"
						bind:value={confirmPassword}
						type="password"
						autocomplete="new-password"
						required
						minlength="8"
						class="w-full rounded-xl border border-gray-200 bg-gray-50 px-3 py-3 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 dark:border-gray-700 dark:bg-gray-900"
					/>
				</div>
				{#if error}<p class="text-sm text-red-600" role="alert">{error}</p>{/if}
				<button
					type="submit"
					disabled={submitting}
					class="w-full rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 py-3 font-semibold text-white disabled:opacity-50"
					>{submitting ? '正在更新…' : '更新密码'}</button
				>
			</form>
		{/if}
	</section>
</main>
