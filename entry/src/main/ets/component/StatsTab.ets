import { Colors, Spacing, Radius } from '../constants/Theme';

import { getAllCourses, getKpCount, getCompletedSessionCountByCourse, getAvgScoreByCourse } from '../service/DatabaseHelper';

import { Course } from '../model/DataModel';



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

        .fontWeight(FontWeight.Medium)

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

  @Prop course: Course;

  isExpanded: boolean = false;

  onToggle: () => void = () => {};

  @State kpCount: number = 0;

  @State completedCount: number = 0;

  @State avgScore: number = 0;



  aboutToAppear(): void {

    this.loadCourseStats();

  }



  async loadCourseStats(): Promise<void> {

    try {

      this.kpCount = await getKpCount(this.course.id);

      this.completedCount = await getCompletedSessionCountByCourse(this.course.id);

      this.avgScore = await getAvgScoreByCourse(this.course.id);

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

            .fontWeight(FontWeight.Medium)

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



interface MasteryRange {
  min: number;
  max: number;
  label: string;
  color: string;
}

@Component

struct MasteryBar {

  label: string = '';

  range: MasteryRange = { min: 0, max: 0, label: '', color: '' };

  score: number = 0;

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

