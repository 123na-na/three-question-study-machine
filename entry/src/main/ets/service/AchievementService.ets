import { Achievement } from '../model/DataModel';

export interface AchievementDef { id: string; name: string; description: string; icon: string; condition: (stats: UserStats) => boolean }

const ACHIEVEMENT_DEFS: AchievementDef[] = [
  {
    id: 'first_lesson',
    name: '初次学习',
    description: '完成第一节课的学习',
    icon: '🌟',
    condition: (s) => s.lessonsCompleted >= 1
  },
  {
    id: 'ten_lessons',
    name: '学海无涯',
    description: '完成10节课的学习',
    icon: '📚',
    condition: (s) => s.lessonsCompleted >= 10
  },
  {
    id: 'perfect_score',
    name: '完美掌握',
    description: '获得一次满分评价',
    icon: '💯',
    condition: (s) => s.perfectScores >= 1
  },
  {
    id: 'three_mastery',
    name: '三问精通',
    description: '完整掌握一个知识点的三个层次',
    icon: '🏆',
    condition: (s) => s.knowledgePointsCompleted >= 1
  },
  {
    id: 'streak_3',
    name: '持续学习',
    description: '连续学习3天',
    icon: '🔥',
    condition: (s) => s.streakDays >= 3
  },
  {
    id: 'streak_7',
    name: '一周坚持',
    description: '连续学习7天',
    icon: '⭐',
    condition: (s) => s.streakDays >= 7
  },
];

export interface UserStats {
  lessonsCompleted: number;
  perfectScores: number;
  knowledgePointsCompleted: number;
  streakDays: number;
}

let unlockedAchievements: Achievement[] = [];

export function getAchievementDefs(): AchievementDef[] {
  return ACHIEVEMENT_DEFS.map((def): AchievementDef => ({ id: def.id, name: def.name, description: def.description, icon: def.icon, condition: def.condition }));
}

export function checkAndUnlockAchievements(stats: UserStats): Achievement[] {
  const newlyUnlocked: Achievement[] = [];
  for (const def of ACHIEVEMENT_DEFS) {
    if (def.condition(stats) && !unlockedAchievements.some(a => a.id === def.id)) {
      const now = new Date();
      const achievement: Achievement = {
        id: def.id,
        name: def.name,
        description: def.description,
        icon: def.icon,
        unlocked_at: now.toISOString(),
      };
      unlockedAchievements.push(achievement);
      newlyUnlocked.push(achievement);
    }
  }
  return newlyUnlocked;
}

export function getUnlockedAchievements(): Achievement[] {
  return unlockedAchievements;
}

export function resetAchievements(): void {
  unlockedAchievements = [];
}
