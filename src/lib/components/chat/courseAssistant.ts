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
		title: '课程问答',
		description: '先检索课程资料，再用带引用的方式解释。',
		prompt: '请先检索 Python 程序设计课程资料，再回答我的问题，并在结尾列出资料依据：',
		accentClass: 'from-indigo-500 via-violet-500 to-fuchsia-500'
	},
	{
		id: 'practice',
		title: '生成练习',
		description: '按章节、难度和题型生成针对性练习。',
		prompt:
			'请调用题库工具，为我生成练习。章节：第02章；难度：beginner；题型：single_choice；数量：3。',
		accentClass: 'from-cyan-500 via-sky-500 to-indigo-500'
	},
	{
		id: 'grade',
		title: '提交答案',
		description: '自动判分并给出错因和复习建议。',
		prompt:
			'我想提交练习答案。请先向我索取 quiz_id 和每道题的答案，然后调用判分工具并输出学习建议。',
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
