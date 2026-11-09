import router from '@ohos.router';
import { getKnowledgePointById, getOrCreateSession, addDialogue, getDialogues, updateSessionScore } from '../service/DatabaseHelper';
import { KnowledgePoint, DialogueRecord } from '../model/DataModel';
import { Colors, Spacing, Radius } from '../constants/Theme';
import { LEARNING_STEPS, STEP_LABELS } from '../constants/AppConstants';
import { evaluateWithAI } from '../service/AIService';
import { promptAction } from '@kit.ArkUI';
import { processReviewResult } from '../service/SpacedRepetitionService';

interface ConversationItem {
  role: 'user' | 'ai';
  content: string;
}

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
  @State stepLabels: string[] = ['是什么', '为什么', '怎么用'];
  @State stepNames: string[] = ['what', 'why', 'how'];
  @State initialPrompt: string = '请回答以下问题：';

  aboutToAppear(): void {
    const params = router.getParams() as Record<string, Object>;
    if (params !== null) {
      const kpIdParam = params['kpId'];
      if (kpIdParam !== undefined) {
        this.kpId = kpIdParam as number;
      }
      const stepParam = params['step'];
      if (stepParam !== undefined) {
        this.step = stepParam as string;
        this.currentStepIndex = this.step === 'what' ? 0 : this.step === 'why' ? 1 : 2;
      }
    }
    this.initSession();
  }

  getNextStepName(): string {
    const nextIdx = this.currentStepIndex + 1;
    if (nextIdx >= 3) return 'how';
    return ['what', 'why', 'how'][nextIdx];
  }

  getStepLabel(): string {
    if (this.step === 'what') return '是什么';
    if (this.step === 'why') return '为什么';
    if (this.step === 'how') return '怎么用';
    return '学习';
  }

  getNextStepLabel(): string {
    const nextIdx = this.currentStepIndex + 1;
    if (nextIdx >= 3) return '';
    const steps = ['是什么', '为什么', '怎么用'];
    return steps[nextIdx];
  }

  async initSession(): Promise<void> {
    try {
      this.knowledgePoint = await getKnowledgePointById(this.kpId);
      if (this.knowledgePoint === null) {
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
      }
      if (this.step === 'what') {
        this.initialPrompt = '请用你自己的话解释这个概念是什么';
      } else if (this.step === 'why') {
        this.initialPrompt = '请解释为什么这个概念是这样，背后的原理是什么';
      } else {
        this.initialPrompt = '请说明这个概念在实际中怎么应用';
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
        Text(this.getStepLabel())
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
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
        ForEach(LEARNING_STEPS, (stepName: string, index: number) => {
          StepDot({
            label: stepName === 'what' ? STEP_LABELS.what : stepName === 'why' ? STEP_LABELS.why : STEP_LABELS.how,
            isActive: index <= this.currentStepIndex,
            isCurrent: index === this.currentStepIndex
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
            Text(this.getStepLabel())
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
            Button('返回课程')
              .width('40%')
              .height(44)
              .backgroundColor(Colors.PRIMARY)
              .borderRadius(Radius.md)
              .fontSize(15)
              .onClick(() => {
                router.back();
              })
            if (this.currentStepIndex < LEARNING_STEPS.length - 1) {
              Button('下一步: ' + this.getNextStepLabel())
                .width('50%')
                .height(44)
                .backgroundColor(Colors.SUCCESS)
                .borderRadius(Radius.md)
                .fontSize(15)
                .margin({ left: Spacing.md })
                .onClick(() => {
                  router.pushUrl({
                    url: 'pages/LearningSessionPage?kpId=' + this.kpId + '&step='
                      + this.getNextStepName()
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
        Column() {
          if (this.conversations.length === 0) {
            Column() {
              Text('🤖')
                .fontSize(40)
              Text(this.initialPrompt)
                .fontSize(16)
                .fontColor(Colors.TEXT)
                .margin({ top: Spacing.md })
              if (this.knowledgePoint !== null) {
                Text(this.knowledgePoint.title)
                  .fontSize(18)
                  .fontWeight(FontWeight.Bold)
                  .fontColor(Colors.PRIMARY)
                  .margin({ top: Spacing.sm })
                  .textAlign(TextAlign.Center)
              }
            }
            .width('100%')
            .alignItems(HorizontalAlign.Center)
            .padding({ top: 30 })
            .layoutWeight(1)
          } else {
            List({ space: 8 }) {
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

          if (this.feedback.length > 0) {
            Column() {
              Text(this.feedback)
                .fontSize(14)
                .fontColor(Colors.TEXT_SECONDARY)
                .lineHeight(20)
              if (this.followUpQuestion.length > 0) {
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
    if (this.userInput === null || this.userInput.trim().length === 0) {
      return;
    }
    const input = this.userInput;
    this.userInput = '';
    this.conversations.push({ role: 'user', content: input });
    this.isProcessing = true;

    try {
      const question = this.knowledgePoint !== null ? this.knowledgePoint.content : '';
      const result = await evaluateWithAI(question, input, this.step);
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
  label: string = '';
  isActive: boolean = false;
  isCurrent: boolean = false;

  build() {
    Column() {
      Circle()
        .width(this.isCurrent ? 14 : 10)
        .height(this.isCurrent ? 14 : 10)
        .fill(this.isActive ? Colors.PRIMARY : Colors.BORDER)
      Text(this.label)
        .fontSize(11)
        .fontColor(this.isActive ? Colors.PRIMARY : Colors.TEXT_LIGHT)
        .margin({ top: 4 })
    }
    .alignItems(HorizontalAlign.Center)
  }
}

@Component
struct ChatBubble {
  item: ConversationItem = { role: 'user', content: '' };

  build() {
    Row() {
      if (this.item.role === 'user') {
        Text(this.item.content)
          .fontSize(15)
          .fontColor(Colors.TEXT)
          .backgroundColor('#EFF6FF')
          .borderRadius({ topLeft: Radius.lg, topRight: Radius.lg, bottomLeft: Radius.lg })
          .padding(Spacing.md)
          .width('80%')
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
          .width('80%')
      }
    }
    .width('100%')
    .justifyContent(this.item.role === 'user' ? FlexAlign.End : FlexAlign.Start)
    .margin({ bottom: Spacing.sm })
  }
}
