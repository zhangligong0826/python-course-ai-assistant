import { describe, expect, it } from 'vitest';
import { COURSE_ACTIONS, extractCourseGrade, isCourseAssistant } from './courseAssistant';

describe('course assistant presentation helpers', () => {
	it('only enables the course experience for tagged models', () => {
		expect(isCourseAssistant({ info: { meta: { courseAssistant: true } } })).toBe(true);
		expect(isCourseAssistant({ info: { meta: {} } })).toBe(false);
		expect(isCourseAssistant(null)).toBe(false);
	});

	it('defines the three learning entry points', () => {
		expect(COURSE_ACTIONS.map((action) => action.id)).toEqual(['ask', 'practice', 'grade']);
	});

	it('extracts a valid grade payload and leaves the explanation visible', () => {
		const result = extractCourseGrade(
			'本次练习已完成。\n```course-grade\n{"score":3,"max_score":5,"correct":3,"wrong":1,"missing":1,"recommendations":["复习函数参数"]}\n```'
		);
		expect(result.grade).toMatchObject({ score: 3, maxScore: 5, wrong: 1 });
		expect(result.content).toBe('本次练习已完成。');
	});

	it('normalizes the quiz service question-id arrays into result rows', () => {
		const result = extractCourseGrade(
			'已完成。\n```course-grade\n{"score":1,"max_score":2,"correct":["q-02-03"],"wrong":["q-02-01"],"missing":[],"recommendations":["复习 range"]}\n```'
		);
		expect(result.grade).toMatchObject({ correct: 1, wrong: 1, missing: 0 });
		expect(result.grade?.results).toEqual([
			{ questionId: 'q-02-03', status: 'correct' },
			{ questionId: 'q-02-01', status: 'wrong' }
		]);
	});

	it('keeps malformed payloads as ordinary markdown', () => {
		const content = '```course-grade\nnot json\n```';
		expect(extractCourseGrade(content)).toEqual({ content, grade: null });
	});
});
