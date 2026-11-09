import router from '@ohos.router';

import { getAllCourses, getKpCount, getCompletedSessionCount, getAvgScore } from '../service/DatabaseHelper';

import { Course, Achievement } from '../model/DataModel';

import { Colors, Spacing, Radius } from '../constants/Theme';



import { getAchievementDefs, getUnlockedAchievements, checkAndUnlockAchievements, AchievementDef, UserStats } from '../service/AchievementService';



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



      const userStats: UserStats = {

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

        Scroll() {

          Column() {

            // Overall progress card

            Column() {

              Text('总体进度')

                .fontSize(16)

                .fontWeight(FontWeight.Medium)

                .fontColor(Colors.TEXT)

              Text(this.overallProgress + '%')

                .fontSize(36)

                .fontWeight(FontWeight.Bold)

                .fontColor(Colors.PRIMARY)

                .margin({ top: Spacing.md })



              Row() {

                StatItem({ label: '总知识点', value: this.totalKps.toString() })

                StatItem({ label: '已完成', value: this.completedKps.toString() })

                StatItem({ label: '平均分', value: this.overallAvgScore + '分' })

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

                .fontWeight(FontWeight.Medium)

                .fontColor(Colors.TEXT)

                .width('100%')

                .margin({ bottom: Spacing.md })



              if (getUnlockedAchievements().length === 0) {

                Column() {

                  ForEach(getAchievementDefs(), (def: AchievementDef) => {

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

                  ForEach(getUnlockedAchievements(), (ach: Achievement) => {

                    Row() {

                      Text(ach.icon)

                        .fontSize(28)

                      Column() {

                        Text(ach.name)

                          .fontSize(15)

                          .fontWeight(FontWeight.Medium)

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

  label: string = '';

  value: string = '';



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

