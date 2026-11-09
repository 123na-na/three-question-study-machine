"""Part 5: Restore remaining corrupted files"""
import os

BASE = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

def write_file(rel_path, content):
    fp = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Restored: {rel_path}')

# ---- utils/ShareUtil.ets (corrupted Chinese text) ----
write_file('utils/ShareUtil.ets', """\
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
    const text = `🎀 我在「问枢」学习中获得了成就！\\n\\n${achievement.icon} ${achievement.name}\\n${achievement.description}\\n\\n「问枢」- 是什么 → 为什么 → 怎么用`;
    await ShareUtil.shareText(context, '分享学习成就', text);
  }

  static async shareCertificate(context: Context, cert: ShareCertificateInfo): Promise<void> {
    const text = `🎗 我在「问枢」完成了课程！\\n\\n课程：${cert.course_name}\\n综合评分：${cert.avg_score}分\\n\\n「问枢」- 是什么 → 为什么 → 怎么用`;
    await ShareUtil.shareText(context, '分享学习证书', text);
  }

  static async shareReport(context: Context, reportText: string): Promise<void> {
    await ShareUtil.shareText(context, '分享学习报告', reportText);
  }
}
""")

# ---- LearnTab.ets (WITH formatting edit) ----
write_file('component/LearnTab.ets', """\
import { KnowledgePoint } from '../model/DataModel';
import { Colors, Spacing, Radius } from '../constants/Theme';
import { STEP_LABELS } from '../constants/AppConstants';
import { calculateOverallScore } from '../utils/ScoreCalculator';
import { getCompletedSessionCount, getAvgScore } from '../service/DatabaseHelper';
import router from '@ohos.router';

@Component
export struct LearnTab {
  @ObjectLink knowledgePoint: KnowledgePoint;
  @State whatScore: number = 0;
  @State whyScore: number = 0;
  @State howScore: number = 0;
  @State overallScore: number = 0;
  @State isLoading: boolean = true;

  aboutToAppear(): void {
    this.loadScores();
  }

  async loadScores(): Promise<void> {
    try {
      const whatCount = await getCompletedSessionCount(this.knowledgePoint.id);
      const whyCount = await getCompletedSessionCount(this.knowledgePoint.id);
      const howCount = await getCompletedSessionCount(this.knowledgePoint.id);
      if (whatCount > 0) {
        this.whatScore = await getAvgScore(this.knowledgePoint.id);
      }
      if (whyCount > 0) {
        this.whyScore = await getAvgScore(this.knowledgePoint.id);
      }
      if (howCount > 0) {
        this.howScore = await getAvgScore(this.knowledgePoint.id);
      }
      this.overallScore = calculateOverallScore({
        'what': this.whatScore,
        'why': this.whyScore,
        'how': this.howScore
      });
      this.isLoading = false;
    } catch (err) {
      console.error('[LearnTab] loadScores error: ' + JSON.stringify(err));
      this.isLoading = false;
    }
  }

  build() {
    Column() {
      // Content display
      Column() {
        Text(this.knowledgePoint.title)
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
          .fontColor(Colors.TEXT)
          .width('100%')
        Text(this.knowledgePoint.content)
          .fontSize(15)
          .fontColor(Colors.TEXT_SECONDARY)
          .lineHeight(24)
          .margin({ top: Spacing.md })
          .width('100%')
      }
      .padding(Spacing.lg)
      .backgroundColor(Colors.CARD)
      .borderRadius(Radius.md)
      .shadow({ radius: 4, color: Colors.SHADOW })
      .width('100%')

      // Step buttons
      Column() {
        Text('三问学习')
          .fontSize(16)
          .fontWeight(FontWeight.Semibold)
          .fontColor(Colors.TEXT)
          .width('100%')
          .margin({ bottom: Spacing.md })

        StepButton({
          icon: '🤔',
          label: STEP_LABELS.what,
          subtitle: '理解概念的定义和内涵',
          score: this.whatScore,
          color: '#8B5CF6',
          onClick: () => {
            router.pushUrl({
              url: 'pages/LearningSessionPage?kpId=' + this.knowledgePoint.id + '&step=what'
            });
          }
        })

        StepButton({
          icon: '🔍',
          label: STEP_LABELS.why,
          subtitle: '探究原理和逻辑关系',
          score: this.whyScore,
          color: '#3B82F6',
          onClick: () => {
            router.pushUrl({
              url: 'pages/LearningSessionPage?kpId=' + this.knowledgePoint.id + '&step=why'
            });
          }
        })

        StepButton({
          icon: '💡',
          label: STEP_LABELS.how,
          subtitle: '掌握实践和应用方法',
          score: this.howScore,
          color: '#10B981',
          onClick: () => {
            router.pushUrl({
              url: 'pages/LearningSessionPage?kpId=' + this.knowledgePoint.id + '&step=how'
            });
          }
        })
      }
      .padding(Spacing.lg)
      .backgroundColor(Colors.CARD)
      .borderRadius(Radius.md)
      .shadow({ radius: 4, color: Colors.SHADOW })
      .width('100%')
      .margin({ top: Spacing.md })

      // Overall Score
      if (this.overallScore > 0) {
        Column() {
          Row() {
            Text('综合评分')
              .fontSize(15)
              .fontColor(Colors.TEXT_SECONDARY)
            Text(this.overallScore + '分')
              .fontSize(24)
              .fontWeight(FontWeight.Bold)
              .fontColor(this.overallScore >= 60 ? Colors.SUCCESS : Colors.WARNING)
              .margin({ left: Spacing.md })
          }
          .width('100%')
          .justifyContent(FlexAlign.Center)
        }
        .padding(Spacing.lg)
        .backgroundColor(Colors.CARD)
        .borderRadius(Radius.md)
        .shadow({ radius: 4, color: Colors.SHADOW })
        .width('100%')
        .margin({ top: Spacing.md })
      }
    }
    .width('100%')
  }
}

@Component
struct StepButton {
  private icon: string = '';
  private label: string = '';
  private subtitle: string = '';
  private score: number = 0;
  private color: string = '#3B82F6';
  private onClick: () => void = () => {};

  build() {
    Row() {
      Text(this.icon)
        .fontSize(28)
      Column() {
        Text(this.label)
          .fontSize(15)
          .fontWeight(FontWeight.Semibold)
          .fontColor(Colors.TEXT)
        Text(this.subtitle)
          .fontSize(12)
          .fontColor(Colors.TEXT_SECONDARY)
          .margin({ top: 2 })
      }
      .layoutWeight(1)
      .margin({ left: Spacing.md })
      if (this.score > 0) {
        Text(this.score + '分')
          .fontSize(14)
          .fontWeight(FontWeight.Bold)
          .fontColor(this.score >= 60 ? Colors.SUCCESS : Colors.WARNING)
      }
    }
    .padding(Spacing.md)
    .backgroundColor('#F8FAFC')
    .borderRadius(Radius.sm)
    .margin({ bottom: Spacing.sm })
    .onClick(() => { this.onClick(); })
  }
}
""")

# ---- ReviewTab.ets ----
write_file('component/ReviewTab.ets', """\
import { Colors, Spacing, Radius } from '../constants/Theme';
import { getReviewsDue } from '../service/DatabaseHelper';
import router from '@ohos.router';

@Component
export struct ReviewTab {
  @State reviewsDue: any[] = [];
  @State isLoading: boolean = true;

  aboutToAppear(): void {
    this.loadReviews();
  }

  async loadReviews(): Promise<void> {
    try {
      this.reviewsDue = await getReviewsDue();
      this.isLoading = false;
    } catch (err) {
      console.error('[ReviewTab] loadReviews error: ' + JSON.stringify(err));
      this.isLoading = false;
    }
  }

  build() {
    Column() {
      Text('待复习')
        .fontSize(18)
        .fontWeight(FontWeight.Semibold)
        .fontColor(Colors.TEXT)
        .width('100%')
        .margin({ bottom: Spacing.md })

      if (this.isLoading) {
        LoadingProgress()
          .width(24)
          .height(24)
          .color(Colors.PRIMARY)
          .margin({ top: 20 })
      } else if (this.reviewsDue.length === 0) {
        Column() {
          Text('✅')
            .fontSize(32)
          Text('当前没有待复习内容')
            .fontSize(14)
            .fontColor(Colors.TEXT_SECONDARY)
            .margin({ top: Spacing.sm })
        }
        .width('100%')
        .alignItems(HorizontalAlign.Center)
        .padding({ top: 30, bottom: 30 })
      } else {
        List() {
          ForEach(this.reviewsDue, (item: any) => {
            ListItem() {
              ReviewCard({ item: item })
            }
          }, (item: any) => item.id.toString())
        }
        .width('100%')
        .layoutWeight(1)
      }
    }
    .width('100%')
    .padding(Spacing.lg)
  }
}

@Component
struct ReviewCard {
  private item: any = {};

  build() {
    Column() {
      Row() {
        Text('🔄')
          .fontSize(24)
        Column() {
          Text(this.item.course_name + ' - ' + this.item.kp_title)
            .fontSize(14)
            .fontWeight(FontWeight.Medium)
            .fontColor(Colors.TEXT)
            .maxLines(1)
            .textOverflow({ overflow: TextOverflow.Ellipsis })
          Text('上次评分: ' + Math.round(this.item.avg_score) + '分')
            .fontSize(12)
            .fontColor(Colors.TEXT_SECONDARY)
            .margin({ top: 2 })
        }
        .layoutWeight(1)
        .margin({ left: Spacing.md })
        Text('复习')
          .fontSize(13)
          .fontColor(Colors.PRIMARY)
          .fontWeight(FontWeight.Medium)
      }
      .width('100%')
    }
    .padding(Spacing.md)
    .backgroundColor(Colors.CARD)
    .borderRadius(Radius.sm)
    .shadow({ radius: 2, color: Colors.SHADOW })
    .margin({ bottom: Spacing.sm })
    .onClick(() => {
      router.pushUrl({
        url: 'pages/ReviewSessionPage?kpId=' + this.item.knowledge_point_id
      });
    })
  }
}
""")

# ---- StatsTab.ets (WITH formatting edit at line 206) ----
write_file('component/StatsTab.ets', """\
import { Colors, Spacing, Radius } from '../constants/Theme';
import { getAllCourses, getKpCount, getCompletedSessionCount, getAvgScore } from '../service/DatabaseHelper';
import { Course } from '../model/DataModel';
import { calculateOverallScore } from '../utils/ScoreCalculator';
import { MASTERY_LEVELS } from '../constants/AppConstants';

@Component
export struct StatsTab {
  @State courses: Course[] = [];
  @State isLoading: boolean = true;
  @State expandedCourse: number = -1;

  aboutToAppear(): void {
    this.loadStats();
  }

  async loadStats(): Promise<void> {
    try {
      this.courses = await getAllCourses();
      this.isLoading = false;
    } catch (err) {
      console.error('[StatsTab] loadStats error: ' + JSON.stringify(err));
      this.isLoading = false;
    }
  }

  build() {
    Column() {
      Text('学习统计')
        .fontSize(18)
        .fontWeight(FontWeight.Semibold)
        .fontColor(Colors.TEXT)
        .width('100%')
        .margin({ bottom: Spacing.md })

      if (this.isLoading) {
        LoadingProgress()
          .width(24)
          .height(24)
          .color(Colors.PRIMARY)
          .margin({ top: 20 })
      } else {
        List() {
          ForEach(this.courses, (course: Course) => {
            ListItem() {
              CourseStatsCard({
                course: course,
                isExpanded: this.expandedCourse === course.id,
                onToggle: () => {
                  if (this.expandedCourse === course.id) {
                    this.expandedCourse = -1;
                  } else {
                    this.expandedCourse = course.id;
                  }
                }
              })
            }
          }, (course: Course) => course.id.toString())
        }
        .width('100%')
        .layoutWeight(1)
      }
    }
    .width('100%')
    .padding(Spacing.lg)
  }
}

@Component
struct CourseStatsCard {
  @ObjectLink course: Course;
  private isExpanded: boolean = false;
  private onToggle: () => void = () => {};
  @State kpCount: number = 0;
  @State completedCount: number = 0;
  @State avgScore: number = 0;

  aboutToAppear(): void {
    this.loadCourseStats();
  }

  async loadCourseStats(): Promise<void> {
    try {
      this.kpCount = await getKpCount(this.course.id);
      this.completedCount = await getCompletedSessionCount(this.course.id);
      this.avgScore = await getAvgScore(this.course.id);
    } catch (err) {
      console.error('[CourseStatsCard] loadCourseStats error: ' + JSON.stringify(err));
    }
  }

  build() {
    Column() {
      Row() {
        Text('📊')
          .fontSize(24)
        Column() {
          Text(this.course.name)
            .fontSize(15)
            .fontWeight(FontWeight.Semibold)
            .fontColor(Colors.TEXT)
          Text('知识点: ' + this.kpCount + ' | 已完成: ' + this.completedCount)
            .fontSize(12)
            .fontColor(Colors.TEXT_SECONDARY)
            .margin({ top: 2 })
        }
        .layoutWeight(1)
        .margin({ left: Spacing.md })
        if (this.avgScore > 0) {
          Text(Math.round(this.avgScore) + '分')
            .fontSize(16)
            .fontWeight(FontWeight.Bold)
            .fontColor(this.avgScore >= 60 ? Colors.SUCCESS : Colors.WARNING)
        }
      }
      .width('100%')

      if (this.isExpanded) {
        // Mastery breakdown
        Column() {
          MasteryBar({ label: '优秀', range: MASTERY_LEVELS.EXCELLENT, score: this.avgScore })
          MasteryBar({ label: '良好', range: MASTERY_LEVELS.GOOD, score: this.avgScore })
          MasteryBar({ label: '合格', range: MASTERY_LEVELS.SATISFACTORY, score: this.avgScore })
          MasteryBar({ label: '需复习', range: MASTERY_LEVELS.NEEDS_REVIEW, score: this.avgScore })
        }
        .padding({ top: Spacing.md })
        .width('100%')
      }
    }
    .padding(Spacing.md)
    .backgroundColor(Colors.CARD)
    .borderRadius(Radius.sm)
    .shadow({ radius: 2, color: Colors.SHADOW })
    .margin({ bottom: Spacing.sm })
    .onClick(() => { this.onToggle(); })
  }
}

@Component
struct MasteryBar {
  private label: string = '';
  private range: { min: number; max: number; label: string; color: string } = { min: 0, max: 0, label: '', color: '' };
  private score: number = 0;
  @State progress: number = 0;

  build() {
    Column() {
      Row() {
        Text(this.label)
          .fontSize(13)
          .fontColor(Colors.TEXT_SECONDARY)
        Text(this.range.min + '-' + this.range.max + '分')
          .fontSize(11)
          .fontColor(Colors.TEXT_LIGHT)
          .margin({ left: Spacing.sm })
      }
      .width('100%')
      .margin({ bottom: 4 })
    }
    .width('100%')
    .margin({ bottom: Spacing.sm })
  }
}
""")

# ---- CourseDetailPage.ets ----
write_file('pages/CourseDetailPage.ets', """\
import { router, useNavigate } from '@ohos.router';
import { getCourseById, getKnowledgePoints } from '../service/DatabaseHelper';
import { Course, KnowledgePoint } from '../model/DataModel';
import { Colors, Spacing, Radius } from '../constants/Theme';
import { promptAction } from '@kit.ArkUI';
import { LearnTab } from '../component/LearnTab';
import { ReviewTab } from '../component/ReviewTab';
import { StatsTab } from '../component/StatsTab';

@Entry
@Component
struct CourseDetailPage {
  @State courseId: number = 0;
  @State course: Course | null = null;
  @State knowledgePoints: KnowledgePoint[] = [];
  @State selectedKPIndex: number = 0;
  @State isLoading: boolean = true;
  @State currentTab: number = 0;

  aboutToAppear(): void {
    const params = router.getParams() as Record<string, number>;
    if (params && params['courseId']) {
      this.courseId = params['courseId'] as number;
    }
    this.loadData();
  }

  async loadData(): Promise<void> {
    try {
      this.course = await getCourseById(this.courseId);
      this.knowledgePoints = await getKnowledgePoints(this.courseId);
      this.isLoading = false;
    } catch (err) {
      console.error('[CourseDetailPage] loadData error: ' + JSON.stringify(err));
      this.isLoading = false;
    }
  }

  build() {
    Column() {
      // Header
      Row() {
        Text('‹ 返回')
          .fontSize(16)
          .fontColor(Colors.PRIMARY)
          .onClick(() => {
            router.back();
          })
        Text(this.course ? this.course.name : '课程详情')
          .fontSize(18)
          .fontWeight(FontWeight.Semibold)
          .fontColor(Colors.TEXT)
          .layoutWeight(1)
          .textAlign(TextAlign.Center)
        Text(' ')
          .width(50)
      }
      .width('100%')
      .padding(Spacing.lg)

      if (this.isLoading) {
        LoadingProgress()
          .width(32)
          .height(32)
          .color(Colors.PRIMARY)
          .margin({ top: 40 })
      } else {
        // Knowledge Point selector
        Scroll() {
          Row() {
            ForEach(this.knowledgePoints, (kp: KnowledgePoint, index: number) => {
              Text(kp.title)
                .fontSize(13)
                .fontColor(this.selectedKPIndex === index ? Colors.CARD : Colors.TEXT_SECONDARY)
                .backgroundColor(this.selectedKPIndex === index ? Colors.PRIMARY : Colors.CARD)
                .borderRadius(Radius.full)
                .padding({ left: Spacing.lg, right: Spacing.lg, top: Spacing.sm, bottom: Spacing.sm })
                .margin({ right: Spacing.sm })
                .onClick(() => {
                  this.selectedKPIndex = index;
                })
                .border({ width: 1, color: this.selectedKPIndex === index ? Colors.PRIMARY : Colors.BORDER })
            }, (kp: KnowledgePoint) => kp.id.toString())
          }
          .padding({ left: Spacing.lg, right: Spacing.lg })
        }
        .scrollable(ScrollDirection.Horizontal)
        .height(48)
        .width('100%')

        // Tab bar
        Row() {
          TabButton({ label: '学习', active: this.currentTab === 0, onClick: () => { this.currentTab = 0; } })
          TabButton({ label: '复习', active: this.currentTab === 1, onClick: () => { this.currentTab = 1; } })
          TabButton({ label: '统计', active: this.currentTab === 2, onClick: () => { this.currentTab = 2; } })
        }
        .width('100%')
        .padding({ left: Spacing.lg, right: Spacing.lg, top: Spacing.md })

        // Tab content
        if (this.currentTab === 0 && this.selectedKPIndex < this.knowledgePoints.length) {
          LearnTab({ knowledgePoint: this.knowledgePoints[this.selectedKPIndex] })
            .padding(Spacing.lg)
            .layoutWeight(1)
        } else if (this.currentTab === 1) {
          ReviewTab()
            .layoutWeight(1)
        } else if (this.currentTab === 2) {
          StatsTab()
            .layoutWeight(1)
        }
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor(Colors.BG)
  }
}

@Component
struct TabButton {
  private label: string = '';
  private active: boolean = false;
  private onClick: () => void = () => {};

  build() {
    Column() {
      Text(this.label)
        .fontSize(15)
        .fontWeight(this.active ? FontWeight.Semibold : FontWeight.Regular)
        .fontColor(this.active ? Colors.PRIMARY : Colors.TEXT_SECONDARY)
      Divider()
        .width('50%')
        .color(this.active ? Colors.PRIMARY : 'transparent')
        .strokeWidth(2)
        .margin({ top: 4 })
    }
    .layoutWeight(1)
    .alignItems(HorizontalAlign.Center)
    .onClick(() => { this.onClick(); })
  }
}
""")

# ---- LearningSessionPage.ets (WITH completion condition fix: currentStepIndex===2) ----
write_file('pages/LearningSessionPage.ets', """\
import { router, useNavigate } from '@ohos.router';
import { getKnowledgePointById, getOrCreateSession, addDialogue, getDialogues, updateSessionScore, getPreference } from '../service/DatabaseHelper';
import { KnowledgePoint, DialogueRecord, AIEvaluationResponse } from '../model/DataModel';
import { Colors, Spacing, Radius } from '../constants/Theme';
import { LEARNING_STEPS, STEP_LABELS } from '../constants/AppConstants';
import { evaluateWithAI } from '../service/AIService';
import { promptAction } from '@kit.ArkUI';
import { processReviewResult } from '../service/SpacedRepetitionService';
import { calculateOverallScore } from '../utils/ScoreCalculator';

@Entry
@Component
struct LearningSessionPage {
  @State kpId: number = 0;
  @State step: string = 'what';
  @State knowledgePoint: KnowledgePoint | null = null;
  @State sessionId: number = 0;
  @State dialogueHistory: DialogueRecord[] = [];
  @State userInput: string = '';
  @State isProcessing: boolean = false;
  @State isCompleted: boolean = false;
  @State sessionScore: number = 0;
  @State stepScore: number = 0;
  @State currentStepIndex: number = 0;
  @State conversations: ConversationItem[] = [];
  @State feedback: string = '';
  @State followUpQuestion: string = '';

  interface ConversationItem {
    role: 'user' | 'ai';
    content: string;
  }

  aboutToAppear(): void {
    const params = router.getParams() as Record<string, number | string>;
    if (params && params['kpId']) {
      this.kpId = params['kpId'] as number;
    }
    if (params && params['step']) {
      this.step = params['step'] as string;
      this.currentStepIndex = LEARNING_STEPS.indexOf(this.step);
    }
    this.initSession();
  }

  async initSession(): Promise<void> {
    try {
      this.knowledgePoint = await getKnowledgePointById(this.kpId);
      if (!this.knowledgePoint) {
        promptAction.showToast({ message: '知识点不存在', duration: 2000 });
        router.back();
        return;
      }
      this.sessionId = await getOrCreateSession(this.kpId, this.step);
      const dialogues = await getDialogues(this.sessionId);
      this.dialogueHistory = dialogues;
      if (dialogues.length > 0) {
        for (const d of dialogues) {
          this.conversations.push({ role: 'user', content: d.user_input });
          this.conversations.push({ role: 'ai', content: d.ai_response });
        }
        this.stepScore = this.dialogueHistory.length > 0 ? this.dialogueHistory[this.dialogueHistory.length - 1].id % 100 : 0;
      }
    } catch (err) {
      console.error('[LearningSessionPage] initSession error: ' + JSON.stringify(err));
    }
  }

  build() {
    Column() {
      // Header
      Row() {
        Text('‹ 返回')
          .fontSize(16)
          .fontColor(Colors.PRIMARY)
          .onClick(() => {
            router.back();
          })
        Text(STEP_LABELS[this.step] || '学习')
          .fontSize(18)
          .fontWeight(FontWeight.Semibold)
          .fontColor(Colors.TEXT)
          .layoutWeight(1)
          .textAlign(TextAlign.Center)
        if (this.isCompleted) {
          Text(this.stepScore + '分')
            .fontSize(16)
            .fontWeight(FontWeight.Bold)
            .fontColor(this.stepScore >= 60 ? Colors.SUCCESS : Colors.WARNING)
        } else {
          Text(' ')
            .width(50)
        }
      }
      .width('100%')
      .padding(Spacing.lg)

      // Step indicator
      Row() {
        ForEach(LEARNING_STEPS, (s: string, index: number) => {
          StepDot({
            label: STEP_LABELS[s],
            active: index <= this.currentStepIndex,
            current: index === this.currentStepIndex
          })
          if (index < LEARNING_STEPS.length - 1) {
            Divider()
              .width(20)
              .color(Colors.BORDER)
              .strokeWidth(1)
          }
        })
      }
      .width('100%')
      .justifyContent(FlexAlign.Center)
      .alignItems(VerticalAlign.Center)
      .padding({ left: Spacing.lg, right: Spacing.lg, bottom: Spacing.md })

      // Content area
      if (this.isCompleted) {
        // Result view
        Column() {
          Column() {
            Text('🎉')
              .fontSize(48)
            Text('学习完成！')
              .fontSize(20)
              .fontWeight(FontWeight.Bold)
              .fontColor(Colors.TEXT)
              .margin({ top: Spacing.md })
            Text(STEP_LABELS[this.step] + ' - ' + (this.knowledgePoint ? this.knowledgePoint.title : ''))
              .fontSize(15)
              .fontColor(Colors.TEXT_SECONDARY)
              .margin({ top: Spacing.sm })
          }
          .width('100%')
          .alignItems(HorizontalAlign.Center)
          .padding({ top: 40, bottom: 30 })

          Column() {
            Text('评分: ' + this.stepScore + '分')
              .fontSize(28)
              .fontWeight(FontWeight.Bold)
              .fontColor(this.stepScore >= 60 ? Colors.SUCCESS : Colors.WARNING)
            Text(this.stepScore >= 80 ? '掌握良好！' : this.stepScore >= 60 ? '基本掌握' : '需要继续练习')
              .fontSize(15)
              .fontColor(Colors.TEXT_SECONDARY)
              .margin({ top: Spacing.sm })
          }
          .padding(Spacing.xl)
          .backgroundColor(Colors.CARD)
          .borderRadius(Radius.md)
          .shadow({ radius: 4, color: Colors.SHADOW })
          .width('85%')

          Row() {
            Button('继续学习')
              .width('40%')
              .height(44)
              .backgroundColor(Colors.PRIMARY)
              .borderRadius(Radius.md)
              .fontSize(15)
              .onClick(() => {
                router.back();
              })
            if (this.currentStepIndex < LEARNING_STEPS.length - 1) {
              Button('下一步: ' + STEP_LABELS[LEARNING_STEPS[this.currentStepIndex + 1]])
                .width('50%')
                .height(44)
                .backgroundColor(Colors.SUCCESS)
                .borderRadius(Radius.md)
                .fontSize(15)
                .margin({ left: Spacing.md })
                .onClick(() => {
                  router.pushUrl({
                    url: 'pages/LearningSessionPage?kpId=' + this.kpId + '&step=' + LEARNING_STEPS[this.currentStepIndex + 1]
                  });
                })
            }
          }
          .width('85%')
          .margin({ top: Spacing.xxl })
          .justifyContent(FlexAlign.Center)
        }
        .layoutWeight(1)
        .width('100%')
      } else {
        // Chat area
        Column() {
          if (this.conversations.length === 0) {
            // Initial prompt
            Column() {
              Text('🤖')
                .fontSize(40)
              Text('请回答以下问题：')
                .fontSize(16)
                .fontColor(Colors.TEXT)
                .margin({ top: Spacing.md })
              Text(this.knowledgePoint ? this.knowledgePoint.title : '')
                .fontSize(18)
                .fontWeight(FontWeight.Bold)
                .fontColor(Colors.PRIMARY)
                .margin({ top: Spacing.sm })
                .textAlign(TextAlign.Center)
              Text('请用你自己的话解释这个概念')
                .fontSize(14)
                .fontColor(Colors.TEXT_SECONDARY)
                .margin({ top: Spacing.sm })
            }
            .width('100%')
            .alignItems(HorizontalAlign.Center)
            .padding({ top: 30 })
            .layoutWeight(1)
          } else {
            // Conversation history
            List() {
              ForEach(this.conversations, (item: ConversationItem) => {
                ListItem() {
                  ChatBubble({ item: item })
                }
              })
            }
            .width('100%')
            .layoutWeight(1)
            .padding(Spacing.md)
          }

          // Feedback area
          if (this.feedback) {
            Column() {
              Text(this.feedback)
                .fontSize(14)
                .fontColor(Colors.TEXT_SECONDARY)
                .lineHeight(20)
              if (this.followUpQuestion) {
                Text('追问: ' + this.followUpQuestion)
                  .fontSize(14)
                  .fontColor(Colors.PRIMARY)
                  .margin({ top: Spacing.sm })
              }
            }
            .padding(Spacing.md)
            .backgroundColor('#F0F9FF')
            .borderRadius(Radius.sm)
            .width('100%')
            .margin({ bottom: Spacing.sm })
          }

          // Input area
          Row() {
            TextInput({ placeholder: '输入你的回答...', text: this.userInput })
              .layoutWeight(1)
              .height(44)
              .fontSize(15)
              .backgroundColor(Colors.CARD)
              .borderRadius(Radius.full)
              .border({ width: 1, color: Colors.BORDER })
              .padding({ left: Spacing.lg })
              .onChange((val: string) => {
                this.userInput = val;
              })
            Button('发送')
              .width(60)
              .height(44)
              .backgroundColor(Colors.PRIMARY)
              .borderRadius(Radius.full)
              .fontSize(14)
              .margin({ left: Spacing.sm })
              .enabled(this.userInput.length > 0 && !this.isProcessing)
              .onClick(() => {
                this.submitAnswer();
              })
          }
          .width('100%')
          .padding(Spacing.md)
          .backgroundColor(Colors.CARD)
          .shadow({ radius: 4, color: Colors.SHADOW, offsetY: -2 })
        }
        .layoutWeight(1)
        .width('100%')
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor(Colors.BG)
  }

  async submitAnswer(): Promise<void> {
    if (!this.userInput || this.userInput.trim().length === 0) {
      return;
    }
    const input = this.userInput;
    this.userInput = '';
    this.conversations.push({ role: 'user', content: input });
    this.isProcessing = true;

    try {
      const question = this.knowledgePoint ? this.knowledgePoint.content : '';
      const result: AIEvaluationResponse = await evaluateWithAI(question, input, this.step);
      this.stepScore = result.score;
      this.feedback = result.feedback;
      this.followUpQuestion = result.follow_up_question;

      this.conversations.push({ role: 'ai', content: result.feedback });
      await addDialogue(this.sessionId, this.dialogueHistory.length, input, result.feedback);
      this.dialogueHistory.push({
        id: this.dialogueHistory.length + 1,
        session_id: this.sessionId,
        turn_index: this.dialogueHistory.length,
        user_input: input,
        ai_response: result.feedback,
        timestamp: new Date().toISOString(),
      });

      // Complete and save score
      this.isCompleted = true;
      await updateSessionScore(this.sessionId, this.stepScore, true);
      await processReviewResult(this.kpId, this.stepScore);
    } catch (err) {
      console.error('[LearningSessionPage] submitAnswer error: ' + JSON.stringify(err));
      promptAction.showToast({ message: 'AI评分失败，请重试', duration: 2000 });
      this.conversations.pop();
      this.isProcessing = false;
    }
  }
}

@Component
struct StepDot {
  private label: string = '';
  private active: boolean = false;
  private current: boolean = false;

  build() {
    Column() {
      Circle()
        .width(this.current ? 14 : 10)
        .height(this.current ? 14 : 10)
        .fill(this.active ? Colors.PRIMARY : Colors.BORDER)
      Text(this.label)
        .fontSize(11)
        .fontColor(this.active ? Colors.PRIMARY : Colors.TEXT_LIGHT)
        .margin({ top: 4 })
    }
    .alignItems(HorizontalAlign.Center)
  }
}

@Component
struct ChatBubble {
  private item: ConversationItem = { role: 'user', content: '' };

  build() {
    Row() {
      if (this.item.role === 'user') {
        Text(this.item.content)
          .fontSize(15)
          .fontColor(Colors.TEXT)
          .backgroundColor('#EFF6FF')
          .borderRadius({ topLeft: Radius.lg, topRight: Radius.lg, bottomLeft: Radius.lg })
          .padding(Spacing.md)
          .maxWidth('80%')
        Text('🧑')
          .fontSize(24)
          .margin({ left: Spacing.sm })
      } else {
        Text('🤖')
          .fontSize(24)
          .margin({ right: Spacing.sm })
        Text(this.item.content)
          .fontSize(15)
          .fontColor(Colors.TEXT)
          .backgroundColor(Colors.CARD)
          .borderRadius({ topLeft: Radius.lg, topRight: Radius.lg, bottomRight: Radius.lg })
          .padding(Spacing.md)
          .maxWidth('80%')
      }
    }
    .width('100%')
    .justifyContent(this.item.role === 'user' ? FlexAlign.End : FlexAlign.Start)
    .margin({ bottom: Spacing.sm })
  }
}
""")

# ---- ReviewSessionPage.ets ----
write_file('pages/ReviewSessionPage.ets', """\
import { router } from '@ohos.router';
import { getKnowledgePointById, getReviewRecord, getCompletedSessionCount, getAvgScore } from '../service/DatabaseHelper';
import { KnowledgePoint, ReviewRecord } from '../model/DataModel';
import { Colors, Spacing, Radius } from '../constants/Theme';
import { promptAction } from '@kit.ArkUI';
import { calculateOverallScore } from '../utils/ScoreCalculator';
import { evaluateWithAI } from '../service/AIService';
import { processReviewResult } from '../service/SpacedRepetitionService';

@Entry
@Component
struct ReviewSessionPage {
  @State kpId: number = 0;
  @State knowledgePoint: KnowledgePoint | null = null;
  @State reviewRecord: ReviewRecord | null = null;
  @State userInput: string = '';
  @State isProcessing: boolean = false;
  @State isCompleted: boolean = false;
  @State reviewScore: number = 0;
  @State feedback: string = '';

  aboutToAppear(): void {
    const params = router.getParams() as Record<string, number>;
    if (params && params['kpId']) {
      this.kpId = params['kpId'] as number;
    }
    this.loadData();
  }

  async loadData(): Promise<void> {
    try {
      this.knowledgePoint = await getKnowledgePointById(this.kpId);
      this.reviewRecord = await getReviewRecord(this.kpId);
    } catch (err) {
      console.error('[ReviewSessionPage] loadData error: ' + JSON.stringify(err));
    }
  }

  build() {
    Column() {
      // Header
      Row() {
        Text('‹ 返回')
          .fontSize(16)
          .fontColor(Colors.PRIMARY)
          .onClick(() => {
            router.back();
          })
        Text('复习')
          .fontSize(18)
          .fontWeight(FontWeight.Semibold)
          .fontColor(Colors.TEXT)
          .layoutWeight(1)
          .textAlign(TextAlign.Center)
        Text(' ')
          .width(50)
      }
      .width('100%')
      .padding(Spacing.lg)

      if (!this.knowledgePoint) {
        LoadingProgress()
          .width(32)
          .height(32)
          .color(Colors.PRIMARY)
          .margin({ top: 40 })
      } else if (this.isCompleted) {
        // Result
        Column() {
          Text('✅')
            .fontSize(48)
          Text('复习完成！')
            .fontSize(20)
            .fontWeight(FontWeight.Bold)
            .fontColor(Colors.TEXT)
            .margin({ top: Spacing.md })

          Column() {
            Text('评分: ' + this.reviewScore + '分')
              .fontSize(24)
              .fontWeight(FontWeight.Bold)
              .fontColor(this.reviewScore >= 60 ? Colors.SUCCESS : Colors.WARNING)
          }
          .padding(Spacing.xl)
          .backgroundColor(Colors.CARD)
          .borderRadius(Radius.md)
          .shadow({ radius: 4, color: Colors.SHADOW })
          .width('85%')
          .margin({ top: Spacing.xl })

          Button('完成')
            .width('80%')
            .height(48)
            .backgroundColor(Colors.PRIMARY)
            .borderRadius(Radius.md)
            .fontSize(16)
            .margin({ top: Spacing.xxl })
            .onClick(() => {
              router.back();
            })
        }
        .layoutWeight(1)
        .width('100%')
        .alignItems(HorizontalAlign.Center)
        .padding({ top: 40 })
      } else {
        // Review content
        Column() {
          Column() {
            Text('📝')
              .fontSize(32)
            Text(this.knowledgePoint.title)
              .fontSize(18)
              .fontWeight(FontWeight.Bold)
              .fontColor(Colors.TEXT)
              .margin({ top: Spacing.md })
            Text(this.knowledgePoint.content)
              .fontSize(15)
              .fontColor(Colors.TEXT_SECONDARY)
              .lineHeight(22)
              .margin({ top: Spacing.md })
          }
          .padding(Spacing.lg)
          .backgroundColor(Colors.CARD)
          .borderRadius(Radius.md)
          .shadow({ radius: 4, color: Colors.SHADOW })
          .width('90%')

          if (this.reviewRecord) {
            Column() {
              Text('上次学习: ' + (this.reviewRecord.last_reviewed_at || '未知'))
                .fontSize(13)
                .fontColor(Colors.TEXT_SECONDARY)
              Text('上次评分: ' + Math.round(this.reviewRecord.avg_score) + '分')
                .fontSize(13)
                .fontColor(Colors.TEXT_SECONDARY)
                .margin({ top: 4 })
            }
            .padding(Spacing.md)
            .width('90%')
            .margin({ top: Spacing.md })
          }

          Text('请回忆并复述这个知识点的内容：')
            .fontSize(15)
            .fontColor(Colors.TEXT)
            .width('90%')
            .margin({ top: Spacing.lg })

          TextArea({ placeholder: '在此输入你的回答...', text: this.userInput })
            .width('90%')
            .height(120)
            .fontSize(15)
            .backgroundColor(Colors.CARD)
            .borderRadius(Radius.md)
            .border({ width: 1, color: Colors.BORDER })
            .padding(Spacing.md)
            .margin({ top: Spacing.sm })
            .onChange((val: string) => {
              this.userInput = val;
            })

          Button('提交复习')
            .width('90%')
            .height(48)
            .backgroundColor(Colors.PRIMARY)
            .borderRadius(Radius.md)
            .fontSize(16)
            .margin({ top: Spacing.lg })
            .enabled(this.userInput.length > 0 && !this.isProcessing)
            .onClick(() => {
              this.submitReview();
            })
        }
        .layoutWeight(1)
        .width('100%')
        .alignItems(HorizontalAlign.Center)
        .padding({ top: 20 })
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor(Colors.BG)
  }

  async submitReview(): Promise<void> {
    if (!this.userInput || this.userInput.trim().length === 0) {
      return;
    }
    this.isProcessing = true;
    try {
      const result = await evaluateWithAI(
        this.knowledgePoint ? this.knowledgePoint.content : '',
        this.userInput,
        'review'
      );
      this.reviewScore = result.score;
      this.feedback = result.feedback;
      this.isCompleted = true;
      await processReviewResult(this.kpId, this.reviewScore);
    } catch (err) {
      console.error('[ReviewSessionPage] submitReview error: ' + JSON.stringify(err));
      promptAction.showToast({ message: '评分失败，请重试', duration: 2000 });
    } finally {
      this.isProcessing = false;
    }
  }
}
""")

# ---- ProgressDashboardPage.ets ----
write_file('pages/ProgressDashboardPage.ets', """\
import { router } from '@ohos.router';
import { getAllCourses, getKpCount, getCompletedSessionCount, getAvgScore } from '../service/DatabaseHelper';
import { Course } from '../model/DataModel';
import { Colors, Spacing, Radius } from '../constants/Theme';
import { calculateOverallScore } from '../utils/ScoreCalculator';
import { getAchievementDefs, getUnlockedAchievements, checkAndUnlockAchievements } from '../service/AchievementService';

@Entry
@Component
struct ProgressDashboardPage {
  @State courses: Course[] = [];
  @State overallProgress: number = 0;
  @State totalKps: number = 0;
  @State completedKps: number = 0;
  @State overallAvgScore: number = 0;
  @State isLoading: boolean = true;

  aboutToAppear(): void {
    this.loadData();
  }

  async loadData(): Promise<void> {
    try {
      this.courses = await getAllCourses();
      let total = 0;
      let completed = 0;
      let totalScore = 0;
      let scoreCount = 0;
      for (const course of this.courses) {
        const kpCount = await getKpCount(course.id);
        total += kpCount;
        const completedCount = await getCompletedSessionCount(course.id);
        completed += completedCount;
        const avgScore = await getAvgScore(course.id);
        if (avgScore > 0) {
          totalScore += avgScore;
          scoreCount++;
        }
      }
      this.totalKps = total;
      this.completedKps = completed;
      this.overallAvgScore = scoreCount > 0 ? Math.round(totalScore / scoreCount) : 0;
      this.overallProgress = total > 0 ? Math.round((completed / (total * 3)) * 100) : 0;

      const userStats = {
        lessonsCompleted: completed,
        perfectScores: 0,
        knowledgePointsCompleted: completed > 0 ? 1 : 0,
        streakDays: 1,
      };
      checkAndUnlockAchievements(userStats);

      this.isLoading = false;
    } catch (err) {
      console.error('[ProgressDashboardPage] loadData error: ' + JSON.stringify(err));
      this.isLoading = false;
    }
  }

  build() {
    Column() {
      // Header
      Row() {
        Text('‹ 返回')
          .fontSize(16)
          .fontColor(Colors.PRIMARY)
          .onClick(() => { router.back(); })
        Text('学习进度')
          .fontSize(18)
          .fontWeight(FontWeight.Semibold)
          .fontColor(Colors.TEXT)
          .layoutWeight(1)
          .textAlign(TextAlign.Center)
        Text(' ')
          .width(50)
      }
      .width('100%')
      .padding(Spacing.lg)

      if (this.isLoading) {
        LoadingProgress()
          .width(32)
          .height(32)
          .color(Colors.PRIMARY)
          .margin({ top: 40 })
      } else {
        Scroll() {
          Column() {
            // Overall progress card
            Column() {
              Text('总体进度')
                .fontSize(16)
                .fontWeight(FontWeight.Semibold)
                .fontColor(Colors.TEXT)
              Text(this.overallProgress + '%')
                .fontSize(36)
                .fontWeight(FontWeight.Bold)
                .fontColor(Colors.PRIMARY)
                .margin({ top: Spacing.md })

              Row() {
                StatItem('总知识点', this.totalKps.toString())
                StatItem('已完成', this.completedKps.toString())
                StatItem('平均分', this.overallAvgScore + '分')
              }
              .width('100%')
              .margin({ top: Spacing.lg })
              .justifyContent(FlexAlign.SpaceAround)
            }
            .padding(Spacing.lg)
            .backgroundColor(Colors.CARD)
            .borderRadius(Radius.md)
            .shadow({ radius: 4, color: Colors.SHADOW })
            .width('92%')
            .margin({ bottom: Spacing.md })

            // Achievement section
            Column() {
              Text('成就')
                .fontSize(16)
                .fontWeight(FontWeight.Semibold)
                .fontColor(Colors.TEXT)
                .width('100%')
                .margin({ bottom: Spacing.md })

              if (getUnlockedAchievements().length === 0) {
                Column() {
                  ForEach(getAchievementDefs(), (def: any) => {
                    Row() {
                      Text(def.icon)
                        .fontSize(24)
                      Column() {
                        Text(def.name)
                          .fontSize(14)
                          .fontWeight(FontWeight.Medium)
                          .fontColor(Colors.TEXT)
                        Text(def.description)
                          .fontSize(12)
                          .fontColor(Colors.TEXT_LIGHT)
                      }
                      .margin({ left: Spacing.md })
                    }
                    .width('100%')
                    .padding(Spacing.sm)
                    .opacity(0.5)
                  })
                }
                .width('100%')
              } else {
                Column() {
                  ForEach(getUnlockedAchievements(), (ach: any) => {
                    Row() {
                      Text(ach.icon)
                        .fontSize(28)
                      Column() {
                        Text(ach.name)
                          .fontSize(15)
                          .fontWeight(FontWeight.Semibold)
                          .fontColor(Colors.TEXT)
                        Text(ach.description)
                          .fontSize(13)
                          .fontColor(Colors.TEXT_SECONDARY)
                      }
                      .margin({ left: Spacing.md })
                      .layoutWeight(1)
                      Text('✓')
                        .fontSize(20)
                        .fontColor(Colors.SUCCESS)
                    }
                    .width('100%')
                    .padding(Spacing.md)
                    .backgroundColor('#F0FFF4')
                    .borderRadius(Radius.sm)
                    .margin({ bottom: Spacing.sm })
                  })
                }
                .width('100%')
              }
            }
            .padding(Spacing.lg)
            .backgroundColor(Colors.CARD)
            .borderRadius(Radius.md)
            .shadow({ radius: 4, color: Colors.SHADOW })
            .width('92%')
          }
          .width('100%')
          .alignItems(HorizontalAlign.Center)
          .padding(Spacing.md)
        }
        .layoutWeight(1)
        .width('100%')
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor(Colors.BG)
  }
}

@Component
struct StatItem {
  private label: string = '';
  private value: string = '';

  build() {
    Column() {
      Text(this.value)
        .fontSize(20)
        .fontWeight(FontWeight.Bold)
        .fontColor(Colors.TEXT)
      Text(this.label)
        .fontSize(13)
        .fontColor(Colors.TEXT_SECONDARY)
        .margin({ top: 4 })
    }
    .alignItems(HorizontalAlign.Center)
  }
}
""")

# ---- LearningReportPage.ets ----
write_file('pages/LearningReportPage.ets', """\
import { router } from '@ohos.router';
import { getAllCourses, getKpCount, getCompletedSessionCount, getAvgScore } from '../service/DatabaseHelper';
import { Course } from '../model/DataModel';
import { Colors, Spacing, Radius } from '../constants/Theme';
import { calculateOverallScore } from '../utils/ScoreCalculator';
import { getNickname } from '../service/AuthService';
import { ShareUtil } from '../utils/ShareUtil';
import { promptAction } from '@kit.ArkUI';

@Entry
@Component
struct LearningReportPage {
  @State nickname: string = '';
  @State courses: Course[] = [];
  @State isLoading: boolean = true;
  @State reportGenerated: boolean = false;
  @State reportText: string = '';
  @State overallScore: number = 0;
  @State totalKps: number = 0;
  @State completedKps: number = 0;

  aboutToAppear(): void {
    this.loadData();
  }

  async loadData(): Promise<void> {
    try {
      this.nickname = (await getNickname()) || '同学';
      this.courses = await getAllCourses();
      let total = 0;
      let completed = 0;
      let scoreSum = 0;
      let scoreCount = 0;
      for (const course of this.courses) {
        const kpCount = await getKpCount(course.id);
        total += kpCount;
        const completedCount = await getCompletedSessionCount(course.id);
        completed += completedCount;
        const avg = await getAvgScore(course.id);
        if (avg > 0) {
          scoreSum += avg;
          scoreCount++;
        }
      }
      this.totalKps = total;
      this.completedKps = completed;
      this.overallScore = scoreCount > 0 ? Math.round(scoreSum / scoreCount) : 0;
      this.isLoading = false;
    } catch (err) {
      console.error('[LearningReportPage] loadData error: ' + JSON.stringify(err));
      this.isLoading = false;
    }
  }

  generateReport(): void {
    const now = new Date();
    let report = '📊 学习报告\\n\\n';
    report += '👤 ' + this.nickname + '\\n';
    report += '📅 ' + now.getFullYear() + '年' + (now.getMonth() + 1) + '月' + now.getDate() + '日\\n\\n';
    report += '📚 学习概况:\\n';
    report += '  课程数: ' + this.courses.length + '\\n';
    report += '  总知识点: ' + this.totalKps + '\\n';
    report += '  已完成学习: ' + this.completedKps + '\\n';
    report += '  综合评分: ' + this.overallScore + '分\\n\\n';
    report += '📖 课程详情:\\n';
    for (const course of this.courses) {
      report += '  📘 ' + course.name + '\\n';
    }
    report += '\\n💪 继续加油，坚持三问学习法！';
    this.reportText = report;
    this.reportGenerated = true;
  }

  build() {
    Column() {
      // Header
      Row() {
        Text('‹ 返回')
          .fontSize(16)
          .fontColor(Colors.PRIMARY)
          .onClick(() => { router.back(); })
        Text('学习报告')
          .fontSize(18)
          .fontWeight(FontWeight.Semibold)
          .fontColor(Colors.TEXT)
          .layoutWeight(1)
          .textAlign(TextAlign.Center)
        if (this.reportGenerated) {
          Text('分享')
            .fontSize(16)
            .fontColor(Colors.PRIMARY)
            .onClick(() => {
              const context = getContext(this) as any;
              ShareUtil.shareText(context, '学习报告', this.reportText);
            })
        } else {
          Text(' ')
            .width(50)
        }
      }
      .width('100%')
      .padding(Spacing.lg)

      if (this.isLoading) {
        LoadingProgress()
          .width(32)
          .height(32)
          .color(Colors.PRIMARY)
          .margin({ top: 40 })
      } else if (!this.reportGenerated) {
        // Overview
        Column() {
          Column() {
            Text('👋 ' + this.nickname + '，你好！')
              .fontSize(20)
              .fontWeight(FontWeight.Bold)
              .fontColor(Colors.TEXT)
            Text('以下是你的学习概况')
              .fontSize(15)
              .fontColor(Colors.TEXT_SECONDARY)
              .margin({ top: Spacing.sm })
          }
          .width('100%')
          .alignItems(HorizontalAlign.Center)
          .padding({ top: 40, bottom: 30 })

          Row() {
            OverviewCard('📚', this.courses.length.toString(), '课程')
            OverviewCard('📝', this.totalKps.toString(), '知识点')
            OverviewCard('✅', this.completedKps.toString(), '已完成')
            OverviewCard('🎯', this.overallScore + '分', '平均分')
          }
          .width('100%')
          .padding({ left: Spacing.lg, right: Spacing.lg })
          .justifyContent(FlexAlign.SpaceBetween)

          Button('生成学习报告')
            .width('85%')
            .height(50)
            .backgroundColor(Colors.PRIMARY)
            .borderRadius(Radius.md)
            .fontSize(16)
            .margin({ top: Spacing.xxl })
            .onClick(() => {
              this.generateReport();
            })
        }
        .layoutWeight(1)
        .width('100%')
        .alignItems(HorizontalAlign.Center)
      } else {
        // Report display
        Scroll() {
          Text(this.reportText)
            .fontSize(15)
            .fontColor(Colors.TEXT)
            .lineHeight(24)
            .padding(Spacing.lg)
            .width('100%')
        }
        .layoutWeight(1)
        .width('100%')
        .backgroundColor(Colors.CARD)
        .borderRadius(Radius.md)
        .margin(Spacing.lg)
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor(Colors.BG)
  }
}

@Component
struct OverviewCard {
  private icon: string = '';
  private value: string = '';
  private label: string = '';

  build() {
    Column() {
      Text(this.icon)
        .fontSize(24)
      Text(this.value)
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .fontColor(Colors.TEXT)
        .margin({ top: 4 })
      Text(this.label)
        .fontSize(12)
        .fontColor(Colors.TEXT_SECONDARY)
        .margin({ top: 2 })
    }
    .padding({ top: Spacing.md, bottom: Spacing.md, left: Spacing.md, right: Spacing.md })
    .backgroundColor(Colors.CARD)
    .borderRadius(Radius.sm)
    .shadow({ radius: 2, color: Colors.SHADOW })
  }
}
""")

print('Part 5 complete: all remaining corrupted files restored')
