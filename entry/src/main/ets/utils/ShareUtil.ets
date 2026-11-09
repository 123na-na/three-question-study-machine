import { BusinessError } from '@kit.BasicServicesKit';
import { common } from '@kit.AbilityKit';

interface ShareAchievementInfo {
  icon: string;
  name: string;
  description: string;
}

interface ShareCertificateInfo {
  course_name: string;
  avg_score: number;
}

export class ShareUtil {

  static async shareText(context: Context, title: string, text: string): Promise<void> {
    try {
      const uiContext: common.UIAbilityContext = context as common.UIAbilityContext;
      await uiContext.startAbility({
        action: 'ohos.want.action.sendData',
        type: 'text/plain',
        parameters: {
          'ability.params.stream': text,
          'shareTitle': title
        }
      });
    } catch (error) {
      console.error('Share failed:', error);
    }
  }

  static async shareAchievement(context: Context, achievement: ShareAchievementInfo): Promise<void> {
    const text = `🎀 我在「问枢」学习中获得了成就！\n\n${achievement.icon} ${achievement.name}\n${achievement.description}\n\n「问枢」- 是什么 → 为什么 → 怎么用`;
    await ShareUtil.shareText(context, '分享学习成就', text);
  }

  static async shareCertificate(context: Context, cert: ShareCertificateInfo): Promise<void> {
    const text = `🎗 我在「问枢」完成了课程！\n\n课程：${cert.course_name}\n综合评分：${cert.avg_score}分\n\n「问枢」- 是什么 → 为什么 → 怎么用`;
    await ShareUtil.shareText(context, '分享学习证书', text);
  }

  static async shareReport(context: Context, reportText: string): Promise<void> {
    await ShareUtil.shareText(context, '分享学习报告', reportText);
  }
}
