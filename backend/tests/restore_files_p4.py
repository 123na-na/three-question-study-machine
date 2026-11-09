"""Part 4: Restore pages with Chinese content & component files"""
import os

BASE = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

def write_file(rel_path, content):
    fp = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Restored: {rel_path}')

# ---- LoginPage.ets ----
write_file('pages/LoginPage.ets', """\
import router from '@ohos.router';
import { getNickname, setNickname, getUserId } from '../service/AuthService';
import { loadSampleCoursesIfNeeded } from '../service/SampleCourseLoader';
import { Spacing } from '../constants/Theme';
import { Colors } from '../constants/Theme';
import { Radius } from '../constants/Theme';
import { promptAction } from '@kit.ArkUI';

@Entry
@Component
struct LoginPage {
  @State nickname: string = '';
  @State isLoading: boolean = false;
  @State showSlogan: boolean = false;

  aboutToAppear(): void {
    getNickname().then((name) => {
      if (name) {
        this.nickname = name;
      }
    });
    setTimeout(() => {
      this.showSlogan = true;
    }, 300);
  }

  build() {
    Column() {
      // Logo & Title
      Column() {
        Text('📖')
          .fontSize(64)
          .margin({ bottom: Spacing.md })

        Text('三问高效学习机')
          .fontSize(28)
          .fontWeight(FontWeight.Bold)
          .fontColor(Colors.TEXT)

        Text('是什么 → 为什么 → 怎么用')
          .fontSize(15)
          .fontColor(Colors.TEXT_SECONDARY)
          .margin({ top: Spacing.sm, bottom: Spacing.xl })
          .textAlign(TextAlign.Center)
          .opacity(this.showSlogan ? 1 : 0)
          .animation({ duration: 800, curve: Curve.FadeIn })
      }
      .width('100%')
      .padding({ top: 60, bottom: 40 })
      .justifyContent(FlexAlign.Center)
      .alignItems(HorizontalAlign.Center)

      // Nickname Input
      Column() {
        TextInput({ placeholder: '输入昵称开始学习', text: this.nickname })
          .width('85%')
          .height(48)
          .fontSize(16)
          .placeholderColor(Colors.TEXT_LIGHT)
          .borderRadius(Radius.lg)
          .backgroundColor(Colors.CARD)
          .border({ width: 1, color: Colors.BORDER })
          .padding({ left: Spacing.lg })
          .maxLength(20)
          .onChange((val: string) => {
            this.nickname = val.trim();
          })
      }
      .width('100%')
      .alignItems(HorizontalAlign.Center)
      .margin({ bottom: Spacing.xxl })

      // Start Button
      Button('开始学习')
        .width('85%')
        .height(50)
        .backgroundColor(Colors.PRIMARY)
        .borderRadius(Radius.lg)
        .fontSize(18)
        .fontWeight(FontWeight.Medium)
        .enabled(this.nickname.length > 0 && !this.isLoading)
        .opacity(this.nickname.length > 0 ? 1 : 0.5)
        .onClick(() => {
          this.startLearning();
        })

      // Loading indicator
      if (this.isLoading) {
        LoadingProgress()
          .width(32)
          .height(32)
          .color(Colors.PRIMARY)
          .margin({ top: Spacing.lg })
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor(Colors.BG)
    .linearGradient({
      direction: GradientDirection.Bottom,
      colors: [['#EFF6FF', 0], ['#F1F5F9', 1]]
    })
    .justifyContent(FlexAlign.Start)
    .alignItems(HorizontalAlign.Center)
  }

  async startLearning(): Promise<void> {
    if (!this.nickname || this.nickname.trim().length === 0) {
      return;
    }
    this.isLoading = true;
    try {
      await setNickname(this.nickname);
      await getUserId();
      await loadSampleCoursesIfNeeded();
      router.replaceUrl({ url: 'pages/HomePage' });
    } catch (err) {
      promptAction.showToast({ message: '初始化失败，请重试', duration: 2000 });
      console.error('[LoginPage] startLearning error: ' + JSON.stringify(err));
    } finally {
      this.isLoading = false;
    }
  }
}
""")

# ---- Index.ets (WITH AIService.initFromPreferences edit) ----
write_file('pages/Index.ets', """\
import router from '@ohos.router';
import { isLoggedIn } from '../service/AuthService';
import { initFromPreferences } from '../service/AIService';
import { getCourseCount } from '../service/DatabaseHelper';

@Entry
@Component
struct Index {
  @State showLoading: boolean = true;
  @State statusText: string = '加载中...';
  @State loadingOpacity: number = 1;

  aboutToAppear(): void {
    this.checkStatus();
  }

  async checkStatus(): Promise<void> {
    await initFromPreferences();
    await this.delay(800);
    const loggedIn = await isLoggedIn();
    if (loggedIn) {
      const count = await getCourseCount();
      this.statusText = count > 0 ? '进入学习...' : '准备课程...';
      await this.delay(500);
      router.replaceUrl({ url: 'pages/HomePage' });
    } else {
      this.statusText = '欢迎回来';
      this.loadingOpacity = 0;
      await this.delay(300);
      router.replaceUrl({ url: 'pages/LoginPage' });
    }
  }

  delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  build() {
    Column() {
      Text('📖')
        .fontSize(64)
        .margin({ bottom: 20 })
      Text('三问高效学习机')
        .fontSize(22)
        .fontWeight(FontWeight.Bold)
        .fontColor('#1E293B')
      Text('问枢')
        .fontSize(14)
        .fontColor('#94A3B8')
        .margin({ top: 8 })
      if (this.showLoading) {
        LoadingProgress()
          .width(32)
          .height(32)
          .color('#3B82F6')
          .margin({ top: 40 })
        Text(this.statusText)
          .fontSize(14)
          .fontColor('#94A3B8')
          .margin({ top: 12 })
          .opacity(this.loadingOpacity)
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F8FAFC')
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
  }
}
""")

# ---- HomePage.ets (WITH padding fix edit) ----
write_file('pages/HomePage.ets', """\
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
        Image($r('app.media.app_icon'))
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
          StatCard('📚', this.courses.length.toString(), '课程')
          StatCard('📝', '3', '学习步骤')
          StatCard('🎯', '三问法', '高效学习')
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
            .fontWeight(FontWeight.Semibold)
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
        TabItem('📖', '学习', this.selectedTab === 0, () => { this.selectedTab = 0; })
        TabItem('📊', '统计', this.selectedTab === 1, () => {
          router.pushUrl({ url: 'pages/ProgressDashboardPage' });
        })
        TabItem('👤', '我的', this.selectedTab === 2, () => {
          router.pushUrl({ url: 'pages/LearningReportPage' });
        })
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
  private icon: string = '';
  private value: string = '';
  private label: string = '';

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
  private icon: string = '';
  private label: string = '';
  private active: boolean = false;
  private onClick: () => void = () => {};

  build() {
    Column() {
      Text(this.icon)
        .fontSize(20)
      Text(this.label)
        .fontSize(11)
        .fontColor(this.active ? Colors.PRIMARY : Colors.TEXT_SECONDARY)
        .margin({ top: 2 })
    }
    .onClick(() => { this.onClick(); })
    .padding({ top: 6 })
  }
}

@Component
struct CourseCard {
  @ObjectLink course: Course;

  build() {
    Column() {
      Row() {
        Text('📘')
          .fontSize(28)
        Column() {
          Text(this.course.name)
            .fontSize(16)
            .fontWeight(FontWeight.Semibold)
            .fontColor(Colors.TEXT)
            .maxLines(1)
            .textOverflow({ overflow: TextOverflow.Ellipsis })
          Text(this.course.description || '无描述')
            .fontSize(13)
            .fontColor(Colors.TEXT_SECONDARY)
            .margin({ top: 4 })
            .maxLines(2)
            .textOverflow({ overflow: TextOverflow.Ellipsis })
        }
        .layoutWeight(1)
        .margin({ left: Spacing.md })
        Image($r('app.media.app_icon'))
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
      router.pushUrl({ url: 'pages/CourseDetailPage?courseId=' + this.course.id });
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
""")

# ---- OnboardingOverlay.ets ----
write_file('component/OnboardingOverlay.ets', """\
@Component
export struct OnboardingOverlay {
  @State currentStep: number = 0;
  private onComplete: () => void = () => {};

  private steps: string[] = [
    '📖 欢迎使用三问高效学习机',
    '是什么 - 理解概念的本质',
    '为什么 - 探究原理与逻辑',
    '怎么用 - 掌握实践与应用',
  ];

  private descriptions: string[] = [
    '三步学习法，系统化掌握每一个知识点',
    '首先明确学习对象的基本定义和概念',
    '深入理解背后的原理和逻辑关系',
    '最后通过实践巩固所学知识',
  ];

  build() {
    Column() {
      // Dots
      Row() {
        ForEach(this.steps, (_: string, index: number) => {
          Circle()
            .width(index === this.currentStep ? 10 : 6)
            .height(index === this.currentStep ? 10 : 6)
            .fill(index === this.currentStep ? '#3B82F6' : '#CBD5E1')
            .margin({ left: 4, right: 4 })
        })
      }
      .width('100%')
      .justifyContent(FlexAlign.Center)
      .margin({ top: 40 })

      // Content
      Column() {
        Text(this.steps[this.currentStep])
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
          .fontColor('#1E293B')
          .textAlign(TextAlign.Center)
          .margin({ top: 30, bottom: 16 })
        Text(this.descriptions[this.currentStep])
          .fontSize(15)
          .fontColor('#64748B')
          .textAlign(TextAlign.Center)
          .lineHeight(22)
          .padding({ left: 30, right: 30 })
      }
      .layoutWeight(1)
      .justifyContent(FlexAlign.Center)

      // Button
      Button(this.currentStep < this.steps.length - 1 ? '下一步' : '开始学习')
        .width('80%')
        .height(50)
        .backgroundColor('#3B82F6')
        .borderRadius(12)
        .fontSize(16)
        .fontWeight(FontWeight.Medium)
        .margin({ bottom: 40 })
        .onClick(() => {
          if (this.currentStep < this.steps.length - 1) {
            this.currentStep++;
          } else {
            this.onComplete();
          }
        })
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#FFFFFF')
    .borderRadius(20)
    .justifyContent(FlexAlign.SpaceBetween)
  }
}
""")

print('Part 4: LoginPage, Index, HomePage, OnboardingOverlay restored')
print('Run part 5 for remaining pages and components')
