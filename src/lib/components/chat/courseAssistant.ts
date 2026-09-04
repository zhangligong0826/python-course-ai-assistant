export type CourseAction = {
	id: 'ask' | 'practice' | 'grade';
	title: string;
	description: string;
	prompt: string;
	accentClass: string;
};

export type CourseGrade = {
	score: number;
	maxScore: number;
	correct: number;
	wrong: number;
	missing: number;
	results: Array<{
		questionId: string;
		status: 'correct' | 'wrong' | 'missing';
	}>;
	recommendations: string[];
};

export const COURSE_ACTIONS: CourseAction[] = [
	{
		id: 'ask',
		title: '知识问答',
		description: '先检索 AIOps 知识库，再用带引用的方式解释。',
		prompt: '请先检索 AIOps 智能运维知识库，再回答我的问题，并在结尾列出资料依据：',
		accentClass: 'from-indigo-500 via-violet-500 to-fuchsia-500'
	},
	{
		id: 'practice',
		title: '故障诊断',
		description: '基于告警、指标和日志做根因分析与处置建议。',
		prompt:
			'请检索 AIOps 知识库，按照"现象分析→可能根因→排查步骤→处置建议"的结构，帮我演练一个运维故障诊断场景：服务接口响应时间突增、错误率上升。',
		accentClass: 'from-cyan-500 via-sky-500 to-indigo-500'
	},
	{
		id: 'grade',
		title: '自测练习',
		description: '调用题库工具生成练习、提交判分并给出复习建议。',
		prompt:
			'我想做自测练习。请先调用题库工具为我生成练习（章节：第02章；难度：beginner；题型：single_choice；数量：3），并在我提交答案后调用判分工具输出学习建议。',
		accentClass: 'from-amber-400 via-orange-500 to-rose-500'
	}
];

export const isCourseAssistant = (model: any): boolean =>
	model?.info?.meta?.courseAssistant === true;

const GRADE_BLOCK = /\n?```course-grade\s*\n([\s\S]*?)\n```\s*$/;

const gradeCount = (value: unknown): number | null => {
	if (Number.isInteger(value) && (value as number) >= 0) return value as number;
	if (Array.isArray(value) && value.every((item) => typeof item === 'string')) return value.length;
	return null;
};

const resultsFromPayload = (payload: Record<string, unknown>) => {
	if (Array.isArray(payload.results)) {
		const results = payload.results
			.filter(
				(item): item is Record<string, unknown> =>
					typeof item === 'object' && item !== null && typeof item.question_id === 'string'
			)
			.map((item) => ({
				questionId: item.question_id as string,
				status: item.status
			}));
		if (results.every((item) => ['correct', 'wrong', 'missing'].includes(item.status as string))) {
			return results as CourseGrade['results'];
		}
	}

	return (['correct', 'wrong', 'missing'] as const).flatMap((status) =>
		Array.isArray(payload[status])
			? payload[status]
					.filter((questionId): questionId is string => typeof questionId === 'string')
					.map((questionId) => ({ questionId, status }))
			: []
	);
};

export const extractCourseGrade = (
	content: string
): { content: string; grade: CourseGrade | null } => {
	const match = content.match(GRADE_BLOCK);
	if (!match) return { content, grade: null };

	try {
		const payload = JSON.parse(match[1]);
		if (
			!Number.isInteger(payload.score) ||
			payload.score < 0 ||
			!Number.isInteger(payload.max_score) ||
			payload.max_score < 0
		) {
			return { content, grade: null };
		}
		const correct = gradeCount(payload.correct);
		const wrong = gradeCount(payload.wrong);
		const missing = gradeCount(payload.missing);
		if (correct === null || wrong === null || missing === null) return { content, grade: null };
		if (payload.score > payload.max_score || !Array.isArray(payload.recommendations)) {
			return { content, grade: null };
		}
		return {
			content: content.slice(0, match.index).trim(),
			grade: {
				score: payload.score,
				maxScore: payload.max_score,
				correct,
				wrong,
				missing,
				results: resultsFromPayload(payload),
				recommendations: payload.recommendations.filter((item: unknown) => typeof item === 'string')
			}
		};
	} catch {
		return { content, grade: null };
	}
};
