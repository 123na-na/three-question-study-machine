import router from '@ohos.router';

import { getKnowledgePointById, getReviewRecord, getCompletedSessionCount, getAvgScore } from '../service/DatabaseHelper';

import { KnowledgePoint, ReviewRecord } from '../model/DataModel';

import { Colors, Spacing, Radius } from '../constants/Theme';

import { promptAction } from '@kit.ArkUI';



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

          .fontWeight(FontWeight.Medium)

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

