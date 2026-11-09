import router from '@ohos.router';

import { getCourseById, getKnowledgePoints, getSessionByKpAndStep, getInProgressSessionsByKP } from '../service/DatabaseHelper';

import { Course, KnowledgePoint, LearningSession } from '../model/DataModel';

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

  @State kpStatus: number[] = [];

  @State kpStatusLabel: string[] = [];

  @State completedSteps: number = 0;

  @State totalSteps: number = 0;

  @State isLoading: boolean = true;

  @State currentTab: number = 0;



  aboutToAppear(): void {

    const params = router.getParams() as Record<string, Object>;

    if (params !== null) {

      const idParam = params['courseId'];

      if (idParam !== undefined) {

        this.courseId = Number(idParam);

      }

    }

    this.loadData();

  }

  onPageShow(): void {

    this.loadData();

  }



  async loadData(): Promise<void> {

    try {

      console.info('[CourseDetailPage] Loading course with id: ' + this.courseId);
      this.course = await getCourseById(this.courseId);

      console.info('[CourseDetailPage] Course loaded: ' + JSON.stringify(this.course ? this.course.name : 'null') + ' id=' + this.courseId);

      this.knowledgePoints = await getKnowledgePoints(this.courseId);

      console.info('[CourseDetailPage] Knowledge points loaded: ' + this.knowledgePoints.length);
      
      if (this.knowledgePoints.length > 0) {
        console.info('[CourseDetailPage] First KP: ' + JSON.stringify(this.knowledgePoints[0]));
      }

      const status: number[] = [];
      const labels: string[] = [];
      let completed = 0;
      const total = this.knowledgePoints.length * 3;
      for (const kp of this.knowledgePoints) {
        const what = await getSessionByKpAndStep(kp.id, 'what');
        const why = await getSessionByKpAndStep(kp.id, 'why');
        const how = await getSessionByKpAndStep(kp.id, 'how');
        const inProgress = await getInProgressSessionsByKP(kp.id);
        const completedSessions = [what, why, how].filter(s => s?.status === 'completed');
        const done = completedSessions.length;
        completed += done;
        if (done === 3) {
          status.push(3);
          labels.push('已完成');
        } else if (done > 0) {
          status.push(2);
          labels.push('部分完成');
        } else if (inProgress.length > 0) {
          status.push(1);
          labels.push('未完成');
        } else {
          status.push(0);
          labels.push('未开始');
        }
      }
      this.kpStatus = status;
      this.kpStatusLabel = labels;
      this.completedSteps = completed;
      this.totalSteps = total;

      this.isLoading = false;
      
      console.info('[CourseDetailPage] Data loading completed. KPs: ' + this.knowledgePoints.length + ', Status: ' + JSON.stringify(this.kpStatus));

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

          .fontWeight(FontWeight.Medium)

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

        // Progress summary

        Row() {

          Text('已完成: ' + this.completedSteps + '/' + this.totalSteps + ' 步骤')

            .fontSize(13)

            .fontColor(Colors.SUCCESS)

          Text('未完成: ' + (this.totalSteps - this.completedSteps) + '/' + this.totalSteps + ' 步骤')

            .fontSize(13)

            .fontColor(Colors.WARNING)

            .margin({ left: Spacing.md })

        }

        .padding({ left: Spacing.lg, right: Spacing.lg, bottom: Spacing.sm })

        .width('100%')

        // Knowledge Point selector

        Scroll() {

          Row() {

            ForEach(this.knowledgePoints, (kp: KnowledgePoint, index: number) => {

              Row() {

                Circle()

                  .width(8)

                  .height(8)

                  .fill(this.kpStatus[index] === 3 ? Colors.SUCCESS : this.kpStatus[index] === 2 ? Colors.WARNING : this.kpStatus[index] === 1 ? '#F59E0B' : Colors.BORDER)

                  .margin({ right: 6 })

                Column() {

                  Text(kp.title)

                    .fontSize(13)

                    .fontColor(this.selectedKPIndex === index ? Colors.CARD : Colors.TEXT_SECONDARY)

                  Text(this.kpStatusLabel[index])

                    .fontSize(10)

                    .fontColor(this.selectedKPIndex === index ? Colors.CARD : Colors.TEXT_LIGHT)

                    .opacity(0.8)

                }

                .alignItems(HorizontalAlign.Center)

              }

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

        .height(64)

        .width('100%')



        // Tab bar

        Row() {

          Column() {

            Text('学习')

              .fontSize(15)

              .fontWeight(this.currentTab === 0 ? FontWeight.Medium : FontWeight.Regular)

              .fontColor(this.currentTab === 0 ? Colors.PRIMARY : Colors.TEXT_SECONDARY)

            Divider()

              .width('50%')

              .color(this.currentTab === 0 ? Colors.PRIMARY : 'transparent')

              .strokeWidth(2)

              .margin({ top: 4 })

          }

          .layoutWeight(1)

          .alignItems(HorizontalAlign.Center)

          .onClick(() => { this.currentTab = 0; })

          Column() {

            Text('复习')

              .fontSize(15)

              .fontWeight(this.currentTab === 1 ? FontWeight.Medium : FontWeight.Regular)

              .fontColor(this.currentTab === 1 ? Colors.PRIMARY : Colors.TEXT_SECONDARY)

            Divider()

              .width('50%')

              .color(this.currentTab === 1 ? Colors.PRIMARY : 'transparent')

              .strokeWidth(2)

              .margin({ top: 4 })

          }

          .layoutWeight(1)

          .alignItems(HorizontalAlign.Center)

          .onClick(() => { this.currentTab = 1; })

          Column() {

            Text('统计')

              .fontSize(15)

              .fontWeight(this.currentTab === 2 ? FontWeight.Medium : FontWeight.Regular)

              .fontColor(this.currentTab === 2 ? Colors.PRIMARY : Colors.TEXT_SECONDARY)

            Divider()

              .width('50%')

              .color(this.currentTab === 2 ? Colors.PRIMARY : 'transparent')

              .strokeWidth(2)

              .margin({ top: 4 })

          }

          .layoutWeight(1)

          .alignItems(HorizontalAlign.Center)

          .onClick(() => { this.currentTab = 2; })

        }

        .width('100%')

        .padding({ left: Spacing.lg, right: Spacing.lg, top: Spacing.md })



        // Tab content

        if (this.currentTab === 0) {

          if (this.knowledgePoints.length > 0 && this.selectedKPIndex < this.knowledgePoints.length) {

            LearnTab({ knowledgePoint: this.knowledgePoints[this.selectedKPIndex] })

              .padding(Spacing.lg)

              .layoutWeight(1)

          } else {

            Column() {

              Text('暂无知识点')

                .fontSize(15)

                .fontColor(Colors.TEXT_SECONDARY)

                .margin({ top: 40 })

            }

            .layoutWeight(1)

            .width('100%')

            .alignItems(HorizontalAlign.Center)

          }

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





