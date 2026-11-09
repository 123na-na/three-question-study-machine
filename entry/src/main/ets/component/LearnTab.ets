import { KnowledgePoint } from '../model/DataModel';

import { Colors, Spacing, Radius } from '../constants/Theme';

import { STEP_LABELS } from '../constants/AppConstants';

import { ScoreCalculator } from '../utils/ScoreCalculator';

import { getSessionByKpAndStep, getInProgressSessionsByKP } from '../service/DatabaseHelper';

import router from '@ohos.router';



@Component

export struct LearnTab {

  @Prop knowledgePoint: KnowledgePoint;

  @State whatScore: number = 0;

  @State whyScore: number = 0;

  @State howScore: number = 0;

  @State whatStatus: string = '未开始';

  @State whyStatus: string = '未开始';

  @State howStatus: string = '未开始';

  @State overallScore: number = 0;

  @State isLoading: boolean = true;



  aboutToAppear(): void {

    this.loadScores();

  }



  async loadScores(): Promise<void> {
    try {
      const whatSession = await getSessionByKpAndStep(this.knowledgePoint.id, 'what');
      const whySession = await getSessionByKpAndStep(this.knowledgePoint.id, 'why');
      const howSession = await getSessionByKpAndStep(this.knowledgePoint.id, 'how');
      const inProgress = await getInProgressSessionsByKP(this.knowledgePoint.id);
      const inProgressSteps = new Set(inProgress.map(s => s.step));
      if (whatSession !== null) {
        this.whatScore = whatSession.score;
        this.whatStatus = '已完成';
      } else if (inProgressSteps.has('what')) {
        this.whatStatus = '未完成';
      }
      if (whySession !== null) {
        this.whyScore = whySession.score;
        this.whyStatus = '已完成';
      } else if (inProgressSteps.has('why')) {
        this.whyStatus = '未完成';
      }
      if (howSession !== null) {
        this.howScore = howSession.score;
        this.howStatus = '已完成';
      } else if (inProgressSteps.has('how')) {
        this.howStatus = '未完成';
      }
      this.overallScore = ScoreCalculator.calculateOverallScore(this.whatScore, this.whyScore, this.howScore);
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

          .fontWeight(FontWeight.Medium)

          .fontColor(Colors.TEXT)

          .width('100%')

          .margin({ bottom: Spacing.md })



        StepButton({

          icon: '🤔',

          label: STEP_LABELS.what,

          subtitle: '理解概念的定义和内涵',

          score: this.whatScore,

          status: this.whatStatus,

          color: '#8B5CF6',

          onPress: () => {
            router.pushUrl({
              url: 'pages/LearningSessionPage',
              params: { kpId: this.knowledgePoint.id, step: 'what' }
            });
          }
        })

        StepButton({
          icon: '🔍',
          label: STEP_LABELS.why,
          subtitle: '探究原理和逻辑关系',
          score: this.whyScore,
          status: this.whyStatus,
          color: '#3B82F6',
          onPress: () => {
            router.pushUrl({
              url: 'pages/LearningSessionPage',
              params: { kpId: this.knowledgePoint.id, step: 'why' }
            });
          }
        })

        StepButton({
          icon: '💡',
          label: STEP_LABELS.how,
          subtitle: '掌握实践和应用方法',
          score: this.howScore,
          status: this.howStatus,
          color: '#10B981',
          onPress: () => {
            router.pushUrl({
              url: 'pages/LearningSessionPage',
              params: { kpId: this.knowledgePoint.id, step: 'how' }
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

  icon: string = '';

  label: string = '';

  subtitle: string = '';

  score: number = 0;

  status: string = '未开始';

  color: string = '#3B82F6';

  onPress: () => void = () => {};



  build() {

    Row() {

      Text(this.icon)

        .fontSize(28)

      Column() {

        Text(this.label)

          .fontSize(15)

          .fontWeight(FontWeight.Medium)

          .fontColor(Colors.TEXT)

        Text(this.subtitle)

          .fontSize(12)

          .fontColor(Colors.TEXT_SECONDARY)

          .margin({ top: 2 })

      }

      .layoutWeight(1)

      .margin({ left: Spacing.md })

      Text(this.status == '已完成' ? '已完成' : this.status == '未完成' ? '未完成' : '未开始')

        .fontSize(11)

        .fontColor(this.status === '已完成' ? Colors.SUCCESS : this.status === '未完成' ? '#F59E0B' : Colors.TEXT_LIGHT)

      if (this.score > 0) {

        Text(this.score + '分')

          .fontSize(14)

          .fontWeight(FontWeight.Bold)

          .fontColor(this.score >= 60 ? Colors.SUCCESS : Colors.WARNING)

          .margin({ left: 6 })

      }

    }

    .padding(Spacing.md)

    .backgroundColor('#F8FAFC')

    .borderRadius(Radius.sm)

    .margin({ bottom: Spacing.sm })

    .onClick(() => { this.onPress(); })

  }

}

