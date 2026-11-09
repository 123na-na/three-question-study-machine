import router from '@ohos.router';

import { getAllCourses, getKpCount, getCompletedSessionCount, getAvgScore, getPreference, setPreference } from '../service/DatabaseHelper';

import { Course } from '../model/DataModel';

import { Spacing, Colors, Radius } from '../constants/Theme';

import { getNickname } from '../service/AuthService';

import { promptAction } from '@kit.ArkUI';



@Entry

@Component

struct HomePage {

  @State courses: Course[] = [];

  @State nickname: string = '';

  @State isLoading: boolean = true;

  @State selectedTab: number = 0;

  @State showSuggestions: boolean = false;



  aboutToAppear(): void {

    this.loadData();

  }



  async loadData(): Promise<void> {

    try {

      this.nickname = (await getNickname()) || '同学';

      this.courses = await getAllCourses();

      this.isLoading = false;

      setTimeout(() => {

        this.showSuggestions = true;

      }, 500);

    } catch (err) {

      console.error('[HomePage] loadData error: ' + JSON.stringify(err));

      this.isLoading = false;

    }

  }



  build() {

    Column() {

      // Header

      Row() {

        Column() {

          Text('Hi, ' + this.nickname)

            .fontSize(22)

            .fontWeight(FontWeight.Bold)

            .fontColor(Colors.TEXT)

          Text('今天想学什么？')

            .fontSize(15)

            .fontColor(Colors.TEXT_SECONDARY)

            .margin({ top: 4 })

        }

        .alignItems(HorizontalAlign.Start)

        .layoutWeight(1)

        Circle().width(40).height(40).fill(Colors.PRIMARY_LIGHT)

          .width(40)

          .height(40)

          .borderRadius(20)

          .border({ width: 2, color: Colors.PRIMARY_LIGHT })

      }

      .width('100%')

      .padding({ left: Spacing.lg, right: Spacing.lg, top: 16 })



      // Quick Stats

      if (!this.isLoading) {

        Row() {

          StatCard({ icon: '📚', value: this.courses.length.toString(), label: '课程' })

          StatCard({ icon: '📝', value: '3', label: '学习步骤' })

          StatCard({ icon: '🎯', value: '三问法', label: '高效学习' })

        }

        .width('100%')

        .padding({ left: Spacing.lg, right: Spacing.lg, top: Spacing.lg })

        .justifyContent(FlexAlign.SpaceBetween)

      }



      // Course List

      Column() {

        Row() {

          Text('我的课程')

            .fontSize(18)

            .fontWeight(FontWeight.Medium)

            .fontColor(Colors.TEXT)

        }

        .width('100%')

        .padding({ left: Spacing.lg, right: Spacing.lg, top: Spacing.xl, bottom: Spacing.md })



        if (this.isLoading) {

          LoadingProgress()

            .width(32)

            .height(32)

            .color(Colors.PRIMARY)

            .margin({ top: 40 })

        } else if (this.courses.length === 0) {

          EmptyState()

        } else {

          List() {

            ForEach(this.courses, (course: Course) => {

              ListItem() {

                CourseCard({ course: course })

              }

            }, (course: Course) => course.id.toString())

          }

          .width('100%')

          .layoutWeight(1)

          .padding({ left: Spacing.lg, right: Spacing.lg })

        }

      }

      .layoutWeight(1)

      .width('100%')



      // Tab bar

      Row() {

        TabItem({ icon: '📖', label: '学习', active: this.selectedTab === 0, onPress: () => { this.selectedTab = 0; } })

        TabItem({ icon: '📊', label: '统计', active: this.selectedTab === 1, onPress: () => { router.pushUrl({ url: 'pages/ProgressDashboardPage' }); } })

        TabItem({ icon: '👤', label: '我的', active: this.selectedTab === 2, onPress: () => { router.pushUrl({ url: 'pages/LearningReportPage' }); } })

      }

      .width('100%')

      .height(56)

      .backgroundColor(Colors.CARD)

      .borderRadius({ topLeft: Radius.lg, topRight: Radius.lg })

      .shadow({ radius: 8, color: Colors.SHADOW_DARK, offsetY: -2 })

      .padding({ left: Spacing.lg, right: Spacing.lg })

      .justifyContent(FlexAlign.SpaceAround)

    }

    .width('100%')

    .height('100%')

    .backgroundColor(Colors.BG)

  }

}



@Component

struct StatCard {

  icon: string = '';

  value: string = '';

  label: string = '';



  build() {

    Column() {

      Text(this.icon)

        .fontSize(24)

      Text(this.value)

        .fontSize(18)

        .fontWeight(FontWeight.Bold)

        .fontColor(Colors.TEXT)

        .margin({ top: 4 })

      Text(this.label)

        .fontSize(12)

        .fontColor(Colors.TEXT_SECONDARY)

    }

    .padding({ top: Spacing.md, bottom: Spacing.md, left: Spacing.xl, right: Spacing.xl })

    .backgroundColor(Colors.CARD)

    .borderRadius(Radius.md)

    .shadow({ radius: 4, color: Colors.SHADOW })

  }

}



@Component

struct TabItem {

  icon: string = '';

  label: string = '';

  active: boolean = false;

  onPress: () => void = () => {};



  build() {

    Column() {

      Text(this.icon)

        .fontSize(20)

      Text(this.label)

        .fontSize(11)

        .fontColor(this.active ? Colors.PRIMARY : Colors.TEXT_SECONDARY)

        .margin({ top: 2 })

    }

    .onClick(() => { this.onPress(); })

    .padding({ top: 6 })

  }

}



@Component

struct CourseCard {

  course: Course | null = null;

  build() {

    Column() {

      Row() {

        Text('📘')

          .fontSize(28)

        Column() {

          Text(this.course?.name ?? '')

            .fontSize(16)

            .fontWeight(FontWeight.Medium)

            .fontColor(Colors.TEXT)

            .maxLines(1)

            .textOverflow({ overflow: TextOverflow.Ellipsis })

          Text(this.course?.description || '无描述')

            .fontSize(13)

            .fontColor(Colors.TEXT_SECONDARY)

            .margin({ top: 4 })

            .maxLines(2)

            .textOverflow({ overflow: TextOverflow.Ellipsis })

        }

        .layoutWeight(1)

        .margin({ left: Spacing.md })

        Circle().width(40).height(40).fill(Colors.PRIMARY_LIGHT)

          .width(20)

          .height(20)

          .rotate({ angle: 90 })

      }

      .padding(Spacing.lg)

    }

    .width('100%')

    .backgroundColor(Colors.CARD)

    .borderRadius(Radius.md)

    .shadow({ radius: 4, color: Colors.SHADOW })

    .margin({ bottom: Spacing.md })

    .onClick(() => {

      if (this.course) { router.pushUrl({ url: 'pages/CourseDetailPage', params: { courseId: this.course.id } }); }

    })

  }

}



@Component

struct EmptyState {

  build() {

    Column() {

      Text('📚')

        .fontSize(48)

        .margin({ top: 40 })

      Text('还没有课程')

        .fontSize(16)

        .fontColor(Colors.TEXT_SECONDARY)

        .margin({ top: Spacing.md })

      Text('返回登录页面重新初始化')

        .fontSize(13)

        .fontColor(Colors.TEXT_LIGHT)

        .margin({ top: Spacing.sm })

    }

    .width('100%')

    .alignItems(HorizontalAlign.Center)

  }

}

