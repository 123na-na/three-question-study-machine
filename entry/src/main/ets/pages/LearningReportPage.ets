import router from '@ohos.router';

import { getAllCourses, getKpCount, getCompletedSessionCount, getAvgScore } from '../service/DatabaseHelper';

import { Course } from '../model/DataModel';

import { Colors, Spacing, Radius } from '../constants/Theme';



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

    let report = '📊 学习报告\n\n';

    report += '👤 ' + this.nickname + '\n';

    report += '📅 ' + now.getFullYear() + '年' + (now.getMonth() + 1) + '月' + now.getDate() + '日\n\n';

    report += '📚 学习概况:\n';

    report += '  课程数: ' + this.courses.length + '\n';

    report += '  总知识点: ' + this.totalKps + '\n';

    report += '  已完成学习: ' + this.completedKps + '\n';

    report += '  综合评分: ' + this.overallScore + '分\n\n';

    report += '📖 课程详情:\n';

    for (const course of this.courses) {

      report += '  📘 ' + course.name + '\n';

    }

    report += '\n💪 继续加油，坚持三问学习法！';

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

          .fontWeight(FontWeight.Medium)

          .fontColor(Colors.TEXT)

          .layoutWeight(1)

          .textAlign(TextAlign.Center)

        if (this.reportGenerated) {

          Text('分享')

            .fontSize(16)

            .fontColor(Colors.PRIMARY)

            .onClick(() => {

              const context = getContext(this);

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

            OverviewCard({ icon: '📚', value: this.courses.length.toString(), label: '课程' })

            OverviewCard({ icon: '📝', value: this.totalKps.toString(), label: '知识点' })

            OverviewCard({ icon: '✅', value: this.completedKps.toString(), label: '已完成' })

            OverviewCard({ icon: '🎯', value: this.overallScore + '分', label: '平均分' })

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

  icon: string = '';

  value: string = '';

  label: string = '';



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

